import uuid
import time
import subprocess
import os
import sys
import socket
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .client import DataflowClient
import unittest.mock
from rest_framework.permissions import IsAuthenticated
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from rest_framework.test import APITestCase
from dataflow.services import DataFlowCatalog

User = get_user_model()

class DataflowIntegrationTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure the mock server is running for integration tests
        cls.mock_server_port = 8001
        cls.mock_server_url = f"http://localhost:{cls.mock_server_port}"
        
        # Check if port is already in use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', cls.mock_server_port)) != 0:
                print(f"[*] Starting Mock Dataflow System for tests...")
                mock_server_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fastapi_app', 'mock_dataflow.py')
                cls.mock_process = subprocess.Popen(
                    [sys.executable, mock_server_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                # Wait for server to start
                time.sleep(2)
            else:
                cls.mock_process = None

    @classmethod
    def tearDownClass(cls):
        if cls.mock_process:
            cls.mock_process.terminate()
            cls.mock_process.wait()
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    def test_client_list_operators(self):
        client = DataflowClient()
        operators = client.list_operators()
        self.assertIsInstance(operators, list)
        self.assertTrue(len(operators) > 0)
        self.assertEqual(operators[0]['id'], "op_llm_extract")

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    @unittest.mock.patch("rest_framework.permissions.IsAuthenticated.has_permission", return_value=True)
    def test_operator_list_view(self, mock_has_permission):
        url = reverse('operator-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], 0)
        self.assertTrue(len(response.data['data']) > 0)

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    @unittest.mock.patch("rest_framework.permissions.IsAuthenticated.has_permission", return_value=True)
    def test_pipeline_status_view(self, mock_has_permission):
        pipeline_id = uuid.uuid4()
        # First create a pipeline via client to ensure it's in the mock DB
        df_client = DataflowClient()
        # Mock request data
        request_data = {
            "pipeline_key_in_backend": str(uuid.uuid4()),
            "priority": 10,
            "pipeline_config": {"name": "test", "task_type": "extract", "nodes": [], "edges": []},
            "datasets_config": [],
            "output_storage_config": {
                "bucket_name": "test", 
                "storage_options": {"key": "k", "secret": "s", "client_kwargs": {"endpoint_url": "http://minio"}},
                "s3_result_directory": "results"
            }
        }
        create_res = df_client.create_pipeline(request_data)
        self.assertEqual(create_res['code'], 0)
        real_pipeline_id = create_res['data']['pipeline_id']

        url = reverse('pipeline-status', kwargs={'pipeline_id': real_pipeline_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], 0)
        self.assertEqual(response.data['data']['status'], "RUNNING")


class DataFlowWorkspaceTests(APITestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        repo_root = Path(self.tempdir.name) / 'DataFlow'
        operators_root = repo_root / 'dataflow' / 'operators'
        package_root = operators_root / 'core_text'
        package_root.mkdir(parents=True)
        (package_root / 'sample_operator.py').write_text('print("ok")\n', encoding='utf-8')
        sandbox_root = Path(self.tempdir.name) / 'sandboxes'
        self.override = override_settings(
            DATAFLOW_OPERATORS_ROOT=str(operators_root),
            DATAFLOW_REPO_ROOT=str(repo_root),
            PACKAGE_EDITOR_SANDBOX_ROOT=str(sandbox_root),
        )
        self.override.enable()

        from dataflow import views as dataflow_views

        self.original_catalog = dataflow_views.catalog
        self.original_binary = dataflow_views.code_server_manager._binary
        self.original_sessions = dict(dataflow_views.code_server_manager._sessions)
        dataflow_views.catalog = DataFlowCatalog()
        dataflow_views.code_server_manager._sessions.clear()
        dataflow_views.code_server_manager._binary = None

    def tearDown(self):
        from dataflow import views as dataflow_views

        dataflow_views.catalog = self.original_catalog
        dataflow_views.code_server_manager._binary = self.original_binary
        dataflow_views.code_server_manager._sessions.clear()
        dataflow_views.code_server_manager._sessions.update(self.original_sessions)
        self.override.disable()
        self.tempdir.cleanup()

    def test_package_listing_and_file_content(self):
        listing = self.client.get('/api/v2/dataflow/packages')
        self.assertEqual(listing.status_code, 200)
        items = listing.json()['data']['list']
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['id'], 'core_text')
        self.assertNotIn('repo_path', items[0])

        tree = self.client.get('/api/v2/dataflow/packages/core_text/files')
        self.assertEqual(tree.status_code, 200)
        self.assertEqual(tree.json()['data']['type'], 'directory')

        content = self.client.get('/api/v2/dataflow/packages/core_text/file', {'path': 'sample_operator.py'})
        self.assertEqual(content.status_code, 200)
        self.assertIn('print("ok")', content.json()['data']['content'])

    def test_editor_start_falls_back_to_preview_mode(self):
        response = self.client.post('/api/v2/dataflow/packages/core_text/editor/start')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['mode'], 'preview')
        self.assertIn('opencode', payload['reason'])

    def test_package_test_runs_compileall(self):
        response = self.client.post('/api/v2/dataflow/packages/core_text/test')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertTrue(payload['success'])
        self.assertIn('compileall', payload['command'])

    @patch('dataflow.proxy_views.httpx.Client')
    def test_proxy_view_uses_sync_client(self, mock_client_cls):
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.request.return_value.status_code = 200
        mock_client.request.return_value.content = b'{"ok": true}'
        mock_client.request.return_value.headers = {'content-type': 'application/json'}

        response = self.client.get('/api/v2/dataflow/operators/list')

        self.assertEqual(response.status_code, 200)
        mock_client.request.assert_called_once()
