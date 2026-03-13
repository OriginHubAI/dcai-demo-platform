import os
import mimetypes
import subprocess
import json
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings

# Path to local sample data
SAMPLE_DATA_ROOT = os.path.join(settings.BASE_DIR, 'fastapi_app', 'sample_data')

def get_commit_hash(dataset_path):
    try:
        # Check if it's a git repo
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

def is_repo_dir(path, name):
    """Check if a directory is a HF repo (contains resolve/ or name.py)"""
    if os.path.exists(os.path.join(path, "resolve")):
        return True
    if os.path.exists(os.path.join(path, f"{name}.py")):
        return True
    subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d != ".git"]
    if not subdirs:
        return True
    return False

def get_local_datasets():
    """List local datasets from sample_data directory"""
    datasets = []
    if not os.path.exists(SAMPLE_DATA_ROOT):
        return datasets
        
    for item in os.listdir(SAMPLE_DATA_ROOT):
        item_path = os.path.join(SAMPLE_DATA_ROOT, item)
        if not os.path.isdir(item_path) or item == ".git":
            continue
            
        if is_repo_dir(item_path, item):
            datasets.append(format_dataset_entry(item, "local", item_path))
        else:
            namespace = item
            for sub_item in os.listdir(item_path):
                sub_path = os.path.join(item_path, sub_item)
                if os.path.isdir(sub_path) and sub_item != ".git":
                    datasets.append(format_dataset_entry(sub_item, namespace, sub_path))
                    
    return datasets

def format_dataset_entry(name, namespace, path):
    repo_id = f"{namespace}/{name}" if namespace != "local" else name
    return {
        "id": repo_id,
        "author": namespace,
        "sha": get_commit_hash(path),
        "lastModified": "2026-03-13T00:00:00Z",
        "tags": ["local"],
        "private": False,
        "downloads": 0,
        "likes": 0,
    }

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_list_datasets(request):
    """HF compatible list datasets API"""
    local_datasets = get_local_datasets()
    return JsonResponse(local_datasets, safe=False)

