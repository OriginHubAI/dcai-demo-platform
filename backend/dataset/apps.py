import os
import subprocess
import time
import sys
import socket
from django.apps import AppConfig
from django.conf import settings

class DatasetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dataset'

    def ready(self):
        if not getattr(settings, 'ENABLE_MOCK_HF', False):
            return

        # Avoid starting the mock server during migrations, collecting static, etc.
        if 'runserver' not in sys.argv:
            return
        
        # Check if we are in the main process (not the reloader)
        if os.environ.get('RUN_MAIN') == 'true':
            self._start_mock_hf_server()

    def _start_mock_hf_server(self):
        service_url = settings.HF_SERVICE_URL
        try:
            port = int(service_url.split(':')[-1].rstrip('/'))
        except (ValueError, IndexError):
            port = 8002

        # Check if port is already in use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                print(f"[*] Mock HF Server: Port {port} already in use, assuming it's already running.")
                return

        print(f"[*] Starting Mock HF Server on port {port}...")
        
        mock_server_path = os.path.join(settings.BASE_DIR, 'fastapi_app', 'mock_hf.py')
        
        # Start uvicorn process
        try:
            # We also pass HF_ENDPOINT to the environment so datasets library uses it
            env = os.environ.copy()
            env["HF_ENDPOINT"] = settings.HF_SERVICE_URL
            
            subprocess.Popen(
                [sys.executable, mock_server_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env
            )
            print(f"[*] Mock HF Server started successfully.")
        except Exception as e:
            print(f"[!] Failed to start Mock HF Server: {e}")
