import os
import unittest
import requests
import json
import io
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
        # Patch HF library constants to point to our test server
        endpoint = f"{cls.live_server_url}/api/hf"
        datasets.config.HF_ENDPOINT = endpoint
        import huggingface_hub.constants
        huggingface_hub.constants.ENDPOINT = endpoint

    def test_load_dataset_from_django(self):
        # Load the mock dataset: test-namespace/local-test-dataset
        # Need trust_remote_code=True for local dataset script
        dataset = load_dataset("test-namespace/local-test-dataset", split="train", streaming=True, trust_remote_code=True)
        self.assertIsNotNone(dataset)
        it = iter(dataset)
        item1 = next(it)
        self.assertEqual(item1["text"], "hello")

    def test_django_api_list(self):
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        ids = [d["id"] for d in data]
        self.assertIn("test-namespace/local-test-dataset", ids)
        # Check for real metadata fields
        for d in data:
            if d["id"] == "test-namespace/local-test-dataset":
                self.assertIn("file_size", d)
                self.assertGreater(d["file_size"], 0)

    def test_django_api_metadata(self):
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/test-namespace/local-test-dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "test-namespace/local-test-dataset")
        self.assertIn("siblings", data)
        filenames = [s["rfilename"] for s in data["siblings"]]
        self.assertIn("train.jsonl", filenames)

    # --- Write API Tests ---

    def test_create_and_delete_repo(self):
        repo_name = "test-namespace/temp-repo"
        # Create
        response = requests.post(f"{self.live_server_url}/api/hf/api/repos/create", json={"name": repo_name})
        self.assertEqual(response.status_code, 201)
        
        # Verify exists
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 200)
        
        # Delete
        response = requests.delete(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 204)
        
        # Verify gone
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 404)

    def test_upload_file(self):
        repo_name = "test-namespace/upload-test"
        requests.post(f"{self.live_server_url}/api/hf/api/repos/create", json={"name": repo_name})
        
        file_content = b'{"text": "uploaded content", "label": 1}'
        file_obj = io.BytesIO(file_content)
        
        upload_url = f"{self.live_server_url}/api/hf/api/datasets/{repo_name}/upload/main/data.jsonl"
        response = requests.post(upload_url, files={'file': ('data.jsonl', file_obj)})
        self.assertEqual(response.status_code, 200)
        
        # Resolve and check content
        resolve_url = f"{self.live_server_url}/api/hf/datasets/{repo_name}/resolve/main/data.jsonl"
        response = requests.get(resolve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, file_content)
        
        # Cleanup
        requests.delete(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")

    # --- Viewer API Tests ---

    def test_viewer_is_valid(self):
        url = f"{self.live_server_url}/api/hf/is-valid?dataset=test-namespace/local-test-dataset"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["viewer"])

    def test_viewer_splits(self):
        url = f"{self.live_server_url}/api/hf/splits?dataset=test-namespace/local-test-dataset"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        splits = response.json()["splits"]
        self.assertGreater(len(splits), 0)
        self.assertEqual(splits[0]["split"], "train")

    def test_viewer_rows(self):
        url = f"{self.live_server_url}/api/hf/rows?dataset=test-namespace/local-test-dataset&split=train&offset=0&length=1"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rows", data)
        self.assertEqual(len(data["rows"]), 1)
        self.assertEqual(data["rows"][0]["row"]["text"], "hello")
        self.assertIn("features", data)

    def test_viewer_info(self):
        url = f"{self.live_server_url}/api/hf/info?dataset=test-namespace/local-test-dataset"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        info = response.json()["dataset_info"]
        self.assertIn("features", info)
        self.assertEqual(info["features"]["text"]["dtype"], "string")
