import uuid
import time
import subprocess
import os
import sys
import socket
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .client import DataflowClient

User = get_user_model()

class DataflowIntegrationTest(TestCase):
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
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    def test_client_list_operators(self):
        client = DataflowClient()
        operators = client.list_operators()
        self.assertIsInstance(operators, list)
        self.assertTrue(len(operators) > 0)
        self.assertEqual(operators[0]['id'], "op_llm_extract")

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    def test_operator_list_view(self):
        url = reverse('operator-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['code'], 0)
        self.assertTrue(len(response.data['data']) > 0)

    @override_settings(DATAFLOW_SERVICE_URL="http://localhost:8001")
    def test_pipeline_status_view(self):
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
