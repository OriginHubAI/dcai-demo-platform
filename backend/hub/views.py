import csv
import io
import json

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import DatasetRepo, DatasetVersion, DatasetFile, ModelRepo, ModelVersion, ModelFile


def _int_param(value, default):
    try:
        return max(1, int(value))
    except (TypeError, ValueError):
        return default


def _dataset_summary(repo: DatasetRepo):
    latest = repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()
    return {
        'id': repo.repo_id,
        'author': repo.author,
        'name': repo.name,
        'task': repo.task,
        'domain': repo.domain,
        'downloads': repo.downloads,
        'likes': repo.likes,
        'lastModified': repo.updated_at.date().isoformat(),
        'rows': repo.row_count,
        'size': repo.size_label,
        'modality': repo.modality,
        'language': repo.language,
        'license': repo.license,
        'description': repo.description,
        'summary': repo.summary,
        'datasetType': repo.dataset_type,
        'readonly': repo.readonly,
        'parentDataset': repo.parent_repo_id or None,
        'derivedDatasets': repo.derived_repo_ids,
        'tags': repo.tags,
        'metadata': repo.metadata,
        'visibility': repo.visibility,
        'hfCompatible': repo.hf_compatible,
        'latestRevision': latest.revision if latest else '',
        'fileCount': latest.files.count() if latest else 0,
    }


def _dataset_file_payload(file_obj: DatasetFile):
    return {
        'path': file_obj.path,
        'fileType': file_obj.file_type,
        'sizeBytes': file_obj.size_bytes,
        'size': file_obj.size_label,
        'split': file_obj.split,
        'rows': file_obj.row_count,
        'sha256': file_obj.sha256,
        'previewRows': file_obj.preview_rows,
        'previewText': file_obj.preview_text,
    }


def _dataset_version_payload(version: DatasetVersion):
    return {
        'revision': version.revision,
        'commitSha': version.commit_sha,
        'rows': version.row_count,
        'size': version.size_label,
        'createdAt': version.created_at.isoformat(),
        'manifest': version.manifest,
        'isLatest': version.is_latest,
    }


def _get_dataset_repo(repo_id):
    return DatasetRepo.objects.filter(repo_id=repo_id).first()


def _get_dataset_version(repo, revision=''):
    if not repo:
        return None
    if revision:
        version = repo.versions.filter(revision=revision).first()
        if version:
            return version
    return repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()


def _normalize_dataset_path(path):
    return (path or '').strip('/').strip()


def _infer_feature_type(value):
    if isinstance(value, bool):
        return {'dtype': 'bool', '_type': 'Value'}
    if isinstance(value, int):
        return {'dtype': 'int64', '_type': 'Value'}
    if isinstance(value, float):
        return {'dtype': 'float64', '_type': 'Value'}
    if isinstance(value, list):
        inner = value[0] if value else ''
        return {'feature': _infer_feature_type(inner), '_type': 'List'}
    if isinstance(value, dict):
        return {
            'feature': {key: _infer_feature_type(item) for key, item in value.items()},
            '_type': 'Struct',
        }
    return {'dtype': 'string', '_type': 'Value'}


def _dataset_features(version):
    first_row = None
    for file_obj in version.files.all():
        rows = file_obj.preview_rows or []
        if rows:
            first_row = rows[0]
            break
    if not isinstance(first_row, dict):
        return {}
    return {key: _infer_feature_type(value) for key, value in first_row.items()}


def _dataset_split_items(version):
    splits = {}
    for file_obj in version.files.all():
        split_name = file_obj.split or ''
        if not split_name and not file_obj.row_count:
            continue
        split_name = split_name or 'default'
        payload = splits.setdefault(split_name, {
            'dataset': version.repo.repo_id,
            'config': 'default',
            'split': split_name,
            'num_rows': 0,
            'num_bytes': 0,
        })
        payload['num_rows'] += int(file_obj.row_count or 0)
        payload['num_bytes'] += int(file_obj.size_bytes or 0)
    return list(splits.values())


