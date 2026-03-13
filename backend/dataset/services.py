import os
import json
import mimetypes
import subprocess
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.http import FileResponse

class LocalFSDatasetsServer:
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir, exist_ok=True)

    def _get_dataset_path(self, repo_id: str) -> str:
        return os.path.join(self.root_dir, repo_id)

    def get_commit_hash(self, dataset_path: str) -> str:
        try:
            if os.path.exists(os.path.join(dataset_path, ".git")):
                result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=dataset_path,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout.strip()
        except Exception:
            pass
        return "mock-commit-hash-12345"

    def is_repo_dir(self, path: str, name: str) -> bool:
        if os.path.exists(os.path.join(path, "resolve")):
            return True
        if os.path.exists(os.path.join(path, f"{name}.py")):
            return True
        # If it contains any common data file types
        data_extensions = {'.jsonl', '.json', '.csv', '.parquet', '.txt'}
        for _, _, files in os.walk(path):
            for f in files:
                if any(f.endswith(ext) for ext in data_extensions):
                    return True
            break # only check top level
        return False

    def list_datasets(self, search: str = "", limit: int = 100) -> List[Dict[str, Any]]:
        datasets = []
        if not os.path.exists(self.root_dir):
            return datasets

        for item in os.listdir(self.root_dir):
            item_path = os.path.join(self.root_dir, item)
            if not os.path.isdir(item_path) or item == ".git":
                continue

            if self.is_repo_dir(item_path, item):
                if not search or search in item:
                    datasets.append(self.format_dataset_entry(item, "local", item_path))
            else:
                # Treat as namespace
                namespace = item
                for sub_item in os.listdir(item_path):
                    sub_path = os.path.join(item_path, sub_item)
                    if os.path.isdir(sub_path) and sub_item != ".git":
                        repo_id = f"{namespace}/{sub_item}"
                        if not search or search in repo_id:
                            datasets.append(self.format_dataset_entry(sub_item, namespace, sub_path))
        
        return datasets[:limit]

    def format_dataset_entry(self, name: str, namespace: str, path: str) -> Dict[str, Any]:
        repo_id = f"{namespace}/{name}" if namespace != "local" else name
        
        # Calculate stats
        file_size = 0
        num_samples = 0
        for root, _, files in os.walk(path):
            for f in files:
                if f.startswith('.'): continue
                f_path = os.path.join(root, f)
                file_size += os.path.getsize(f_path)
        
        return {
            "id": repo_id,
            "author": namespace,
            "sha": self.get_commit_hash(path),
            "lastModified": "2026-03-13T00:00:00Z",
            "tags": ["local"],
            "private": False,
            "downloads": 0,
            "likes": 0,
            "num_samples": num_samples, # Still 0 unless we count rows for all
            "file_size": file_size,
        }

    def get_metadata(self, repo_id: str) -> Optional[Dict[str, Any]]:
        dataset_path = self._get_dataset_path(repo_id)
        if not os.path.exists(dataset_path):
            return None

        # Prefer files in resolve/main
        data_dir = os.path.join(dataset_path, "resolve", "main")
        if not os.path.exists(data_dir):
            data_dir = dataset_path

        siblings = []
        for root, _, files in os.walk(data_dir):
            for name in files:
                if name.startswith("."): continue
                rel_path = os.path.relpath(os.path.join(root, name), data_dir)
                siblings.append({"rfilename": rel_path})

        # Add .py file from root if missing
        repo_name = os.path.basename(repo_id)
        py_file = f"{repo_name}.py"
        if os.path.exists(os.path.join(dataset_path, py_file)):
            if not any(s["rfilename"] == py_file for s in siblings):
                siblings.append({"rfilename": py_file})

        return {
            "id": repo_id,
            "sha": self.get_commit_hash(dataset_path),
            "lastModified": "2026-03-13T00:00:00.000Z",
            "siblings": siblings,
            "private": False,
            "config": "default"
        }

    def resolve_file(self, repo_id: str, revision: str, path: str) -> Optional[str]:
        dataset_path = self._get_dataset_path(repo_id)
        commit_hash = self.get_commit_hash(dataset_path)
        
        effective_revision = revision
        if revision == commit_hash:
            effective_revision = "main"

        # Try multiple paths
        possible_paths = [
            os.path.join(dataset_path, "resolve", effective_revision, path),
            os.path.join(dataset_path, path),
        ]
        
        # Special case for .py script which might be at root but requested via resolve/main
        if path.endswith(".py"):
            repo_name = os.path.basename(repo_id)
            if path == f"{repo_name}.py":
                possible_paths.append(os.path.join(dataset_path, path))

        if effective_revision != "main":
            possible_paths.append(os.path.join(dataset_path, "resolve", "main", path))

        for file_path in possible_paths:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
        return None

    def create_repo(self, repo_id: str) -> bool:
        path = self._get_dataset_path(repo_id)
        os.makedirs(path, exist_ok=True)
        return True

    def delete_repo(self, repo_id: str) -> bool:
        path = self._get_dataset_path(repo_id)
        if not os.path.exists(path):
            return False
        import shutil
        shutil.rmtree(path)
        return True

    # --- Viewer Logic ---

    def get_splits(self, repo_id: str) -> Optional[Dict[str, Any]]:
        metadata = self.get_metadata(repo_id)
        if not metadata:
            return None
        
        # Simplified: scan siblings for likely split names
        splits = ["train"]
        for s in metadata.get("siblings", []):
            fname = s["rfilename"].lower()
            for sn in ["test", "validation", "dev"]:
                if sn in fname and sn not in splits:
                    splits.append(sn)
        
        return {
            "splits": [{"dataset": repo_id, "config": "default", "split": s} for s in splits],
            "pending": [],
            "failed": []
        }

    def infer_features(self, repo_id: str, split: str = "train") -> Dict[str, Any]:
        rows = self.get_rows(repo_id, split=split, length=5).get("rows", [])
        features = {}
        if rows:
            first_row = rows[0]["row"]
            for k, v in first_row.items():
                dtype = "string"
                if isinstance(v, int): dtype = "int64"
                elif isinstance(v, float): dtype = "float64"
                elif isinstance(v, bool): dtype = "bool"
                features[k] = {"dtype": dtype, "_type": "Value"}
        return features

    def get_rows(self, repo_id: str, split: str = "train", offset: int = 0, length: int = 100) -> Dict[str, Any]:
        dataset_path = self._get_dataset_path(repo_id)
        # Find a data file matching the split
        target_file = None
        data_dir = os.path.join(dataset_path, "resolve", "main")
        if not os.path.exists(data_dir): data_dir = dataset_path
        
        for f in os.listdir(data_dir):
            if split in f.lower() and any(f.endswith(ext) for ext in ['.jsonl', '.json', '.csv', '.parquet']):
                target_file = os.path.join(data_dir, f)
                break
        
        if not target_file and os.path.exists(os.path.join(data_dir, "train.jsonl")):
            target_file = os.path.join(data_dir, "train.jsonl")

        if not target_file:
            return {"rows": [], "features": [], "num_rows_total": 0}

        file_ext = os.path.splitext(target_file)[1].lower()
        chunk_data = []
        
        try:
            if file_ext == ".jsonl":
                with open(target_file, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if i >= offset + length: break
                        if i >= offset:
                            chunk_data.append(json.loads(line.strip()))
            elif file_ext == ".json":
                with open(target_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        chunk_data = data[offset:offset+length]
                    else:
                        chunk_data = [data] if offset == 0 else []
            elif file_ext == ".csv":
                import pandas as pd
                df = pd.read_csv(target_file, skiprows=range(1, offset+1), nrows=length)
                chunk_data = df.to_dict(orient="records")
            elif file_ext == ".parquet":
                import pandas as pd
                df = pd.read_parquet(target_file)
                chunk_data = df.iloc[offset:offset+length].to_dict(orient="records")
        except Exception:
            pass

        return {
            "rows": [{"row_idx": offset + i, "row": r, "truncated_cells": []} for i, r in enumerate(chunk_data)],
            "num_rows_total": offset + len(chunk_data) + 1, # Mock total
            "partial": False
        }

# Global instance
dataset_server = LocalFSDatasetsServer(os.path.join(settings.BASE_DIR, 'fastapi_app', 'sample_data'))
