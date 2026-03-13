import os
import unittest
import requests
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

# We force the live server to use port 8010 so we can set HF_ENDPOINT globally
os.environ["HF_ENDPOINT"] = "http://localhost:8010/api/hf"

import datasets
from datasets import load_dataset

class DatasetHFCompatibilityTest(StaticLiveServerTestCase):
    port = 8010

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_load_dataset_from_django(self):
        # Load the mock dataset: test-namespace/local-test-dataset
        print(f"[*] Loading dataset: test-namespace/local-test-dataset from {self.live_server_url}")
        # Need trust_remote_code=True for local dataset script
        dataset = load_dataset("test-namespace/local-test-dataset", split="train", streaming=True, trust_remote_code=True)
        
        self.assertIsNotNone(dataset)
        # For streaming datasets, we iterate to get items
        it = iter(dataset)
        item1 = next(it)
        item2 = next(it)
        
        self.assertEqual(item1["text"], "hello")
        self.assertEqual(item2["text"], "world")

    def test_load_instruct_10k_dataset_from_django(self):
        print(f"[*] Loading dataset: OpenDCAI/dataflow-instruct-10k from {self.live_server_url}")
        # repo_id is "OpenDCAI/dataflow-instruct-10k"
        dataset = load_dataset("OpenDCAI/dataflow-instruct-10k", split="train", streaming=True, trust_remote_code=True)
        self.assertIsNotNone(dataset)
        # Check first item
        item = next(iter(dataset))
        self.assertIn("conversations", item)

    def test_load_knowledge_med_40k_dataset_from_django(self):
        print(f"[*] Loading dataset: OpenDCAI/dataflow-knowledge-med-40k from {self.live_server_url}")
        dataset = load_dataset("OpenDCAI/dataflow-knowledge-med-40k", split="train", streaming=True, trust_remote_code=True)
        self.assertIsNotNone(dataset)
        # Check first item
        item = next(iter(dataset))
        self.assertIn("answer", item)
        self.assertIn("question", item)

    def test_django_api_list(self):
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        ids = [d["id"] for d in data]
        self.assertIn("test-namespace/local-test-dataset", ids)

    def test_django_api_metadata(self):
        # We use re_path in core/urls.py for this
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/test-namespace/local-test-dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("METADATA response:", data)
        self.assertEqual(data["id"], "test-namespace/local-test-dataset")
        self.assertIn("sha", data)
        self.assertTrue(isinstance(data["sha"], str))
        self.assertTrue(len(data["sha"]) > 0)

    def test_django_api_info(self):
        response = requests.get(f"{self.live_server_url}/api/hf/info?dataset=test-namespace/local-test-dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dataset_info", data)
        self.assertIn("default", data["dataset_info"])
        self.assertEqual(data["dataset_info"]["default"]["features"]["text"]["dtype"], "string")
