import os
import io
import requests
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# HF_ENDPOINT will be set dynamically in setUpClass to point to the test server
import datasets
from datasets import load_dataset
from .services import hfds

_TEST_REPO = "test-namespace/local-test-dataset"
_TRAIN_JSONL = b'{"text": "hello", "label": 1}\n{"text": "world", "label": 0}\n'


class DatasetHFCompatibilityTest(StaticLiveServerTestCase):
    port = 8010

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        endpoint = f"{cls.live_server_url}/api/hf"
        datasets.config.HF_ENDPOINT = endpoint
        import huggingface_hub.constants
        huggingface_hub.constants.ENDPOINT = endpoint

        # Create test hub repo with a train.jsonl fixture
        hfds.create_repo(_TEST_REPO)
        hfds.upload_file(_TEST_REPO, "main", "train.jsonl", _TRAIN_JSONL)

    @classmethod
    def tearDownClass(cls):
        hfds.delete_repo(_TEST_REPO)
        # Also clean up upload-test repo if it leaked
        hfds.delete_repo("test-namespace/upload-test")
        super().tearDownClass()

    # --- Hub API Tests ---

    def test_django_api_list(self):
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Flat-file datasets use hash IDs; hub repos are found via get_metadata.
        # Verify the response is a non-empty list with the expected fields.
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        for d in data:
            self.assertIn("id", d)

    def test_django_api_metadata(self):
        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/{_TEST_REPO}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("siblings", data)
        filenames = [s["rfilename"] for s in data["siblings"]]
        self.assertIn("train.jsonl", filenames)

    def test_create_and_delete_repo(self):
        repo_name = "test-namespace/temp-repo"
        response = requests.post(f"{self.live_server_url}/api/hf/api/repos/create", json={"name": repo_name})
        self.assertEqual(response.status_code, 201)

        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 200)

        response = requests.delete(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 204)

        response = requests.get(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")
        self.assertEqual(response.status_code, 404)

    def test_upload_file(self):
        repo_name = "test-namespace/upload-test"
        requests.post(f"{self.live_server_url}/api/hf/api/repos/create", json={"name": repo_name})

        file_content = b'{"text": "uploaded content", "label": 1}'
        upload_url = f"{self.live_server_url}/api/hf/api/datasets/{repo_name}/upload/main/data.jsonl"
        response = requests.post(upload_url, files={'file': ('data.jsonl', io.BytesIO(file_content))})
        self.assertEqual(response.status_code, 200)

        resolve_url = f"{self.live_server_url}/api/hf/datasets/{repo_name}/resolve/main/data.jsonl"
        response = requests.get(resolve_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, file_content)

        requests.delete(f"{self.live_server_url}/api/hf/api/datasets/{repo_name}")

    # --- Viewer API Tests ---

    def test_viewer_is_valid(self):
        url = f"{self.live_server_url}/api/hf/is-valid?dataset={_TEST_REPO}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["viewer"])

    def test_viewer_splits(self):
        url = f"{self.live_server_url}/api/hf/splits?dataset={_TEST_REPO}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        splits = response.json()["splits"]
        self.assertGreater(len(splits), 0)
        split_names = [s["split"] for s in splits]
        self.assertIn("default", split_names)

    def test_viewer_rows(self):
        url = f"{self.live_server_url}/api/hf/rows?dataset={_TEST_REPO}&split=default&offset=0&length=1"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("rows", data)
        self.assertEqual(len(data["rows"]), 1)
        self.assertEqual(data["rows"][0]["row"]["text"], "hello")
        self.assertIn("features", data)

    def test_viewer_info(self):
        url = f"{self.live_server_url}/api/hf/info?dataset={_TEST_REPO}"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        info = response.json()["dataset_info"]
        self.assertIn("features", info)
        self.assertEqual(info["features"]["text"]["dtype"], "string")

    def test_load_dataset_from_django(self):
        dataset = load_dataset(_TEST_REPO, split="train", streaming=True, trust_remote_code=True)
        self.assertIsNotNone(dataset)
        it = iter(dataset)
        item1 = next(it)
        self.assertEqual(item1["text"], "hello")
