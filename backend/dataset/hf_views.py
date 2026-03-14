import os
import mimetypes
import json
import logging
from django.http import FileResponse, HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .services import hfds

logger = logging.getLogger('django')


# --- Hub APIs ---

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_list_datasets(request):
    search = request.GET.get('search', '').lower()
    limit = int(request.GET.get('limit', 100))
    results = []
    for ds in hfds.list():
        if search and search not in ds.get("name", "").lower() and search not in ds.get("pipeline", "").lower():
            continue
        results.append({
            "id": ds["id"],
            "name": ds["name"],
            "pipeline": ds["pipeline"],
            "author": "local",
            "tags": ["local"],
            "private": False,
            "downloads": 0,
            "likes": 0,
            "num_samples": ds.get("num_samples", 0),
            "file_size": ds.get("file_size", 0),
        })
    return JsonResponse(results[:limit], safe=False)


@api_view(['GET', 'HEAD', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def hf_dataset_metadata(request, repo_id):
    logger.info(f"Incoming {request.method} request for metadata: {repo_id}")

    if "/paths-info/" in repo_id:
        return _hf_paths_info(request, repo_id)
    if "/tree/" in repo_id:
        return _hf_tree(request, repo_id)
    if "/commits/" in repo_id:
        return _hf_commits(request, repo_id)
    if "/revision/" in repo_id:
        repo_id = repo_id.split("/revision/", 1)[0]

    metadata = hfds.get_metadata(repo_id)
    if not metadata:
        return JsonResponse({"error": f"Dataset {repo_id} not found"}, status=404)

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
    except Exception:
        paths = []
        if hasattr(request, 'data'):
            if hasattr(request.data, 'getlist'):
                paths = request.data.getlist("paths") or request.data.getlist("paths[]")
            else:
                paths = request.data.get("paths") or []
        elif hasattr(request, 'POST'):
            paths = request.POST.getlist("paths") or request.POST.getlist("paths[]")
    if isinstance(paths, str):
        paths = [paths]

    results = []
    for p in paths:
        file_path = hfds.resolve_file(repo_id, revision, p)
        if file_path:
            is_dir = os.path.isdir(file_path)
            results.append({
                "type": "directory" if is_dir else "file",
                "path": p,
                "size": 0 if is_dir else os.path.getsize(file_path),
                "oid": "mock-oid",
            })
    return JsonResponse(results, safe=False)


def _hf_tree(request, repo_id_with_suffix):
    repo_id, rev_and_sub = repo_id_with_suffix.split("/tree/", 1)
    if "/" in rev_and_sub:
        revision, subpath = rev_and_sub.split("/", 1)
    else:
        revision, subpath = rev_and_sub, ""

    dataset_dir = hfds.get_dataset_dir(repo_id)
    data_dir = os.path.join(dataset_dir, "resolve", revision)
    if not os.path.exists(data_dir):
        data_dir = os.path.join(dataset_dir, subpath) if subpath else dataset_dir
    else:
        data_dir = os.path.join(data_dir, subpath) if subpath else data_dir

    results = []
    if os.path.isdir(data_dir):
        for item in os.listdir(data_dir):
            if item == ".git": continue
            item_path = os.path.join(data_dir, item)
            is_dir = os.path.isdir(item_path)
            results.append({
                "type": "directory" if is_dir else "file",
                "path": os.path.join(subpath, item) if subpath else item,
                "size": 0 if is_dir else os.path.getsize(item_path),
                "oid": "mock-oid",
            })
    return JsonResponse(results, safe=False)


def _hf_commits(request, repo_id_with_suffix):
    repo_id, revision = repo_id_with_suffix.split("/commits/", 1)
    metadata = hfds.get_metadata(repo_id)
    if not metadata:
        return JsonResponse({"error": "Dataset not found"}, status=404)
    commit_hash = metadata.get("sha", "mock-commit-hash-12345")
    return JsonResponse([{
        "id": commit_hash,
        "authors": [],
        "date": "2026-03-14T00:00:00.000Z",
        "title": "Mock commit",
        "message": "Mock commit message"
    }], safe=False)


@api_view(['GET', 'HEAD', 'DELETE'])
@permission_classes([AllowAny])
def hf_resolve_file(request, repo_id, revision, path):
    if request.method == "DELETE":
        return HttpResponse(status=501)
    file_path = hfds.resolve_file(repo_id, revision, path)
    if not file_path:
        return HttpResponse("File not found", status=404)
    if request.method == "HEAD":
        return HttpResponse(status=200)
    content_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')


@api_view(['POST'])
@permission_classes([AllowAny])
def hf_create_repo(request):
    repo_id = request.data.get("name")
    if not repo_id:
        return JsonResponse({"error": "Missing repo name"}, status=400)
    hfds.create_repo(repo_id)
    return JsonResponse({"url": f"/api/datasets/{repo_id}"}, status=201)


@api_view(['DELETE', 'GET', 'HEAD', 'POST'])
@permission_classes([AllowAny])
def hf_delete_repo(request, repo_id):
    if request.method == "DELETE":
        if hfds.delete_repo(repo_id):
            return HttpResponse(status=204)
        return JsonResponse({"error": "Repo not found"}, status=404)
    metadata = hfds.get_metadata(repo_id)
    if not metadata:
        return JsonResponse({"error": f"Dataset {repo_id} not found"}, status=404)
    return JsonResponse(metadata)


@api_view(['POST'])
@permission_classes([AllowAny])
def hf_upload_file(request, repo_id, revision, path):
    if not os.path.exists(hfds.get_dataset_dir(repo_id)):
        return JsonResponse({"error": "Repo not found"}, status=404)
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)
    content = b"".join(uploaded_file.chunks())
    hfds.upload_file(repo_id, revision, path, content)
    return JsonResponse({"commit": {"oid": "new-hash"}, "url": f"/datasets/{repo_id}/resolve/{revision}/{path}"})


# --- Viewer APIs ---

@api_view(['GET'])
@permission_classes([AllowAny])
def hf_is_valid(request):
    dataset = request.GET.get('dataset')
    if not dataset or not hfds.get_metadata(dataset):
        return JsonResponse({"error": "Dataset not found"}, status=404)
    return JsonResponse({"preview": True, "viewer": True, "search": False, "filter": False, "statistics": False})


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_splits(request):
    dataset = request.GET.get('dataset')
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
    splits = hfds.get_splits(dataset)
    if not splits:
        return JsonResponse({"error": "Dataset not found"}, status=404)
    return JsonResponse(splits)


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_info(request):
    dataset = request.GET.get('dataset')
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)
    metadata = hfds.get_metadata(dataset)
    if not metadata:
        return JsonResponse({"error": "Dataset not found"}, status=404)
    features = hfds.infer_features(dataset)
    splits = hfds.get_splits(dataset) or {"splits": []}
    return JsonResponse({
        "dataset_info": {
            "description": f"Local dataset {dataset}",
            "features": features,
            "builder_name": "generator",
            "config_name": "default",
            "version": {"version_str": "0.0.0"},
            "splits": {s["split"]: {"num_examples": 0} for s in splits["splits"]},
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_rows(request):
    dataset = request.GET.get('dataset')
    offset = int(request.GET.get('offset', 0))
    length = int(request.GET.get('length', 100))
    if not dataset:
        return JsonResponse({"error": "Missing dataset parameter"}, status=400)

    result = hfds.get_rows(dataset, offset=offset, length=length)
    features = hfds.infer_features(dataset)
    formatted_features = [{"feature_idx": i, "name": k, "type": v} for i, (k, v) in enumerate(features.items())]
    return JsonResponse({
        "features": formatted_features,
        "rows": result["rows"],
        "num_rows_total": result["num_rows_total"],
        "num_rows_per_page": length,
        "partial": False,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_parquet_list(request):
    return JsonResponse({"error": "Parquet export not supported"}, status=404)