@api_view(['GET', 'HEAD', 'POST'])
@permission_classes([AllowAny])
def hf_dataset_metadata(request, repo_id):
    """HF compatible dataset metadata API"""
    base_repo_id = repo_id
    revision = "main"
    
    if "/paths-info/" in repo_id:
        base_repo_id, revision = repo_id.split("/paths-info/", 1)
        dataset_path = os.path.join(SAMPLE_DATA_ROOT, base_repo_id)
        
        try:
            body = json.loads(request.body)
            paths = body.get("paths", [])
        except:
            paths = request.POST.getlist("paths") if request.POST else []
            
        data_dir = os.path.join(dataset_path, "resolve", "main")
        if not os.path.exists(data_dir):
            data_dir = dataset_path

        results = []
        for p in paths:
            file_path = os.path.join(data_dir, p)
            if not os.path.exists(file_path):
                alt_path = os.path.join(dataset_path, p)
                if os.path.exists(alt_path):
                    file_path = alt_path
            
            if os.path.exists(file_path):
                is_dir = os.path.isdir(file_path)
                results.append({
                    "type": "directory" if is_dir else "file",
                    "path": p,
                    "size": 0 if is_dir else os.path.getsize(file_path),
                    "oid": "mock-oid"
                })
        return JsonResponse(results, safe=False)

    if "/tree/" in repo_id:
        base_repo_id, revision = repo_id.split("/tree/", 1)
        # handle optional subpaths like /tree/main/data
        if "/" in revision:
            revision, subpath = revision.split("/", 1)
        else:
            subpath = ""
            
        dataset_path = os.path.join(SAMPLE_DATA_ROOT, base_repo_id)
        data_dir = os.path.join(dataset_path, "resolve", "main")
        if not os.path.exists(data_dir):
            data_dir = dataset_path
            
        if subpath:
            data_dir = os.path.join(data_dir, subpath)
            
        results = []
        if os.path.exists(data_dir):
            for root, dirs, files in os.walk(data_dir):
                for name in dirs:
                    if name == ".git": continue
                    rel_path = os.path.relpath(os.path.join(root, name), data_dir)
                    results.append({
                        "type": "directory",
                        "path": os.path.join(subpath, rel_path) if subpath else rel_path,
                        "oid": "mock-oid"
                    })
                for name in files:
                    rel_path = os.path.relpath(os.path.join(root, name), data_dir)
                    results.append({
                        "type": "file",
                        "path": os.path.join(subpath, rel_path) if subpath else rel_path,
                        "size": os.path.getsize(os.path.join(root, name)),
                        "oid": "mock-oid"
                    })
                break
                
        # Also add python file at the root of the dataset if subpath is empty
        if not subpath:
            repo_name = os.path.basename(base_repo_id)
            py_file = f"{repo_name}.py"
            py_path = os.path.join(dataset_path, py_file)
            if os.path.exists(py_path):
                if not any(r["path"] == py_file for r in results):
                    results.append({
                        "type": "file",
                        "path": py_file,
                        "size": os.path.getsize(py_path),
                        "oid": "mock-oid"
                    })
                    
        return JsonResponse(results, safe=False)
    
    # Handle /revision/ in path
    if "/revision/" in repo_id:
        base_repo_id, revision = repo_id.split("/revision/", 1)
        
    dataset_path = os.path.join(SAMPLE_DATA_ROOT, base_repo_id)
    if not os.path.exists(dataset_path):
        return JsonResponse({"error": "Dataset not found"}, status=404)
        
    if request.method == "HEAD":
        return HttpResponse(status=200)

    # Check if files exist in resolve/main or root
    data_dir = os.path.join(dataset_path, "resolve", "main")
    if not os.path.exists(data_dir):
        data_dir = dataset_path
        
    siblings = []
    for root, _, files in os.walk(data_dir):
        for name in files:
            if name.startswith("."): continue
            rel_path = os.path.relpath(os.path.join(root, name), data_dir)
            siblings.append({"rfilename": rel_path})
            
    if not siblings:
        siblings = [{"rfilename": "train.jsonl"}]
    
    # Add the .py file if it exists at repo root
    repo_name = os.path.basename(base_repo_id)
    py_file = f"{repo_name}.py"
    if os.path.exists(os.path.join(dataset_path, py_file)):
        if not any(s["rfilename"] == py_file for s in siblings):
            siblings.append({"rfilename": py_file})
    
    commit_hash = get_commit_hash(dataset_path)
    return JsonResponse({
        "id": base_repo_id,
        "sha": commit_hash,
        "lastModified": "2026-03-13T00:00:00.000Z",
        "siblings": siblings,
        "private": False,
        "config": "default"
    })

@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
def hf_resolve_file(request, repo_id, revision, path):
    """HF compatible resolve file API (download/stream)"""
    dataset_path = os.path.join(SAMPLE_DATA_ROOT, repo_id)
    commit_hash = get_commit_hash(dataset_path)
    
    effective_revision = revision
    if revision == commit_hash:
        effective_revision = "main"

    file_path = os.path.join(SAMPLE_DATA_ROOT, repo_id, "resolve", effective_revision, path)
    
    if not os.path.exists(file_path):
        alt_path = os.path.join(SAMPLE_DATA_ROOT, repo_id, path)
        if os.path.exists(alt_path):
            file_path = alt_path
        else:
            if effective_revision != "main":
                 alt_path = os.path.join(SAMPLE_DATA_ROOT, repo_id, "resolve", "main", path)
                 if os.path.exists(alt_path):
                     file_path = alt_path
            
            if not os.path.exists(file_path) or os.path.isdir(file_path):
                return HttpResponse("File not found", status=404)
            
    if request.method == "HEAD":
        return HttpResponse(status=200)
        
    content_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_parquet_list(request):
    """Mock GET /parquet?dataset={dataset_name}"""
    return JsonResponse({"error": "Not found"}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_info(request):
    """Mock GET /info?dataset={dataset_name}"""
    dataset = request.GET.get('dataset')
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
        
    dataset_path = os.path.join(SAMPLE_DATA_ROOT, dataset)
    
    # Check if a specific info.json exists in the dataset path
    info_path = os.path.join(dataset_path, "info.json")
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            info_data = json.load(f)
    else:
        info_data = {
            "default": {
                "description": "Mock dataset description",
                "features": {
                    "text": {"dtype": "string", "_type": "Value"},
                    "label": {"dtype": "int64", "_type": "Value"}
                }
            }
        }
        
    return JsonResponse(
        data={
            "partial": False,
            "pending": False,
            "failed": False,
            "dataset_info": info_data
        }
    )
