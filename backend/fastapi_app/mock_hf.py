import os
import json
import subprocess
from typing import Any, Dict, List, Optional

def get_commit_hash(dataset_path: str) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], 
            cwd=dataset_path, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return "mock-commit-hash-12345"
from fastapi import FastAPI, APIRouter, HTTPException, Path, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Mock Hugging Face Hub", version="0.1.0")
router = APIRouter()

# --- Configuration ---
# Use absolute path for sample data to avoid issues when running from different directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_DIR = os.environ.get("MOCK_HF_DATA_DIR", os.path.join(BASE_DIR, "sample_data"))

# --- Hub APIs ---

@router.api_route("/api/datasets/{repo_id:path}", methods=["GET", "HEAD", "POST"])
async def handle_api_request(repo_id: str, request: Request):
    """
    Greedy handler for /api/datasets/{repo_id}
    Handles:
    - /api/datasets/{repo_id}
    - /api/datasets/{repo_id}/revision/{rev}
    - /api/datasets/{repo_id}/tree/{rev}
    - /api/datasets/{repo_id}/commits/{rev}
    - /api/datasets/{repo_id}/paths-info/{rev} (POST)
    """
    path = repo_id
    base_repo_id = path
    revision = "main"
    
    if "/tree/" in path:
        base_repo_id, revision = path.split("/tree/", 1)
        return await list_repo_tree(base_repo_id, revision, request)
    elif "/commits/" in path:
        base_repo_id, revision = path.split("/commits/", 1)
        return await list_repo_commits(base_repo_id, revision)
    elif "/paths-info/" in path:
        base_repo_id, revision = path.split("/paths-info/", 1)
        return await get_paths_info(base_repo_id, revision, request)
    elif "/revision/" in path:
        base_repo_id, revision = path.split("/revision/", 1)
        # Fallthrough to metadata
    
    dataset_path = os.path.join(SAMPLE_DATA_DIR, base_repo_id)
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail=f"Dataset not found: {base_repo_id}")
    
    # Check if files exist in resolve/main or root
    data_dir = os.path.join(dataset_path, "resolve", "main")
    if not os.path.exists(data_dir):
        data_dir = dataset_path
        
    siblings = []
    for root, _, files in os.walk(data_dir):
        for name in files:
            # Skip hidden files
            if name.startswith("."): continue
            rel_path = os.path.relpath(os.path.join(root, name), data_dir)
            siblings.append({"rfilename": rel_path})
            
    if not siblings:
        siblings = [{"rfilename": "train.jsonl"}]
    
    commit_hash = get_commit_hash(dataset_path)
    # Simple mock metadata
    return {
        "id": base_repo_id,
        "sha": commit_hash,
        "lastModified": "2024-03-10T00:00:00.000Z",
        "siblings": siblings,
        "private": False,
        "config": "default"
    }

async def list_repo_commits(repo_id: str, revision: str):
    """Mock GET /api/datasets/{repo_id}/commits/{revision}"""
    dataset_path = os.path.join(SAMPLE_DATA_DIR, repo_id)
    commit_hash = get_commit_hash(dataset_path)
    return [
        {
            "id": commit_hash,
            "authors": [],
            "date": "2024-03-10T00:00:00.000Z",
            "title": "Mock commit",
            "message": "Mock commit message"
        }
    ]

async def list_repo_tree(repo_id: str, revision: str, request: Request):
    """Internal handler for GET /api/datasets/{repo_id}/tree/{revision}"""
    dataset_path = os.path.join(SAMPLE_DATA_DIR, repo_id)
    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    recursive = request.query_params.get("recursive", "false").lower() == "true"
    
    results = []
    # Check resolve/main/ (or the revision)
    data_dir = os.path.join(dataset_path, "resolve", "main")
    if not os.path.exists(data_dir):
         data_dir = dataset_path # Fallback to root
         
    for root, dirs, files in os.walk(data_dir):
        if not recursive and root != data_dir:
            continue
            
        for name in files:
            rel_path = os.path.relpath(os.path.join(root, name), data_dir)
            if rel_path == ".": continue
            results.append({
                "type": "file",
                "path": rel_path,
                "size": os.path.getsize(os.path.join(root, name)),
                "oid": "mock-oid",
                "lfs": None
            })
        
        for name in dirs:
            rel_path = os.path.relpath(os.path.join(root, name), data_dir)
            if rel_path == ".": continue
            results.append({
                "type": "directory",
                "path": rel_path,
                "oid": "mock-oid"
            })
            
        if not recursive:
            break
            
    return results