def _dataset_info_payload(repo, version):
    splits = _dataset_split_items(version)
    return {
        'dataset': repo.repo_id,
        'default_config': 'default',
        'dataset_info': {
            'description': repo.description,
            'citation': '',
            'homepage': '',
            'license': repo.license,
            'features': _dataset_features(version),
            'splits': {
                item['split']: {
                    'name': item['split'],
                    'num_bytes': item['num_bytes'],
                    'num_examples': item['num_rows'],
                }
                for item in splits
            },
            'download_size': sum(item['num_bytes'] for item in splits),
            'dataset_size': sum(item['num_bytes'] for item in splits),
        },
    }


def _dataset_file_preview_rows(file_obj, offset=0, length=100):
    rows = file_obj.preview_rows or []
    start = max(0, int(offset or 0))
    end = start + max(1, int(length or 100))
    return rows[start:end]


def _dataset_rows_payload(version, split='', path='', offset=0, length=100):
    file_obj = None
    normalized_path = _normalize_dataset_path(path)
    if normalized_path:
        file_obj = version.files.filter(path=normalized_path).first()
    elif split:
        file_obj = version.files.filter(split=split).order_by('sort_order', 'path').first()
    if not file_obj:
        file_obj = version.files.order_by('sort_order', 'path').first()
    if not file_obj:
        return {'rows': [], 'features': {}, 'num_rows_total': 0, 'file': None}

    preview_rows = _dataset_file_preview_rows(file_obj, offset=offset, length=length)
    return {
        'rows': [
            {'row_idx': int(offset or 0) + index, 'row': row, 'truncated_cells': []}
            for index, row in enumerate(preview_rows)
        ],
        'features': _dataset_features(version),
        'num_rows_total': int(file_obj.row_count or len(file_obj.preview_rows or [])),
        'file': _dataset_file_payload(file_obj),
    }


def _list_tree_children(version, current_path=''):
    current_path = _normalize_dataset_path(current_path)
    directories = {}
    files = []

    for file_obj in version.files.all():
        full_path = _normalize_dataset_path(file_obj.path)
        if current_path:
            prefix = f'{current_path}/'
            if not full_path.startswith(prefix):
                continue
            remainder = full_path[len(prefix):]
        else:
            remainder = full_path

        if not remainder:
            continue

        if '/' in remainder:
            segment = remainder.split('/', 1)[0]
            directory_path = f'{current_path}/{segment}' if current_path else segment
            if directory_path not in directories:
                directories[directory_path] = {
                    'type': 'directory',
                    'path': directory_path,
                    'name': segment,
                    'sizeBytes': 0,
                    'size': '0B',
                    'rowCount': 0,
                }
            directories[directory_path]['sizeBytes'] += int(file_obj.size_bytes or 0)
            directories[directory_path]['rowCount'] += int(file_obj.row_count or 0)
        else:
            payload = _dataset_file_payload(file_obj)
            payload.update({
                'type': 'file',
                'name': remainder,
                'rowCount': int(file_obj.row_count or 0),
            })
            files.append(payload)

    directory_items = []
    for item in directories.values():
        item['size'] = f"{item['sizeBytes']}B" if item['sizeBytes'] else '0B'
        directory_items.append(item)

    return sorted(directory_items, key=lambda item: item['name']) + sorted(files, key=lambda item: item['name'])


