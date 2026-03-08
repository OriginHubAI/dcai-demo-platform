import shutil
import socket
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from django.conf import settings


EDITOR_BINARIES = (
    'code-server',
    'openvscode-server',
)


@dataclass
class EditorSession:
    package_id: str
    repo_path: str
    mode: str
    port: Optional[int] = None
    process: Optional[subprocess.Popen] = None
    url: Optional[str] = None
    reason: str = ''


class CodeServerManager:
    def __init__(self):
        self._lock = threading.Lock()
        self._sessions: dict[str, EditorSession] = {}
        self._binary = self._detect_binary()
        self._base_port = int(getattr(settings, 'CODE_SERVER_BASE_PORT', 18080))

    def _detect_binary(self) -> Optional[str]:
        for binary in EDITOR_BINARIES:
            if shutil.which(binary):
                return binary
        return None

    def _find_free_port(self, start: int) -> int:
        port = start
        while port < start + 200:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex(('127.0.0.1', port)) != 0:
                    return port
            port += 1
        raise RuntimeError('No free port available for editor session')

    def _build_command(self, repo_path: str, port: int) -> list[str]:
        if self._binary == 'code-server':
            return [
                self._binary,
                '--bind-addr',
                f'127.0.0.1:{port}',
                '--auth',
                'none',
                repo_path,
            ]
        return [
            self._binary,
            '--host',
            '127.0.0.1',
            '--port',
            str(port),
            '--without-connection-token',
            repo_path,
        ]

    def get_or_start(self, package_id: str, repo_path: str) -> EditorSession:
        repo_path = str(Path(repo_path).resolve())
        with self._lock:
            existing = self._sessions.get(package_id)
            if existing:
                return existing

            if not self._binary:
                session = EditorSession(
                    package_id=package_id,
                    repo_path=repo_path,
                    mode='preview',
                    reason='No code-server/openvscode-server binary found in PATH',
                )
                self._sessions[package_id] = session
                return session

            port = self._find_free_port(self._base_port + len(self._sessions))
            process = subprocess.Popen(
                self._build_command(repo_path, port),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=repo_path,
            )
            session = EditorSession(
                package_id=package_id,
                repo_path=repo_path,
                mode='external',
                port=port,
                process=process,
                url=f'http://127.0.0.1:{port}/',
            )
            self._sessions[package_id] = session
            return session

    def stop(self, package_id: str) -> bool:
        with self._lock:
            session = self._sessions.pop(package_id, None)
            if not session:
                return False
            if session.process and session.process.poll() is None:
                session.process.terminate()
                try:
                    session.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    session.process.kill()
            return True

    def stop_all(self) -> None:
        for package_id in list(self._sessions):
            self.stop(package_id)


manager = CodeServerManager()
