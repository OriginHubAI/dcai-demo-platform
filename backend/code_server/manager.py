import shutil
import socket
import subprocess
import threading
import time
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen

from django.conf import settings


EDITOR_BINARIES = (
    'opencode',
)

IGNORE_NAMES = (
    '.git',
    '__pycache__',
    '.pytest_cache',
    '.mypy_cache',
    '.ruff_cache',
    '.venv',
    'node_modules',
    '.DS_Store',
)


@dataclass
class EditorSession:
    package_id: str
    repo_path: str
    mode: str
    sandbox_path: str = ''
    package_path: str = ''
    session_id: str = ''
    session_directory: str = ''
    port: Optional[int] = None
    process: Optional[subprocess.Popen] = None
    url: Optional[str] = None
    reason: str = ''


class CodeServerManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._sessions: dict[str, EditorSession] = {}
        self._binary = self._detect_binary()
        self._port = int(getattr(settings, 'PACKAGE_EDITOR_PORT', 18004))
        self._sandbox_root = Path(getattr(settings, 'PACKAGE_EDITOR_SANDBOX_ROOT')).resolve()

    def _detect_binary(self) -> Optional[str]:
        for binary in EDITOR_BINARIES:
            if shutil.which(binary):
                return binary
        return None

    def _is_port_open(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(('127.0.0.1', port)) == 0

    def _build_command(self, port: int) -> list[str]:
        return [
            self._binary,
            'web',
            '--hostname',
            '0.0.0.0',
            '--port',
            str(port),
        ]

    def _wait_until_ready(self, url: str, timeout: float = 20.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                with urlopen(url, timeout=2):
                    return True
            except Exception:
                time.sleep(0.5)
        return False

    def _active_session(self) -> Optional[EditorSession]:
        for session in self._sessions.values():
            if session.process and session.process.poll() is None:
                return session
        return None

    def _stop_session(self, session: EditorSession) -> None:
        if session.process and session.process.poll() is None:
            session.process.terminate()
            try:
                session.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                session.process.kill()

    def _release_port(self) -> None:
        if not self._is_port_open(self._port):
            return
        if shutil.which('fuser'):
            subprocess.run(
                ['fuser', '-k', f'{self._port}/tcp'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            time.sleep(0.5)

    def _build_sandbox(self, package_id: str, repo_path: str) -> tuple[Path, Path]:
        source_repo = Path(repo_path).resolve()
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        sandbox_dir = self._sandbox_root / f'{package_id}-{timestamp}'
        workspace_dir = sandbox_dir / 'workspace'
        shutil.copytree(
            source_repo,
            workspace_dir,
            ignore=shutil.ignore_patterns(*IGNORE_NAMES),
        )
        package_path = workspace_dir / 'dataflow' / 'operators' / package_id
        if not package_path.exists():
            raise FileNotFoundError(f'Package path not found in sandbox: {package_id}')
        return sandbox_dir, package_path

    def _create_session(self, base_url: str) -> tuple[str, str]:
        payload = json.dumps({}).encode('utf-8')
        request = Request(
            f'{base_url.rstrip("/")}/session',
            data=payload,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        return data.get('id', ''), data.get('directory', '')

    def get_or_start(self, package_id: str, repo_path: str) -> EditorSession:
        repo_path = str(Path(repo_path).resolve())
        with self._lock:
            existing = self._sessions.get(package_id)
            if existing and existing.process and existing.process.poll() is None:
                return existing

            active = self._active_session()
            if active and active.package_id != package_id:
                self._sessions.pop(active.package_id, None)
                self._stop_session(active)

            if not self._binary:
                session = EditorSession(
                    package_id=package_id,
                    repo_path=repo_path,
                    mode='preview',
                    reason='No opencode binary found in PATH',
                )
                self._sessions[package_id] = session
                return session

            sandbox_dir, package_path = self._build_sandbox(package_id, repo_path)
            if self._is_port_open(self._port):
                self._release_port()
            process = subprocess.Popen(
                self._build_command(self._port),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=package_path,
            )
            session = EditorSession(
                package_id=package_id,
                repo_path=str(package_path),
                sandbox_path=str(sandbox_dir),
                package_path=str(package_path),
                mode='external',
                port=self._port,
                process=process,
                url=f'http://127.0.0.1:{self._port}/',
            )
            if not self._wait_until_ready(session.url):
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                session.mode = 'preview'
                session.process = None
                session.url = None
                session.reason = 'OpenCode failed to start within timeout'
            elif session.url:
                try:
                    session.session_id, session.session_directory = self._create_session(session.url)
                except Exception:
                    session.reason = 'OpenCode started, but session creation failed'
            self._sessions[package_id] = session
            return session

    def stop(self, package_id: str) -> bool:
        with self._lock:
            session = self._sessions.pop(package_id, None)
            if not session:
                return False
            self._stop_session(session)
            return True

    def stop_all(self) -> None:
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        for session in sessions:
            self._stop_session(session)


manager = CodeServerManager()