def _dataset_file_response(file_obj: DatasetFile):
    file_type = (file_obj.file_type or '').lower()
    content_type = 'text/plain; charset=utf-8'

    if file_obj.preview_text:
        body = file_obj.preview_text
    elif file_obj.preview_rows:
        if file_type == 'csv':
            fieldnames = list(file_obj.preview_rows[0].keys()) if file_obj.preview_rows else []
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(file_obj.preview_rows)
            body = buffer.getvalue()
            content_type = 'text/csv; charset=utf-8'
        elif file_type == 'json':
            body = json.dumps(file_obj.preview_rows, ensure_ascii=False, indent=2)
            content_type = 'application/json'
        else:
            body = '\n'.join(json.dumps(row, ensure_ascii=False) for row in file_obj.preview_rows)
            content_type = 'application/jsonl'
    else:
        body = json.dumps({
            'path': file_obj.path,
            'fileType': file_obj.file_type,
            'sizeBytes': file_obj.size_bytes,
            'sha256': file_obj.sha256,
        }, ensure_ascii=False, indent=2)
        content_type = 'application/json'

    response = HttpResponse(body, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{file_obj.path.split("/")[-1]}"'
    return response


def _model_summary(repo: ModelRepo):
    latest = repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()
    latest_revision = latest.revision if latest else ''
    return {
        'id': repo.repo_id,
        'author': repo.author,
        'name': repo.name,
        'pipeline_tag': repo.pipeline_tag,
        'downloads': repo.downloads,
        'likes': repo.likes,
        'lastModified': repo.updated_at.date().isoformat(),
        'tags': repo.tags,
        'library': repo.library,
        'language': repo.language,
        'license': repo.license,
        'featured': repo.featured,
        'description': repo.description,
        'summary': repo.summary,
        'baseModel': repo.base_model,
        'dataset': repo.dataset,
        'visibility': repo.visibility,
        'hfCompatible': repo.hf_compatible,
        'latestRevision': latest_revision,
    }


def _model_file_payload(file_obj: ModelFile):
    return {
        'path': file_obj.path,
        'fileType': file_obj.file_type,
        'sizeBytes': file_obj.size_bytes,
        'size': file_obj.size_label,
        'sha256': file_obj.sha256,
        'previewText': file_obj.preview_text,
    }


def _model_version_payload(version: ModelVersion):
    return {
        'revision': version.revision,
        'commitSha': version.commit_sha,
        'framework': version.framework,
        'params': version.params_label,
        'quantization': version.quantization,
        'createdAt': version.created_at.isoformat(),
        'isLatest': version.is_latest,
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_list_v2(request):
    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'recent').strip()
    page = _int_param(request.query_params.get('page'), 1)
    page_size = min(_int_param(request.query_params.get('page_size'), 20), 100)

    queryset = DatasetRepo.objects.all()
    if search:
        queryset = queryset.filter(
            Q(repo_id__icontains=search)
            | Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(author__icontains=search)
            | Q(domain__icontains=search)
        )

    if sort == 'downloads':
        queryset = queryset.order_by('-downloads', 'repo_id')
    elif sort == 'likes':
        queryset = queryset.order_by('-likes', 'repo_id')
    elif sort == 'rows':
        queryset = queryset.order_by('-row_count', 'repo_id')
    elif sort == 'name':
        queryset = queryset.order_by('name', 'repo_id')
    else:
        queryset = queryset.order_by('-updated_at', 'repo_id')

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': [_dataset_summary(repo) for repo in page_obj.object_list],
            'total': paginator.count,
            'page': page_obj.number,
            'page_size': page_size,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_detail_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'code': 1, 'msg': 'Dataset not found', 'data': {}}, status=404)

    versions = list(repo.versions.all())
    latest = _get_dataset_version(repo)
    files = list(latest.files.all()) if latest else []
    preview_file = files[0] if files else None

    payload = _dataset_summary(repo)
    payload.update({
        'cardSections': repo.card_sections,
        'versions': [_dataset_version_payload(version) for version in versions],
        'files': [_dataset_file_payload(file_obj) for file_obj in files],
        'preview': _dataset_file_payload(preview_file) if preview_file else None,
        'usage': {
            'hfDatasets': f'from datasets import load_dataset\\n\\ndataset = load_dataset("{repo.repo_id}")',
            'gitClone': f'git clone https://your-hub.example/datasets/{repo.repo_id}',
        },
        'defaultRevision': latest.revision if latest else '',
        'splitSummary': _dataset_split_items(latest) if latest else [],
        'features': _dataset_features(latest) if latest else {},
    })
    return Response({'code': 0, 'msg': 'success', 'data': payload})


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_preview_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'code': 1, 'msg': 'Dataset not found', 'data': {}}, status=404)

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'code': 1, 'msg': 'Dataset version not found', 'data': {}}, status=404)

    path = _normalize_dataset_path(request.query_params.get('path', ''))
    file_obj = version.files.filter(path=path).first() if path else version.files.first()
    if not file_obj:
        return Response({'code': 1, 'msg': 'Dataset file not found', 'data': {}}, status=404)

    return Response({'code': 0, 'msg': 'success', 'data': _dataset_file_payload(file_obj)})


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_tree_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'code': 1, 'msg': 'Dataset not found', 'data': {}}, status=404)

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'code': 1, 'msg': 'Dataset version not found', 'data': {}}, status=404)

    current_path = request.query_params.get('path', '')
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'repoId': repo.repo_id,
            'revision': version.revision,
            'path': _normalize_dataset_path(current_path),
            'items': _list_tree_children(version, current_path),
        },
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_splits_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'code': 1, 'msg': 'Dataset not found', 'data': {}}, status=404)

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'code': 1, 'msg': 'Dataset version not found', 'data': {}}, status=404)

    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'repoId': repo.repo_id,
            'revision': version.revision,
            'splits': _dataset_split_items(version),
        },
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_rows_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'code': 1, 'msg': 'Dataset not found', 'data': {}}, status=404)

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'code': 1, 'msg': 'Dataset version not found', 'data': {}}, status=404)

    split = request.query_params.get('split', '')
    path = request.query_params.get('path', '')
    offset = request.query_params.get('offset', 0)
    length = request.query_params.get('length', 100)

    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'repoId': repo.repo_id,
            'revision': version.revision,
            **_dataset_rows_payload(version, split=split, path=path, offset=offset, length=length),
        },
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_list_datasets(request):
    search = (request.query_params.get('search') or '').strip().lower()
    limit = min(_int_param(request.query_params.get('limit'), 100), 200)

    items = []
    for repo in DatasetRepo.objects.all().order_by('repo_id'):
        if search and search not in repo.repo_id.lower() and search not in repo.name.lower():
            continue
        items.append({
            'id': repo.repo_id,
            'name': repo.name,
            'author': repo.author,
            'pipeline_tag': repo.task,
            'downloads': repo.downloads,
            'likes': repo.likes,
            'private': repo.visibility != 'public',
            'tags': repo.tags,
            'num_rows': repo.row_count,
            'description': repo.description,
        })
    return Response(items[:limit])


