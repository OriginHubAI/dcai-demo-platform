import os
import subprocess
import time
import sys
import socket
import atexit

from django.apps import AppConfig
from django.conf import settings

class DataflowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'df'
    verbose_name = 'DataFlow'

    _cleanup_registered = False

    def ready(self):
        if not self.__class__._cleanup_registered:
            from code_server.manager import manager as code_server_manager
            atexit.register(code_server_manager.stop_all)
            self.__class__._cleanup_registered = True

        if getattr(settings, 'ENABLE_MOCK_DATAFLOW', False):
            # Avoid starting the mock server during migrations, collecting static, etc.
            # Only start if it's the actual runserver process (not the reloader)
            if 'runserver' in sys.argv:
                # Check if we are in the main process (not the reloader)
                # Django's reloader sets RUN_MAIN to 'true' in the child process
                if os.environ.get('RUN_MAIN') == 'true':
                    self._start_mock_server()

    def _start_mock_server(self):
        service_url = getattr(settings, 'DATAFLOW_SYSTEM_URL', 'http://127.0.0.1:8001')
        # Extract port from URL (e.g., http://localhost:8001 -> 8001)
        try:
            port = int(service_url.split(':')[-1].rstrip('/'))
        except (ValueError, IndexError):
            port = 8001

        # Check if port is already in use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                print(f"[*] Mock Dataflow System: Port {port} already in use, assuming it's already running.")
                return

        print(f"[*] Starting Mock Dataflow System on port {port}...")
        
        mock_server_path = os.path.join(settings.BASE_DIR, 'fastapi_app', 'mock_dataflow.py')
        
        # Start uvicorn process
        try:
            subprocess.Popen(
                [sys.executable, mock_server_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=os.environ.copy()
            )
            print(f"[*] Mock Dataflow System started successfully.")
        except Exception as e:
            print(f"[!] Failed to start Mock Dataflow System: {e}")
