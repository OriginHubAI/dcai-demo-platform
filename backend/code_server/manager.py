import os
import signal
import shutil
import socket
import subprocess
import threading
import time
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
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
        configured = Path(getattr(settings, 'PACKAGE_EDITOR_BINARY', '')).expanduser()
        if str(configured).strip() and configured.exists() and configured.is_file():
            return str(configured)
        for binary in EDITOR_BINARIES:
            if shutil.which(binary):
                return binary
        return None

    def _is_port_open(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(('127.0.0.1', port)) == 0

    def _pid_on_port(self, port: int) -> Optional[int]:
        if shutil.which('netstat'):
            result = subprocess.run(
                ['netstat', '-ltnp'],
                capture_output=True,
                text=True,
                check=False,
            )
            suffix = f':{port}'
            for line in result.stdout.splitlines():
                if suffix not in line or 'LISTEN' not in line:
                    continue
                pid_field = line.split()[-1]
                pid = pid_field.split('/', 1)[0]
                if pid.isdigit():
                    return int(pid)
        return None

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

    def _openai_base_url(self) -> str:
        base_url = str(getattr(settings, 'LLM_PROVIDER_BASE_URL', '') or '').strip()
        if not base_url:
            return ''
        parsed = urlparse(base_url)
        if parsed.path.rstrip('/').endswith('/v1'):
            return base_url.rstrip('/')
        return f'{base_url.rstrip("/")}/v1'

    def _has_dedicated_process_group(self, process: subprocess.Popen) -> bool:
        if not hasattr(os, 'getpgid'):
            return False
        try:
            return os.getpgid(process.pid) == process.pid
        except ProcessLookupError:
            return False

    def _signal_process(self, process: subprocess.Popen, sig: int) -> None:
        if self._has_dedicated_process_group(process) and hasattr(os, 'killpg'):
            os.killpg(process.pid, sig)
            return
        os.kill(process.pid, sig)

    def _stop_session(self, session: EditorSession) -> None:
        process = session.process
        if process and process.poll() is None:
            try:
                self._signal_process(process, signal.SIGTERM)
            except ProcessLookupError:
                process = None

            if process is not None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        self._signal_process(process, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    try:
                        process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        pass

        if self._is_port_open(self._port):
            self._release_port()

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
            return

        pid = self._pid_on_port(self._port)
        if not pid:
            return

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            return

        deadline = time.time() + 5
        while time.time() < deadline:
            if not self._is_port_open(self._port):
                return
            time.sleep(0.2)

        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            return
        time.sleep(0.5)

    def _init_package_repo(self, package_path: Path) -> None:
        if not shutil.which('git'):
            return
        if (package_path / '.git').exists():
            return
        subprocess.run(
            ['git', 'init', '-q'],
            cwd=package_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

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
        # Make the operator directory its own git root so OpenCode treats it as
        # an isolated project instead of walking up to the outer workspace repo.
        self._init_package_repo(package_path)
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
            env = os.environ.copy()
            # Keep PWD aligned with the sandbox package path; some Node-based tools
            # consult it instead of the kernel cwd when deriving project roots.
            env['PWD'] = str(package_path)
            api_key = str(getattr(settings, 'LLM_PROVIDER_API_KEY', '') or '').strip()
            if api_key:
                env['OPENAI_API_KEY'] = api_key
                openai_base_url = self._openai_base_url()
                if openai_base_url:
                    env['OPENAI_BASE_URL'] = openai_base_url
            process = subprocess.Popen(
                self._build_command(self._port),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=package_path,
                env=env,
                start_new_session=True,
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
                if self._is_port_open(self._port):
                    self._release_port()
                    return True
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