@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
def hf_dataset_metadata(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'error': f'Dataset {repo_id} not found'}, status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    payload = _dataset_summary(repo)
    payload.update({
        'sha': version.commit_sha,
        'siblings': [
            {'rfilename': file_obj.path, 'size': file_obj.size_bytes}
            for file_obj in version.files.all()
        ],
        'cardData': repo.card_sections,
        'dataset_info': _dataset_info_payload(repo, version)['dataset_info'],
    })
    return Response(payload)


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_tree(request, repo_id, revision):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    current_path = request.query_params.get('path', '')
    items = _list_tree_children(version, current_path)
    return Response([
        {
            'type': item['type'],
            'path': item['path'],
            'size': item.get('sizeBytes', 0),
            'oid': item.get('sha256', '') or version.commit_sha,
        }
        for item in items
    ])


@api_view(['POST'])
@permission_classes([AllowAny])
def hf_dataset_paths_info(request, repo_id, revision):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    paths = request.data.get('paths') or []
    if isinstance(paths, str):
        paths = [paths]

    results = []
    for path in paths:
        normalized = _normalize_dataset_path(path)
        direct_file = version.files.filter(path=normalized).first()
        if direct_file:
            results.append({
                'type': 'file',
                'path': normalized,
                'size': direct_file.size_bytes,
                'oid': direct_file.sha256 or version.commit_sha,
            })
            continue

        children = _list_tree_children(version, normalized)
        if children:
            results.append({
                'type': 'directory',
                'path': normalized,
                'size': 0,
                'oid': version.commit_sha,
            })
    return Response(results)


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_commits(request, repo_id, revision):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    return Response([{
        'id': version.commit_sha,
        'authors': [{'name': repo.author}],
        'date': version.created_at.isoformat(),
        'title': f'{repo.repo_id}@{version.revision}',
        'message': f'Hub revision {version.revision}',
    }])


