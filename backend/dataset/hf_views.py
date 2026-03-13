import os
import mimetypes
import json
import logging
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from .services import dataset_server

logger = logging.getLogger('django')

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_list_datasets(request):
    """HF compatible list datasets API"""
    search = request.GET.get('search', '')
    limit = int(request.GET.get('limit', 100))
    datasets = dataset_server.list_datasets(search=search, limit=limit)
    return JsonResponse(datasets, safe=False)

@api_view(['GET', 'HEAD', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def hf_dataset_metadata(request, repo_id):
    """HF compatible dataset metadata API"""
    logger.info(f"Incoming {request.method} request for metadata: {repo_id}")
    
    # Git Tree / Paths Info / Revision handling
    if "/paths-info/" in repo_id:
        return _hf_paths_info(request, repo_id)
    if "/tree/" in repo_id:
        return _hf_tree(request, repo_id)
    if "/revision/" in repo_id:
        repo_id = repo_id.split("/revision/", 1)[0]

    metadata = dataset_server.get_metadata(repo_id)
    if not metadata:
        logger.info(f"Metadata NOT FOUND for {repo_id}")
        return JsonResponse({"error": f"Dataset {repo_id} not found"}, status=404)
        
    logger.info(f"Metadata found for {repo_id}: {metadata}")
    if request.method == "HEAD":
        return HttpResponse(status=200)
    
    if request.method == "DELETE":
        return hf_delete_repo(request._request, repo_id)

    return JsonResponse(metadata)

def _hf_paths_info(request, repo_id_with_suffix):
    repo_id, revision = repo_id_with_suffix.split("/paths-info/", 1)
    
    try:
        body = json.loads(request.body)
        paths = body.get("paths", [])
    except:
        if hasattr(request, 'data'):
            # It could be a dict or a QueryDict
            paths_data = request.data.get("paths") or request.data.get("paths[]") or []
            if hasattr(request.data, "getlist"):
                paths = request.data.getlist("paths")
                if not paths:
                    paths = request.data.getlist("paths[]")
            else:
                paths = paths_data
        elif hasattr(request, 'POST'):
            paths = request.POST.getlist("paths")
            if not paths and "paths[]" in request.POST:
                paths = request.POST.getlist("paths[]")
        else:
            paths = []
            
    if isinstance(paths, str):
        paths = [paths]
            
    logger.info(f"Paths-info received paths: {paths}")
        
    results = []
    for p in paths:
        file_path = dataset_server.resolve_file(repo_id, revision, p)
        if file_path:
            is_dir = os.path.isdir(file_path)
            results.append({
                "type": "directory" if is_dir else "file",
                "path": p,
                "size": 0 if is_dir else os.path.getsize(file_path),
                "oid": "mock-oid"
            })
    logger.info(f"Paths-info for {repo_id}: {results}")
    return JsonResponse(results, safe=False)

def _hf_tree(request, repo_id_with_suffix):
    repo_id, revision = repo_id_with_suffix.split("/tree/", 1)
    if "/" in revision:
        revision, subpath = revision.split("/", 1)
    else:
        subpath = ""
        
    dataset_path = dataset_server._get_dataset_path(repo_id)
    data_dir = os.path.join(dataset_path, "resolve", revision)
    if not os.path.exists(data_dir):
        data_dir = os.path.join(dataset_path, subpath) if subpath else dataset_path
    else:
        data_dir = os.path.join(data_dir, subpath) if subpath else data_dir
        
    results = []
    if os.path.exists(data_dir) and os.path.isdir(data_dir):
        for item in os.listdir(data_dir):
            if item == ".git": continue
            item_path = os.path.join(data_dir, item)
            is_dir = os.path.isdir(item_path)
            results.append({
                "type": "directory" if is_dir else "file",
                "path": os.path.join(subpath, item) if subpath else item,
                "size": 0 if is_dir else os.path.getsize(item_path),
                "oid": "mock-oid"
            })
            
    # Also add python file at the root of the dataset if subpath is empty
    if not subpath:
        repo_name = os.path.basename(repo_id)
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
    
    logger.info(f"Tree for {repo_id} ({revision}): {results}")
    return JsonResponse(results, safe=False)

@api_view(['GET', 'HEAD', 'DELETE'])
@permission_classes([AllowAny])
def hf_resolve_file(request, repo_id, revision, path):
    """HF compatible resolve file API"""
    if request.method == "DELETE":
        return HttpResponse(status=501)

    file_path = dataset_server.resolve_file(repo_id, revision, path)
    logger.info(f"Resolve file {repo_id}@{revision}/{path} -> {file_path}")
    if not file_path:
        return HttpResponse("File not found", status=404)
            
    if request.method == "HEAD":
        return HttpResponse(status=200)
        
    content_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')

# --- Write APIs ---

@api_view(['POST'])
@permission_classes([AllowAny])
def hf_create_repo(request):
    repo_id = request.data.get("name")
    if not repo_id:
        return JsonResponse({"error": "Missing repo name"}, status=400)
    
    dataset_server.create_repo(repo_id)
    return JsonResponse({"url": f"/api/datasets/{repo_id}"}, status=201)

@api_view(['DELETE', 'GET', 'HEAD', 'POST'])
@permission_classes([AllowAny])
def hf_delete_repo(request, repo_id):
    if request.method == "DELETE":
        if dataset_server.delete_repo(repo_id):
            return HttpResponse(status=204)
        return JsonResponse({"error": "Repo not found"}, status=404)
    
    metadata = dataset_server.get_metadata(repo_id)
    if not metadata:
        return JsonResponse({"error": f"Dataset {repo_id} not found"}, status=404)
    return JsonResponse(metadata)

@api_view(['POST'])
@permission_classes([AllowAny])
def hf_upload_file(request, repo_id, revision, path):
    dataset_path = dataset_server._get_dataset_path(repo_id)
    if not os.path.exists(dataset_path):
        return JsonResponse({"error": "Repo not found"}, status=404)
    
    target_path = os.path.join(dataset_path, "resolve", revision, path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)
        
    with open(target_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
            
    return JsonResponse({"commit": {"oid": "new-hash"}, "url": f"/datasets/{repo_id}/resolve/{revision}/{path}"})

# --- Viewer APIs ---

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_is_valid(request):
    dataset = request.GET.get('dataset')
    if not dataset or not dataset_server.get_metadata(dataset):
        return JsonResponse({"error": "Dataset not found"}, status=404)
    return JsonResponse({
        "preview": True,
        "viewer": True,
        "search": False,
        "filter": False,
        "statistics": False
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_splits(request):
    dataset = request.GET.get('dataset')
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
    splits = dataset_server.get_splits(dataset)
    if not splits:
        return JsonResponse({"error": "Dataset not found"}, status=404)
    return JsonResponse(splits)

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_info(request):
    dataset = request.GET.get('dataset')
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
    
    metadata = dataset_server.get_metadata(dataset)
    if not metadata:
        return JsonResponse({"error": "Dataset not found"}, status=404)
        
    features = dataset_server.infer_features(dataset)
    splits_info = dataset_server.get_splits(dataset)
    
    return JsonResponse({
        "dataset_info": {
            "description": f"Local dataset {dataset}",
            "features": features,
            "builder_name": "generator",
            "config_name": "default",
            "version": {"version_str": "0.0.0"},
            "splits": {s["split"]: {"num_examples": 0} for s in splits_info["splits"]}
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_rows(request):
    dataset = request.GET.get('dataset')
    split = request.GET.get('split', 'train')
    offset = int(request.GET.get('offset', 0))
    length = int(request.GET.get('length', 100))
    
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
        
    rows_data = dataset_server.get_rows(dataset, split=split, offset=offset, length=length)
    features = dataset_server.infer_features(dataset, split=split)
    
    formatted_features = []
    for i, (name, type_info) in enumerate(features.items()):
        formatted_features.append({
            "feature_idx": i,
            "name": name,
            "type": type_info
        })

    return JsonResponse({
        "features": formatted_features,
        "rows": rows_data["rows"],
        "num_rows_total": rows_data["num_rows_total"],
        "num_rows_per_page": length,
        "partial": False
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_parquet_list(request):
    return JsonResponse({"error": "Parquet export not supported"}, status=404)
