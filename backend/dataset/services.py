import os
import json
import hashlib
import tempfile
import mimetypes
import subprocess
import yaml
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.http import FileResponse

_DATA_EXTENSIONS = {'.jsonl', '.json', '.csv', '.parquet'}


class HFDatasetFileRegistry:
    """
    dcai-platform's unified HF-compatible dataset registry.

    Responsibilities:
    - Scans ``scan_dir`` on startup and indexes all flat data files
      (jsonl / json / parquet / csv) into a YAML registry.
    - Provides Hub read/write APIs (create_repo, delete_repo, upload_file,
      get_metadata, resolve_file).
    - Provides Viewer APIs (get_splits, get_rows, infer_features).

    Hub write operations use ``hub_root`` so uploaded repos are kept
    separate from the auto-scanned directory.

    Lookup keys accepted by ``get()``:
      - ds_id    — sha1 hash of the file path (stable)
      - pipeline — parent directory name
      - name     — file stem
    """

    def __init__(self, registry_path: str, scan_dir: str, hub_root: str):
        self.registry_path = os.path.abspath(registry_path)
        self.scan_dir = scan_dir
        self.hub_root = hub_root
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        os.makedirs(self.hub_root, exist_ok=True)
        self._rescan()

    # ------------------------------------------------------------------
    # YAML helpers
    # ------------------------------------------------------------------

    def _make_id(self, file_path: str) -> str:
        return hashlib.sha1(file_path.encode()).hexdigest()[:10]

    def _read(self) -> dict:
        if not os.path.exists(self.registry_path):
            return {"datasets": {}, "repos": {}}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        data.setdefault("datasets", {})
        data.setdefault("repos", {})
        return data

    def _write(self, data: dict):
        tmp_dir = os.path.dirname(self.registry_path)
        with tempfile.NamedTemporaryFile("w", dir=tmp_dir, delete=False,
                                         encoding="utf-8", suffix=".tmp") as tmp:
            yaml.safe_dump(data, tmp, allow_unicode=True, sort_keys=False)
            tmp_path = tmp.name
        os.replace(tmp_path, self.registry_path)

    # ------------------------------------------------------------------
    # Flat-file scan
    # ------------------------------------------------------------------

    def _build_entry(self, file_path: str) -> dict:
        pipeline = os.path.basename(os.path.dirname(file_path))
        name = os.path.splitext(os.path.basename(file_path))[0]
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        return {
            "id": self._make_id(file_path),
            "name": name,
            "pipeline": pipeline,
            "root": file_path,
            "type": ext,
            "num_samples": self._count_rows(file_path),
            "file_size": self._safe_getsize(file_path),
        }

    def _safe_getsize(self, path: str) -> int:
        try:
            return os.path.getsize(path)
        except OSError:
            return 0

    def _count_rows(self, file_path: str) -> int:
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        try:
            if ext == 'parquet':
                import pyarrow.parquet as pq
                return pq.read_metadata(file_path).num_rows
            elif ext == 'jsonl':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return sum(1 for line in f if line.strip())
            elif ext == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return len(data) if isinstance(data, list) else 1
            elif ext == 'csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return max(0, sum(1 for _ in f) - 1)
        except Exception:
            pass
        return 0

    def _rescan(self):
        """Rebuild flat-file dataset entries from scan_dir."""
        data = self._read()
        datasets = {}
        if os.path.isdir(self.scan_dir):
            for root, dirs, files in os.walk(self.scan_dir):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for fname in files:
                    if os.path.splitext(fname)[1].lower() not in _DATA_EXTENSIONS:
                        continue
                    file_path = os.path.join(root, fname)
                    entry = self._build_entry(file_path)
                    datasets[entry["id"]] = entry
        data["datasets"] = datasets
        self._write(data)

    # ------------------------------------------------------------------
    # Flat-file dataset API
    # ------------------------------------------------------------------

    def list(self) -> List[dict]:
        return list(self._read()["datasets"].values())

    def get(self, key: str) -> Optional[dict]:
        """Look up by ds_id, pipeline name, or file stem (case-insensitive)."""
        datasets = self._read()["datasets"]
        if key in datasets:
            return datasets[key]
        key_lower = key.lower()
        for ds in datasets.values():
            if ds.get("pipeline", "").lower() == key_lower:
                return ds
            if ds.get("name", "").lower() == key_lower:
                return ds
        return None

    def get_rows(self, key: str, offset: int = 0, length: int = 100) -> Dict[str, Any]:
        ds = self.get(key)
        if not ds:
            # Fall back to hub repo: find the first data file under hub_root/key/
            ds = self._hub_repo_as_entry(key)
        if not ds:
            return {"rows": [], "num_rows_total": 0}
        file_path = ds["root"]
        ext = ds.get("type", "")
        chunk_data = []
        num_rows_total = ds.get("num_samples", 0)
        try:
            if ext == "jsonl":
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [l for l in f if l.strip()]
                num_rows_total = len(lines)
                chunk_data = [json.loads(l) for l in lines[offset:offset + length]]
            elif ext == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    num_rows_total = len(data)
                    chunk_data = data[offset:offset + length]
                else:
                    num_rows_total = 1
                    chunk_data = [data] if offset == 0 else []
            elif ext == "parquet":
                import pandas as pd
                df = pd.read_parquet(file_path)
                num_rows_total = len(df)
                chunk_data = df.iloc[offset:offset + length].to_dict(orient="records")
            elif ext == "csv":
                import pandas as pd
                df = pd.read_csv(file_path)
                num_rows_total = len(df)
                chunk_data = df.iloc[offset:offset + length].to_dict(orient="records")
        except Exception:
            pass
        rows = [{"row_idx": offset + i, "row": r, "truncated_cells": []} for i, r in enumerate(chunk_data)]
        return {"rows": rows, "num_rows_total": num_rows_total}

    def _hub_repo_as_entry(self, repo_id: str) -> Optional[dict]:
        """Return a synthetic entry for the first data file found in a hub repo."""
        repo_path = self._repo_path(repo_id)
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                if ext in _DATA_EXTENSIONS:
                    file_path = os.path.join(root, fname)
                    return {
                        "id": self._make_id(file_path),
                        "name": os.path.splitext(fname)[0],
                        "pipeline": repo_id,
                        "root": file_path,
                        "type": ext.lstrip('.'),
                        "num_samples": self._count_rows(file_path),
                        "file_size": self._safe_getsize(file_path),
                    }
        return None

    def infer_features(self, key: str) -> Dict[str, Any]:
        result = self.get_rows(key, offset=0, length=5)
        features = {}
        rows = result.get("rows", [])
        if rows:
            for k, v in rows[0]["row"].items():
                if isinstance(v, bool): dtype = "bool"
                elif isinstance(v, int): dtype = "int64"
                elif isinstance(v, float): dtype = "float64"
                else: dtype = "string"
                features[k] = {"dtype": dtype, "_type": "Value"}
        return features

    def get_splits(self, key: str) -> Optional[Dict[str, Any]]:
        ds = self.get(key)
        if not ds:
            # Check hub repo
            if not os.path.exists(self._repo_path(key)):
                return None
        return {
            "splits": [{"dataset": key, "config": "default", "split": "default"}],
            "pending": [],
            "failed": [],
        }

    # ------------------------------------------------------------------
    # Hub repo API (folder-based, stored under hub_root)
    # ------------------------------------------------------------------

    def _repo_path(self, repo_id: str) -> str:
        return os.path.join(self.hub_root, repo_id)

    def _get_commit_hash(self, path: str) -> str:
        try:
            if os.path.exists(os.path.join(path, ".git")):
                result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=path, capture_output=True, text=True, check=True,
                )
                return result.stdout.strip()
        except Exception:
            pass
        return "mock-commit-hash-12345"

    def get_metadata(self, repo_id: str) -> Optional[Dict[str, Any]]:
        # Try flat-file registry first
        ds = self.get(repo_id)
        if ds:
            return {
                "id": ds["id"],
                "sha": self._make_id(ds["root"]),
                "lastModified": "2026-03-14T00:00:00.000Z",
                "siblings": [{"rfilename": os.path.basename(ds["root"])}],
                "private": False,
                "config": "default",
            }
        # Fall back to hub repo directory
        repo_path = self._repo_path(repo_id)
        if not os.path.exists(repo_path):
            return None
        data_dir = os.path.join(repo_path, "resolve", "main")
        if not os.path.exists(data_dir):
            data_dir = repo_path
        siblings = []
        for root, _, files in os.walk(data_dir):
            for name in files:
                if name.startswith("."): continue
                rel = os.path.relpath(os.path.join(root, name), data_dir)
                siblings.append({"rfilename": rel})
        return {
            "id": repo_id,
            "sha": self._get_commit_hash(repo_path),
            "lastModified": "2026-03-14T00:00:00.000Z",
            "siblings": siblings,
            "private": False,
            "config": "default",
        }

    def resolve_file(self, repo_id: str, revision: str, path: str) -> Optional[str]:
        # The HF library sometimes sends path = "resolve/main/filename" when it
        # fetches via a commit hash revision.  Strip that redundant prefix.
        import re as _re
        path = _re.sub(r'^resolve/[^/]+/', '', path)

        # Try flat-file dataset first
        ds = self.get(repo_id)
        if ds and os.path.basename(ds["root"]) == path:
            return ds["root"]
        # Hub repo: always try 'main' as canonical fallback alongside the given revision
        repo_path = self._repo_path(repo_id)
        candidates = [
            os.path.join(repo_path, "resolve", revision, path),
            os.path.join(repo_path, "resolve", "main", path),
            os.path.join(repo_path, path),
        ]
        for p in candidates:
            if os.path.isfile(p):
                return p
        return None

    def create_repo(self, repo_id: str) -> bool:
        os.makedirs(self._repo_path(repo_id), exist_ok=True)
        return True

    def delete_repo(self, repo_id: str) -> bool:
        repo_path = self._repo_path(repo_id)
        if not os.path.exists(repo_path):
            return False
        import shutil
        shutil.rmtree(repo_path)
        return True

    def upload_file(self, repo_id: str, revision: str, path: str, content: bytes):
        """Save uploaded bytes and re-index if it's a data file."""
        target = os.path.join(self._repo_path(repo_id), "resolve", revision, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(content)
        if os.path.splitext(path)[1].lower() in _DATA_EXTENSIONS:
            data = self._read()
            entry = self._build_entry(target)
            data["datasets"][entry["id"]] = entry
            self._write(data)

    def get_dataset_dir(self, repo_id: str) -> str:
        """Return the hub repo directory for a given repo_id (for upload views)."""
        return self._repo_path(repo_id)


hfds = HFDatasetFileRegistry(
    registry_path=settings.DATASET_REGISTRY_PATH,
    scan_dir=settings.DATASET_SCAN_DIR,
    hub_root=os.path.join(settings.BASE_DIR, '..', 'data', 'hub_datasets'),
)