@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
def hf_resolve_file(request, repo_id, revision, file_path):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return HttpResponse('Dataset not found', status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return HttpResponse('Dataset version not found', status=404)
    file_obj = version.files.filter(path=_normalize_dataset_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    return _dataset_file_response(file_obj)


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_is_valid(request):
    dataset = request.query_params.get('dataset', '')
    repo = _get_dataset_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    return Response({'preview': True, 'viewer': True, 'search': False, 'filter': False, 'statistics': False})


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_splits(request):
    dataset = request.query_params.get('dataset', '')
    revision = request.query_params.get('revision', '')
    repo = _get_dataset_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response({
        'dataset': repo.repo_id,
        'default_config': 'default',
        'splits': _dataset_split_items(version),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_dataset_info(request):
    dataset = request.query_params.get('dataset', '')
    revision = request.query_params.get('revision', '')
    repo = _get_dataset_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response(_dataset_info_payload(repo, version))


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_get_rows(request):
    dataset = request.query_params.get('dataset', '')
    revision = request.query_params.get('revision', '')
    split = request.query_params.get('split', '')
    path = request.query_params.get('path', '')
    offset = request.query_params.get('offset', 0)
    length = request.query_params.get('length', 100)

    repo = _get_dataset_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    return Response(_dataset_rows_payload(version, split=split, path=path, offset=offset, length=length))


@api_view(['GET'])
@permission_classes([AllowAny])
def hf_parquet_list(request):
    dataset = request.query_params.get('dataset', '')
    revision = request.query_params.get('revision', '')
    repo = _get_dataset_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    version = _get_dataset_version(repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    items = []
    for file_obj in version.files.filter(file_type='parquet'):
        items.append({
            'dataset': repo.repo_id,
            'config': 'default',
            'split': file_obj.split or 'default',
            'url': f'/api/v2/hf/datasets/{repo.repo_id}/resolve/{version.revision}/{file_obj.path}',
            'filename': file_obj.path.split('/')[-1],
            'size': file_obj.size_bytes,
        })
    return Response({'parquet_files': items})


@api_view(['GET'])
@permission_classes([AllowAny])
def model_list_v2(request):
    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'recent').strip()
    page = _int_param(request.query_params.get('page'), 1)
    page_size = min(_int_param(request.query_params.get('page_size'), 20), 100)

    queryset = ModelRepo.objects.all()
    if search:
        queryset = queryset.filter(
            Q(repo_id__icontains=search)
            | Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(author__icontains=search)
            | Q(pipeline_tag__icontains=search)
        )

    if sort == 'downloads':
        queryset = queryset.order_by('-downloads', 'repo_id')
    elif sort == 'likes':
        queryset = queryset.order_by('-likes', 'repo_id')
    elif sort == 'name':
        queryset = queryset.order_by('name', 'repo_id')
    else:
        queryset = queryset.order_by('-updated_at', 'repo_id')

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': [_model_summary(repo) for repo in page_obj.object_list],
            'total': paginator.count,
            'page': page_obj.number,
            'page_size': page_size,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def model_detail_v2(request, repo_id):
    repo = ModelRepo.objects.filter(repo_id=repo_id).first()
    if not repo:
        return Response({'code': 1, 'msg': 'Model not found', 'data': {}}, status=404)

    versions = list(repo.versions.all())
    latest = next((item for item in versions if item.is_latest), None) or (versions[0] if versions else None)
    files = list(latest.files.all()) if latest else []
    preview_file = files[0] if files else None

    payload = _model_summary(repo)
    payload.update({
        'metrics': repo.metrics,
        'cardSections': repo.card_sections,
        'versions': [_model_version_payload(version) for version in versions],
        'files': [_model_file_payload(file_obj) for file_obj in files],
        'preview': _model_file_payload(preview_file) if preview_file else None,
        'usage': {
            'transformers': (
                'from transformers import pipeline\\n\\n'
                f'pipe = pipeline("{repo.pipeline_tag}", model="{repo.repo_id}")\\n'
                'print(pipe("Hello world"))'
            ),
            'gitClone': f'git clone https://your-hub.example/models/{repo.repo_id}',
        },
    })
    return Response({'code': 0, 'msg': 'success', 'data': payload})