async def get_paths_info(repo_id: str, revision: str, request: Request):
    """Mock POST /api/datasets/{repo_id}/paths-info/{revision}"""
    try:
        body = await request.form()
        paths = body.getlist("paths")
    except:
        try:
            body = await request.json()
            paths = body.get("paths", [])
        except:
            paths = []

    dataset_path = os.path.join(SAMPLE_DATA_DIR, repo_id)
    data_dir = os.path.join(dataset_path, "resolve", "main")
    if not os.path.exists(data_dir):
        data_dir = dataset_path

    results = []
    for path in paths:
        file_path = os.path.join(data_dir, path)
        if os.path.exists(file_path):
            is_dir = os.path.isdir(file_path)
            results.append({
                "type": "directory" if is_dir else "file",
                "path": path,
                "size": 0 if is_dir else os.path.getsize(file_path),
                "oid": "mock-oid"
            })
            
    return results

@router.api_route("/datasets/{repo_id:path}/resolve/{revision}/{path:path}", methods=["GET", "HEAD"])
async def resolve_file(repo_id: str, revision: str, path: str, request: Request):
    """Mock GET/HEAD /datasets/{repo_id}/resolve/{revision}/{path}"""
    # Map to local file: SAMPLE_DATA_DIR/{repo_id}/resolve/{revision}/{path}
    # In mock, we often use 'main' as the directory name instead of actual hashes
    dataset_path = os.path.join(SAMPLE_DATA_DIR, repo_id)
    commit_hash = get_commit_hash(dataset_path)
    
    effective_revision = revision
    if revision == commit_hash or revision == "mock-commit-hash-12345":
        effective_revision = "main"

    file_path = os.path.join(SAMPLE_DATA_DIR, repo_id, "resolve", effective_revision, path)
    
    if not os.path.exists(file_path):
        # Also try direct repo_id/path if resolve/revision is skipped in local layout
        alt_path = os.path.join(SAMPLE_DATA_DIR, repo_id, path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            # Try 'main' if revision was something else
            if effective_revision != "main":
                 alt_path = os.path.join(SAMPLE_DATA_DIR, repo_id, "resolve", "main", path)
                 if os.path.exists(alt_path):
                     file_path = alt_path
            
            if not os.path.exists(file_path):
                # For README.md, return 404 silently if it doesn't exist (datasets often checks it)
                if path == "README.md":
                    raise HTTPException(status_code=404, detail="README not found")
                raise HTTPException(status_code=404, detail=f"File not found: {path} (tried {file_path})")
            
    if request.method == "HEAD":
        return Response(status_code=200)
    return FileResponse(file_path)

# --- Dataset Viewer APIs ---
# These are typically on datasets-server.huggingface.co
# We support them on the same host for simplicity

@router.get("/parquet")
async def get_parquet_list(dataset: str):
    """Mock GET /parquet?dataset={dataset_name}"""
    return JSONResponse(
        content={
            "partial": False,
            "pending": False,
            "failed": False,
            "parquet_files": [
                {
                    "dataset": dataset,
                    "config": "default",
                    "split": "train",
                    "url": f"/datasets/{dataset}/resolve/main/train.jsonl",
                    "filename": "train.jsonl",
                    "size": 1024
                }
            ]
        },
        headers={"X-Revision": get_commit_hash(os.path.join(SAMPLE_DATA_DIR, dataset))}
    )

@router.get("/info")
async def get_dataset_info(dataset: str):
    """Mock GET /info?dataset={dataset_name}"""
    return JSONResponse(
        content={
            "partial": False,
            "pending": False,
            "failed": False,
            "dataset_info": {
                "default": {
                    "description": "Mock dataset description",
                    "features": {
                        "text": {"dtype": "string", "_type": "Value"},
                        "label": {"dtype": "int64", "_type": "Value"}
                    }
                }
            }
        },
        headers={"X-Revision": get_commit_hash(os.path.join(SAMPLE_DATA_DIR, dataset))}
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    # Default port 8002 as configured in settings.py
    port = int(os.environ.get("MOCK_HF_PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
