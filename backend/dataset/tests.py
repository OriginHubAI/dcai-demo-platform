import os
import sys
import time
import socket
import subprocess
import unittest
import unittest.mock
import requests
from django.test import SimpleTestCase
from django.conf import settings

# Set HF_ENDPOINT before importing datasets or huggingface_hub
os.environ["HF_ENDPOINT"] = "http://localhost:8002"

try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False

class MockHFServerTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_server_port = 8002
        cls.mock_server_url = f"http://localhost:{cls.mock_server_port}"
        
        # Ensure HF_ENDPOINT matches the server we are about to start
        os.environ["HF_ENDPOINT"] = cls.mock_server_url
        
        # Check if port is already in use
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', cls.mock_server_port)) != 0:
                print(f"[*] Starting Mock HF Server for tests...")
                current_dir = os.path.dirname(os.path.abspath(__file__))
                mock_server_path = os.path.join(os.path.dirname(current_dir), 'fastapi_app', 'mock_hf.py')
                
                cls.mock_process = subprocess.Popen(
                    [sys.executable, mock_server_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env={**os.environ, "MOCK_HF_PORT": str(cls.mock_server_port)}
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

    @unittest.skipIf(not HAS_DATASETS, "datasets library not installed")
    def test_load_dataset_from_mock(self):
        # Load the mock dataset created in setup
        # repo_id is "my-dataset"
        print("[*] Loading dataset: my-dataset")
        dataset = load_dataset("my-dataset", split="train")
        
        self.assertIsNotNone(dataset)
        self.assertEqual(len(dataset), 2)
        self.assertEqual(dataset[0]["text"], "hello")
        self.assertEqual(dataset[1]["text"], "world")

    @unittest.skipIf(not HAS_DATASETS, "datasets library not installed")
    def test_load_instruct_10k_dataset_from_mock(self):
        print("[*] Loading dataset: OpenDCAI/dataflow-instruct-10k")
        dataset = load_dataset("OpenDCAI/dataflow-instruct-10k", split="train")
        self.assertIsNotNone(dataset)
        self.assertEqual(len(dataset), 10000)

    @unittest.skipIf(not HAS_DATASETS, "datasets library not installed")
    def test_load_knowledge_med_40k_dataset_from_mock(self):
        print("[*] Loading dataset: OpenDCAI/dataflow-knowledge-med-40k")
        dataset = load_dataset("OpenDCAI/dataflow-knowledge-med-40k", split="train")
        self.assertIsNotNone(dataset)
        self.assertEqual(len(dataset), 41318)

    def test_mock_server_api_metadata(self):
        response = requests.get(f"{self.mock_server_url}/api/datasets/my-dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "my-dataset")
        self.assertIn("sha", data)
        self.assertTrue(isinstance(data["sha"], str))
        self.assertTrue(len(data["sha"]) > 0)

    def test_mock_server_api_info(self):
        response = requests.get(f"{self.mock_server_url}/info?dataset=my-dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dataset_info", data)
        self.assertIn("default", data["dataset_info"])
        self.assertEqual(data["dataset_info"]["default"]["features"]["text"]["dtype"], "string")
