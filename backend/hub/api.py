import csv
import hashlib
import io
import json
import mimetypes
import uuid
from pathlib import Path

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .auth import HubOpenAPIKeyAuthentication, can_read_repo, can_write_repo, default_author_for_user
from .models import (
    DatasetFile,
    DatasetRepo,
    DatasetVersion,
    KnowledgeBuild,
    KnowledgeFile,
    KnowledgeRepo,
    KnowledgeVersion,
    ModelFile,
    ModelRepo,
    ModelVersion,
)


AUTH_CLASSES = [HubOpenAPIKeyAuthentication, JWTAuthentication]


def _int_param(value, default, minimum=None):
    try:
        number = int(value)
    except (TypeError, ValueError):
        return default
    if minimum is not None:
        return max(minimum, number)
    return number


def _size_label(size_bytes):
    value = int(size_bytes or 0)
    if value >= 1024 * 1024 * 1024:
        return f'{value / (1024 * 1024 * 1024):.1f}GB'.replace('.0', '')
    if value >= 1024 * 1024:
        return f'{value / (1024 * 1024):.1f}MB'.replace('.0', '')
    if value >= 1024:
        return f'{value / 1024:.1f}KB'.replace('.0', '')
    return f'{value}B'


def _normalize_path(path):
    return (path or '').strip().strip('/')


def _repo_identity(payload, fallback_author=''):
    repo_id = (payload.get('repoId') or payload.get('repo_id') or '').strip()
    namespace = (payload.get('namespace') or '').strip()
    slug = (payload.get('slug') or '').strip()

    if repo_id:
        if '/' in repo_id:
            namespace, slug = repo_id.split('/', 1)
        else:
            namespace = namespace or fallback_author or 'users'
            slug = repo_id
            repo_id = f'{namespace}/{slug}'
    else:
        namespace = namespace or fallback_author or 'users'
        if not slug:
            return None
        repo_id = f'{namespace}/{slug}'

    if not namespace or not slug:
        return None
    return {'repo_id': repo_id, 'namespace': namespace, 'slug': slug}


def _file_type_from_path(path):
    suffix = Path(path or '').suffix.lower().lstrip('.')
    return suffix or 'text'


def _storage_root():
    return Path(settings.MEDIA_ROOT) / 'hub'


def _stored_file_path(repo_type, repo_id, revision, file_path):
    namespace, slug = repo_id.split('/', 1) if '/' in repo_id else ('default', repo_id)
    return _storage_root() / repo_type / namespace / slug / revision / _normalize_path(file_path)


def _decode_file_content(item):
    content = item.get('content')
    if content is None:
        return None
    encoding = (item.get('encoding') or 'utf-8').lower()
    if encoding == 'base64':
        import base64

        return base64.b64decode(content)
    return str(content).encode('utf-8')


def _write_file_to_storage(repo_type, repo_id, revision, path, raw_bytes):
    target = _stored_file_path(repo_type, repo_id, revision, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw_bytes)
    return target


def _infer_row_count_from_content(file_type, raw_bytes, preview_rows):
    file_type = (file_type or '').lower()
    fallback = len(preview_rows or [])
    if raw_bytes is None:
        return fallback

    try:
        text = raw_bytes.decode('utf-8', errors='replace')
        if file_type == 'jsonl':
            return len([line for line in text.splitlines() if line.strip()])
        if file_type == 'json':
            parsed = json.loads(text)
            return len(parsed) if isinstance(parsed, list) else 0
        if file_type == 'csv':
            lines = [line for line in text.splitlines() if line.strip()]
            return max(0, len(lines) - 1)
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback

    return fallback


def _visible_queryset(request, queryset):
    user = getattr(request, 'user', None)
    if getattr(user, 'is_superuser', False):
        return queryset
    if not getattr(user, 'is_authenticated', False):
        return queryset.filter(visibility='public')

    identifiers = {
        (getattr(user, 'username', '') or '').strip(),
        (getattr(user, 'email', '') or '').strip(),
        (getattr(user, 'name', '') or '').strip(),
    }
    email = (getattr(user, 'email', '') or '').strip()
    if email and '@' in email:
        identifiers.add(email.split('@', 1)[0])
    identifiers = [value for value in identifiers if value]
    if not identifiers:
        return queryset.filter(visibility='public')
    return queryset.filter(Q(visibility='public') | Q(author__in=identifiers))


def _file_payload(file_obj):
    payload = {
        'path': file_obj.path,
        'fileType': file_obj.file_type,
        'sizeBytes': file_obj.size_bytes,
        'size': file_obj.size_label,
        'sha256': file_obj.sha256,
        'previewText': getattr(file_obj, 'preview_text', ''),
    }
    if hasattr(file_obj, 'split'):
        payload['split'] = file_obj.split
    if hasattr(file_obj, 'row_count'):
        payload['rows'] = file_obj.row_count
        payload['previewRows'] = getattr(file_obj, 'preview_rows', [])
    return payload


def _dataset_summary(repo):
    latest = repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()
    return {
        'id': repo.repo_id,
        'repoType': 'dataset',
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


def _knowledge_summary(repo):
    latest = repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()
    return {
        'id': repo.repo_id,
        'repoType': 'knowledge',
        'author': repo.author,
        'name': repo.name,
        'description': repo.description,
        'summary': repo.summary,
        'status': repo.status,
        'lastModified': repo.updated_at.isoformat(),
        'visibility': repo.visibility,
        'downloads': repo.downloads,
        'likes': repo.likes,
        'tags': repo.tags,
        'metadata': repo.metadata,
        'sourceDataset': repo.source_dataset or '',
        'sourceFiles': repo.source_files,
        'fileCount': repo.file_count,
        'documentCount': repo.document_count,
        'vectorStore': repo.vector_store,
        'pipeline': repo.pipeline,
        'knowledgeGraph': repo.knowledge_graph,
        'retrieval': repo.retrieval,
        'mcp': repo.mcp,
        'hfCompatible': repo.hf_compatible,
        'latestRevision': latest.revision if latest else '',
    }


def _model_summary(repo):
    latest = repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()
    latest_revision = latest.revision if latest else ''
    return {
        'id': repo.repo_id,
        'repoType': 'model',
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


def _dataset_version_payload(version):
    return {
        'revision': version.revision,
        'commitSha': version.commit_sha,
        'rows': version.row_count,
        'size': version.size_label,
        'createdAt': version.created_at.isoformat(),
        'manifest': version.manifest,
        'isLatest': version.is_latest,
    }


def _knowledge_version_payload(version):
    return {
        'revision': version.revision,
        'commitSha': version.commit_sha,
        'createdAt': version.created_at.isoformat(),
        'manifest': version.manifest,
        'isLatest': version.is_latest,
    }


def _model_version_payload(version):
    return {
        'revision': version.revision,
        'commitSha': version.commit_sha,
        'framework': version.framework,
        'params': version.params_label,
        'quantization': version.quantization,
        'createdAt': version.created_at.isoformat(),
        'isLatest': version.is_latest,
    }


def _build_payload(build):
    return {
        'id': build.id,
        'trigger': build.trigger,
        'status': build.status,
        'progress': build.progress,
        'stages': build.stages,
        'errorMessage': build.error_message,
        'createdAt': build.created_at.isoformat(),
        'updatedAt': build.updated_at.isoformat(),
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


def _get_knowledge_repo(repo_id):
    return KnowledgeRepo.objects.filter(repo_id=repo_id).first()


def _get_knowledge_version(repo, revision=''):
    if not repo:
        return None
    if revision:
        version = repo.versions.filter(revision=revision).first()
        if version:
            return version
    return repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()


def _get_model_repo(repo_id):
    return ModelRepo.objects.filter(repo_id=repo_id).first()


def _get_model_version(repo, revision=''):
    if not repo:
        return None
    if revision:
        version = repo.versions.filter(revision=revision).first()
        if version:
            return version
    return repo.versions.filter(is_latest=True).first() or repo.versions.order_by('-created_at').first()


def _dataset_like_repo(repo_id):
    repo = _get_dataset_repo(repo_id)
    if repo:
        return ('dataset', repo)
    repo = _get_knowledge_repo(repo_id)
    if repo:
        return ('knowledge', repo)
    return (None, None)


def _dataset_like_version(repo_type, repo, revision=''):
    if repo_type == 'dataset':
        return _get_dataset_version(repo, revision)
    if repo_type == 'knowledge':
        return _get_knowledge_version(repo, revision)
    return None


def _dataset_features(version):
    first_row = None
    for file_obj in version.files.all():
        rows = getattr(file_obj, 'preview_rows', []) or []
        if rows:
            first_row = rows[0]
            break
    if not isinstance(first_row, dict):
        return {}
    return {key: _infer_feature_type(value) for key, value in first_row.items()}


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
        return {'feature': {key: _infer_feature_type(item) for key, item in value.items()}, '_type': 'Struct'}
    return {'dtype': 'string', '_type': 'Value'}


def _dataset_split_items(version):
    splits = {}
    for file_obj in version.files.all():
        split_name = getattr(file_obj, 'split', '') or ''
        row_count = int(getattr(file_obj, 'row_count', 0) or 0)
        if not split_name and not row_count:
            continue
        split_name = split_name or 'default'
        payload = splits.setdefault(
            split_name,
            {
                'dataset': version.repo.repo_id,
                'config': 'default',
                'split': split_name,
                'num_rows': 0,
                'num_bytes': 0,
            },
        )
        payload['num_rows'] += row_count
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
            'license': repo.license if hasattr(repo, 'license') else 'apache-2.0',
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


def _dataset_rows_payload(version, split='', path='', offset=0, length=100):
    file_obj = None
    normalized_path = _normalize_path(path)
    if normalized_path:
        file_obj = version.files.filter(path=normalized_path).first()
    elif split and hasattr(version.files.model, 'split'):
        file_obj = version.files.filter(split=split).order_by('sort_order', 'path').first()
    if not file_obj:
        file_obj = version.files.order_by('sort_order', 'path').first()
    if not file_obj:
        return {'rows': [], 'features': {}, 'num_rows_total': 0, 'file': None}

    rows = getattr(file_obj, 'preview_rows', []) or []
    start = max(0, int(offset or 0))
    end = start + max(1, int(length or 100))
    preview_rows = rows[start:end]
    return {
        'rows': [
            {'row_idx': start + index, 'row': row, 'truncated_cells': []}
            for index, row in enumerate(preview_rows)
        ],
        'features': _dataset_features(version),
        'num_rows_total': int(getattr(file_obj, 'row_count', 0) or len(rows)),
        'file': _file_payload(file_obj),
    }


def _list_tree_children(version, current_path=''):
    current_path = _normalize_path(current_path)
    directories = {}
    files = []

    for file_obj in version.files.all():
        full_path = _normalize_path(file_obj.path)
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
            directories[directory_path]['rowCount'] += int(getattr(file_obj, 'row_count', 0) or 0)
        else:
            payload = _file_payload(file_obj)
            payload.update({'type': 'file', 'name': remainder, 'rowCount': int(getattr(file_obj, 'row_count', 0) or 0)})
            files.append(payload)

    directory_items = []
    for item in directories.values():
        item['size'] = _size_label(item['sizeBytes'])
        directory_items.append(item)

    return sorted(directory_items, key=lambda item: item['name']) + sorted(files, key=lambda item: item['name'])


def _file_response(repo_type, version, file_obj):
    actual_path = _stored_file_path(repo_type, version.repo.repo_id, version.revision, file_obj.path)
    if actual_path.exists():
        content_type = mimetypes.guess_type(file_obj.path)[0] or 'application/octet-stream'
        response = HttpResponse(actual_path.read_bytes(), content_type=content_type)
        response['Content-Disposition'] = f'inline; filename="{Path(file_obj.path).name}"'
        return response

    file_type = (file_obj.file_type or '').lower()
    content_type = 'text/plain; charset=utf-8'

    if getattr(file_obj, 'preview_text', ''):
        body = file_obj.preview_text
    elif getattr(file_obj, 'preview_rows', []):
        preview_rows = file_obj.preview_rows
        if file_type == 'csv':
            fieldnames = list(preview_rows[0].keys()) if preview_rows else []
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(preview_rows)
            body = buffer.getvalue()
            content_type = 'text/csv; charset=utf-8'
        elif file_type == 'json':
            body = json.dumps(preview_rows, ensure_ascii=False, indent=2)
            content_type = 'application/json'
        else:
            body = '\n'.join(json.dumps(row, ensure_ascii=False) for row in preview_rows)
            content_type = 'application/jsonl'
    else:
        body = json.dumps(_file_payload(file_obj), ensure_ascii=False, indent=2)
        content_type = 'application/json'

    response = HttpResponse(body, content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{Path(file_obj.path).name}"'
    return response


def _repo_not_found(message='Repository not found'):
    return Response({'code': 1, 'msg': message, 'data': {}}, status=404)


def _forbidden(message='Permission denied'):
    return Response({'code': 1, 'msg': message, 'data': {}}, status=403)


def _bad_request(message):
    return Response({'code': 1, 'msg': message, 'data': {}}, status=400)


def _save_revision_files(repo_type, repo_id, revision_name, file_model, version, files):
    field_names = {field.name for field in file_model._meta.fields}
    total_size = 0
    total_rows = 0
    created = []

    for index, item in enumerate(files or []):
        path = _normalize_path(item.get('path'))
        if not path:
            continue

        raw_bytes = _decode_file_content(item)
        preview_text = item.get('previewText') or item.get('preview_text') or ''
        preview_rows = item.get('previewRows') or item.get('preview_rows') or []
        file_type = item.get('fileType') or item.get('file_type') or _file_type_from_path(path)
        size_bytes = int(item.get('sizeBytes') or item.get('size_bytes') or (len(raw_bytes) if raw_bytes is not None else 0))
        sha256 = item.get('sha256') or ''

        if raw_bytes is not None:
            _write_file_to_storage(repo_type, repo_id, revision_name, path, raw_bytes)
            if not sha256:
                sha256 = hashlib.sha256(raw_bytes).hexdigest()
            if not preview_text and file_type in {'md', 'txt', 'json', 'yaml', 'yml', 'py', 'js', 'ts'}:
                preview_text = raw_bytes.decode('utf-8', errors='replace')[:4000]
            if not size_bytes:
                size_bytes = len(raw_bytes)

        kwargs = {
            'version': version,
            'path': path,
            'file_type': file_type,
            'size_bytes': size_bytes,
            'size_label': item.get('size') or _size_label(size_bytes),
            'sha256': sha256,
            'preview_text': preview_text,
            'sort_order': int(item.get('sortOrder') or item.get('sort_order') or index),
        }
        if 'split' in field_names:
            kwargs['split'] = item.get('split', '')
        if 'row_count' in field_names:
            row_count = item.get('rowCount')
            if row_count is None:
                row_count = item.get('rows')
            if row_count is None:
                row_count = _infer_row_count_from_content(file_type, raw_bytes, preview_rows)
            kwargs['row_count'] = row_count
            kwargs['preview_rows'] = preview_rows
            total_rows += int(row_count or 0)

        total_size += size_bytes
        created.append(file_model.objects.create(**kwargs))

    return created, total_size, total_rows


def _ensure_write_access(request, repo=None):
    if not can_write_repo(request, repo):
        return _forbidden('Write access required')
    return None


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_list_v2(request):
    if request.method == 'POST':
        denied = _ensure_write_access(request)
        if denied:
            return denied

        identity = _repo_identity(request.data, fallback_author=default_author_for_user(request.user))
        if not identity:
            return _bad_request('repoId or namespace/slug is required')
        if DatasetRepo.objects.filter(repo_id=identity['repo_id']).exists():
            return _bad_request('Dataset repo already exists')

        author = (request.data.get('author') or default_author_for_user(request.user)).strip()
        repo = DatasetRepo.objects.create(
            **identity,
            author=author,
            name=(request.data.get('name') or identity['slug']).strip(),
            task=(request.data.get('task') or 'text-generation').strip(),
            domain=(request.data.get('domain') or 'general').strip(),
            modality=(request.data.get('modality') or 'text').strip(),
            language=(request.data.get('language') or 'en').strip(),
            license=(request.data.get('license') or 'apache-2.0').strip(),
            description=(request.data.get('description') or '').strip(),
            summary=(request.data.get('summary') or '').strip(),
            visibility=(request.data.get('visibility') or 'public').strip(),
            dataset_type=(request.data.get('datasetType') or request.data.get('dataset_type') or '').strip(),
            readonly=bool(request.data.get('readonly', False)),
            tags=request.data.get('tags') or [],
            metadata=request.data.get('metadata') or {},
            card_sections=request.data.get('cardSections') or request.data.get('card_sections') or [],
            parent_repo_id=(request.data.get('parentDataset') or request.data.get('parent_repo_id') or '').strip(),
            derived_repo_ids=request.data.get('derivedDatasets') or [],
            hf_compatible=bool(request.data.get('hfCompatible', True)),
        )
        return Response({'code': 0, 'msg': 'success', 'data': _dataset_summary(repo)}, status=201)

    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'recent').strip()
    page = _int_param(request.query_params.get('page'), 1, 1)
    page_size = min(_int_param(request.query_params.get('page_size'), 20, 1), 100)

    queryset = _visible_queryset(request, DatasetRepo.objects.all())
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
        'data': {'list': [_dataset_summary(repo) for repo in page_obj.object_list], 'total': paginator.count, 'page': page_obj.number, 'page_size': page_size},
    })


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_detail_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if not can_read_repo(request, repo):
        return _forbidden('Dataset is private')

    if request.method == 'PATCH':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        for field, key in [
            ('name', 'name'),
            ('task', 'task'),
            ('domain', 'domain'),
            ('modality', 'modality'),
            ('language', 'language'),
            ('license', 'license'),
            ('description', 'description'),
            ('summary', 'summary'),
            ('visibility', 'visibility'),
            ('dataset_type', 'datasetType'),
            ('parent_repo_id', 'parentDataset'),
        ]:
            if key in request.data:
                setattr(repo, field, request.data.get(key) or '')
        if 'readonly' in request.data:
            repo.readonly = bool(request.data.get('readonly'))
        if 'derivedDatasets' in request.data:
            repo.derived_repo_ids = request.data.get('derivedDatasets') or []
        if 'tags' in request.data:
            repo.tags = request.data.get('tags') or []
        if 'metadata' in request.data:
            repo.metadata = request.data.get('metadata') or {}
        if 'cardSections' in request.data:
            repo.card_sections = request.data.get('cardSections') or []
        if 'hfCompatible' in request.data:
            repo.hf_compatible = bool(request.data.get('hfCompatible'))
        repo.save()

    if request.method == 'DELETE':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        repo.delete()
        return Response({'code': 0, 'msg': 'success', 'data': {}})

    selected_version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    versions = list(repo.versions.all())
    files = list(selected_version.files.all()) if selected_version else []
    preview_file = files[0] if files else None

    payload = _dataset_summary(repo)
    payload.update(
        {
            'cardSections': repo.card_sections,
            'versions': [_dataset_version_payload(version) for version in versions],
            'files': [_file_payload(file_obj) for file_obj in files],
            'preview': _file_payload(preview_file) if preview_file else None,
            'usage': {
                'hfDatasets': f'from datasets import load_dataset\n\ndataset = load_dataset("{repo.repo_id}")',
                'gitClone': f'git clone https://your-hub.example/datasets/{repo.repo_id}',
            },
            'defaultRevision': selected_version.revision if selected_version else '',
            'splitSummary': _dataset_split_items(selected_version) if selected_version else [],
            'features': _dataset_features(selected_version) if selected_version else {},
        }
    )
    return Response({'code': 0, 'msg': 'success', 'data': payload})


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_revisions_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if request.method == 'GET':
        if not can_read_repo(request, repo):
            return _forbidden('Dataset is private')
        return Response({'code': 0, 'msg': 'success', 'data': [_dataset_version_payload(version) for version in repo.versions.all()]})

    denied = _ensure_write_access(request, repo)
    if denied:
        return denied

    revision_name = (request.data.get('revision') or '').strip()
    if not revision_name:
        return _bad_request('revision is required')
    if repo.versions.filter(revision=revision_name).exists():
        return _bad_request('revision already exists')

    mark_latest = bool(request.data.get('markLatest', True))
    if mark_latest:
        repo.versions.update(is_latest=False)
    version = DatasetVersion.objects.create(
        repo=repo,
        revision=revision_name,
        commit_sha=(request.data.get('commitSha') or uuid.uuid4().hex[:12]).strip(),
        manifest=request.data.get('manifest') or {},
        row_count=int(request.data.get('rowCount') or 0),
        size_label=request.data.get('size') or '0B',
        is_latest=mark_latest,
    )
    files, total_size, total_rows = _save_revision_files('datasets', repo.repo_id, revision_name, DatasetFile, version, request.data.get('files') or [])
    if total_rows:
        version.row_count = int(request.data.get('rowCount') or total_rows)
    if total_size:
        version.size_label = request.data.get('size') or _size_label(total_size)
    version.save(update_fields=['row_count', 'size_label'])
    if mark_latest:
        repo.row_count = version.row_count
        repo.size_label = version.size_label
        repo.save(update_fields=['row_count', 'size_label', 'updated_at'])
    return Response({'code': 0, 'msg': 'success', 'data': {'version': _dataset_version_payload(version), 'files': [_file_payload(item) for item in files]}}, status=201)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_preview_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if not can_read_repo(request, repo):
        return _forbidden('Dataset is private')

    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Dataset version not found')
    path = _normalize_path(request.query_params.get('path', ''))
    file_obj = version.files.filter(path=path).first() if path else version.files.first()
    if not file_obj:
        return _repo_not_found('Dataset file not found')
    return Response({'code': 0, 'msg': 'success', 'data': _file_payload(file_obj)})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_tree_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if not can_read_repo(request, repo):
        return _forbidden('Dataset is private')
    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Dataset version not found')
    current_path = request.query_params.get('path', '')
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, 'path': _normalize_path(current_path), 'items': _list_tree_children(version, current_path)}})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_splits_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if not can_read_repo(request, repo):
        return _forbidden('Dataset is private')
    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Dataset version not found')
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, 'splits': _dataset_split_items(version)}})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_rows_v2(request, repo_id):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return _repo_not_found('Dataset not found')
    if not can_read_repo(request, repo):
        return _forbidden('Dataset is private')
    version = _get_dataset_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Dataset version not found')
    payload = _dataset_rows_payload(
        version,
        split=request.query_params.get('split', ''),
        path=request.query_params.get('path', ''),
        offset=request.query_params.get('offset', 0),
        length=request.query_params.get('length', 100),
    )
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, **payload}})


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def dataset_resolve_v2(request, repo_id, revision, file_path):
    repo = _get_dataset_repo(repo_id)
    if not repo:
        return HttpResponse('Dataset not found', status=404)
    if not can_read_repo(request, repo):
        return HttpResponse('Dataset is private', status=403)
    version = _get_dataset_version(repo, revision)
    if not version:
        return HttpResponse('Dataset version not found', status=404)
    file_obj = version.files.filter(path=_normalize_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    return _file_response('datasets', version, file_obj)


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_list_v2(request):
    if request.method == 'POST':
        denied = _ensure_write_access(request)
        if denied:
            return denied
        identity = _repo_identity(request.data, fallback_author=default_author_for_user(request.user))
        if not identity:
            return _bad_request('repoId or namespace/slug is required')
        if ModelRepo.objects.filter(repo_id=identity['repo_id']).exists():
            return _bad_request('Model repo already exists')
        author = (request.data.get('author') or default_author_for_user(request.user)).strip()
        repo = ModelRepo.objects.create(
            **identity,
            author=author,
            name=(request.data.get('name') or identity['slug']).strip(),
            pipeline_tag=(request.data.get('pipeline_tag') or request.data.get('pipelineTag') or 'text-generation').strip(),
            library=(request.data.get('library') or 'transformers').strip(),
            language=(request.data.get('language') or 'en').strip(),
            license=(request.data.get('license') or 'apache-2.0').strip(),
            description=(request.data.get('description') or '').strip(),
            summary=(request.data.get('summary') or '').strip(),
            visibility=(request.data.get('visibility') or 'public').strip(),
            featured=bool(request.data.get('featured', False)),
            base_model=(request.data.get('baseModel') or request.data.get('base_model') or '').strip(),
            dataset=(request.data.get('dataset') or '').strip(),
            tags=request.data.get('tags') or [],
            metrics=request.data.get('metrics') or [],
            card_sections=request.data.get('cardSections') or request.data.get('card_sections') or [],
            hf_compatible=bool(request.data.get('hfCompatible', True)),
        )
        return Response({'code': 0, 'msg': 'success', 'data': _model_summary(repo)}, status=201)

    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'recent').strip()
    page = _int_param(request.query_params.get('page'), 1, 1)
    page_size = min(_int_param(request.query_params.get('page_size'), 20, 1), 100)

    queryset = _visible_queryset(request, ModelRepo.objects.all())
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
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [_model_summary(repo) for repo in page_obj.object_list], 'total': paginator.count, 'page': page_obj.number, 'page_size': page_size}})


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_detail_v2(request, repo_id):
    repo = _get_model_repo(repo_id)
    if not repo:
        return _repo_not_found('Model not found')
    if not can_read_repo(request, repo):
        return _forbidden('Model is private')

    if request.method == 'PATCH':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        for field, key in [
            ('name', 'name'),
            ('pipeline_tag', 'pipelineTag'),
            ('library', 'library'),
            ('language', 'language'),
            ('license', 'license'),
            ('description', 'description'),
            ('summary', 'summary'),
            ('visibility', 'visibility'),
            ('base_model', 'baseModel'),
            ('dataset', 'dataset'),
        ]:
            if key in request.data:
                setattr(repo, field, request.data.get(key) or '')
        if 'featured' in request.data:
            repo.featured = bool(request.data.get('featured'))
        if 'tags' in request.data:
            repo.tags = request.data.get('tags') or []
        if 'metrics' in request.data:
            repo.metrics = request.data.get('metrics') or []
        if 'cardSections' in request.data:
            repo.card_sections = request.data.get('cardSections') or []
        if 'hfCompatible' in request.data:
            repo.hf_compatible = bool(request.data.get('hfCompatible'))
        repo.save()

    if request.method == 'DELETE':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        repo.delete()
        return Response({'code': 0, 'msg': 'success', 'data': {}})

    selected_version = _get_model_version(repo, request.query_params.get('revision', ''))
    versions = list(repo.versions.all())
    files = list(selected_version.files.all()) if selected_version else []
    preview_file = files[0] if files else None

    payload = _model_summary(repo)
    payload.update(
        {
            'metrics': repo.metrics,
            'cardSections': repo.card_sections,
            'versions': [_model_version_payload(version) for version in versions],
            'files': [_file_payload(file_obj) for file_obj in files],
            'preview': _file_payload(preview_file) if preview_file else None,
            'usage': {
                'transformers': (
                    'from transformers import pipeline\n\n'
                    f'pipe = pipeline("{repo.pipeline_tag}", model="{repo.repo_id}")\n'
                    'print(pipe("Hello world"))'
                ),
                'gitClone': f'git clone https://your-hub.example/models/{repo.repo_id}',
            },
            'selectedRevision': selected_version.revision if selected_version else '',
        }
    )
    return Response({'code': 0, 'msg': 'success', 'data': payload})


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_revisions_v2(request, repo_id):
    repo = _get_model_repo(repo_id)
    if not repo:
        return _repo_not_found('Model not found')
    if request.method == 'GET':
        if not can_read_repo(request, repo):
            return _forbidden('Model is private')
        return Response({'code': 0, 'msg': 'success', 'data': [_model_version_payload(version) for version in repo.versions.all()]})

    denied = _ensure_write_access(request, repo)
    if denied:
        return denied

    revision_name = (request.data.get('revision') or '').strip()
    if not revision_name:
        return _bad_request('revision is required')
    if repo.versions.filter(revision=revision_name).exists():
        return _bad_request('revision already exists')

    mark_latest = bool(request.data.get('markLatest', True))
    if mark_latest:
        repo.versions.update(is_latest=False)
    version = ModelVersion.objects.create(
        repo=repo,
        revision=revision_name,
        commit_sha=(request.data.get('commitSha') or uuid.uuid4().hex[:12]).strip(),
        framework=(request.data.get('framework') or repo.library or 'transformers').strip(),
        params_label=(request.data.get('params') or request.data.get('paramsLabel') or '').strip(),
        quantization=(request.data.get('quantization') or '').strip(),
        is_latest=mark_latest,
    )
    files, _, _ = _save_revision_files('models', repo.repo_id, revision_name, ModelFile, version, request.data.get('files') or [])
    return Response({'code': 0, 'msg': 'success', 'data': {'version': _model_version_payload(version), 'files': [_file_payload(item) for item in files]}}, status=201)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_tree_v2(request, repo_id):
    repo = _get_model_repo(repo_id)
    if not repo:
        return _repo_not_found('Model not found')
    if not can_read_repo(request, repo):
        return _forbidden('Model is private')
    version = _get_model_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Model version not found')
    current_path = request.query_params.get('path', '')
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, 'path': _normalize_path(current_path), 'items': _list_tree_children(version, current_path)}})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_preview_v2(request, repo_id):
    repo = _get_model_repo(repo_id)
    if not repo:
        return _repo_not_found('Model not found')
    if not can_read_repo(request, repo):
        return _forbidden('Model is private')
    version = _get_model_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Model version not found')
    path = _normalize_path(request.query_params.get('path', ''))
    file_obj = version.files.filter(path=path).first() if path else version.files.first()
    if not file_obj:
        return _repo_not_found('Model file not found')
    return Response({'code': 0, 'msg': 'success', 'data': _file_payload(file_obj)})


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def model_resolve_v2(request, repo_id, revision, file_path):
    repo = _get_model_repo(repo_id)
    if not repo:
        return HttpResponse('Model not found', status=404)
    if not can_read_repo(request, repo):
        return HttpResponse('Model is private', status=403)
    version = _get_model_version(repo, revision)
    if not version:
        return HttpResponse('Model version not found', status=404)
    file_obj = version.files.filter(path=_normalize_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    return _file_response('models', version, file_obj)


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_list_v2(request):
    if request.method == 'POST':
        denied = _ensure_write_access(request)
        if denied:
            return denied
        identity = _repo_identity(request.data, fallback_author=default_author_for_user(request.user))
        if not identity:
            return _bad_request('repoId or namespace/slug is required')
        if KnowledgeRepo.objects.filter(repo_id=identity['repo_id']).exists():
            return _bad_request('Knowledge repo already exists')
        author = (request.data.get('author') or default_author_for_user(request.user)).strip()
        repo = KnowledgeRepo.objects.create(
            **identity,
            author=author,
            name=(request.data.get('name') or identity['slug']).strip(),
            description=(request.data.get('description') or '').strip(),
            summary=(request.data.get('summary') or '').strip(),
            visibility=(request.data.get('visibility') or 'public').strip(),
            status=(request.data.get('status') or 'pending').strip(),
            source_dataset=(request.data.get('sourceDataset') or request.data.get('source_dataset') or '').strip(),
            source_files=request.data.get('sourceFiles') or [],
            tags=request.data.get('tags') or [],
            metadata=request.data.get('metadata') or {},
            card_sections=request.data.get('cardSections') or [],
            vector_store=request.data.get('vectorStore') or {},
            pipeline=request.data.get('pipeline') or {},
            knowledge_graph=request.data.get('knowledgeGraph') or {},
            retrieval=request.data.get('retrieval') or {},
            mcp=request.data.get('mcp') or {},
            hf_compatible=bool(request.data.get('hfCompatible', True)),
        )
        return Response({'code': 0, 'msg': 'success', 'data': _knowledge_summary(repo)}, status=201)

    search = (request.query_params.get('search') or request.query_params.get('q') or '').strip()
    sort = (request.query_params.get('sort') or 'recent').strip()
    page = _int_param(request.query_params.get('page'), 1, 1)
    page_size = min(_int_param(request.query_params.get('page_size'), 20, 1), 100)

    queryset = _visible_queryset(request, KnowledgeRepo.objects.all())
    if search:
        queryset = queryset.filter(
            Q(repo_id__icontains=search)
            | Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(author__icontains=search)
            | Q(source_dataset__icontains=search)
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
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [_knowledge_summary(repo) for repo in page_obj.object_list], 'total': paginator.count, 'page': page_obj.number, 'page_size': page_size}})


@api_view(['GET', 'PATCH', 'DELETE'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_detail_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if not can_read_repo(request, repo):
        return _forbidden('Knowledge repo is private')

    if request.method == 'PATCH':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        for field, key in [
            ('name', 'name'),
            ('description', 'description'),
            ('summary', 'summary'),
            ('visibility', 'visibility'),
            ('status', 'status'),
            ('source_dataset', 'sourceDataset'),
        ]:
            if key in request.data:
                setattr(repo, field, request.data.get(key) or '')
        if 'sourceFiles' in request.data:
            repo.source_files = request.data.get('sourceFiles') or []
        if 'tags' in request.data:
            repo.tags = request.data.get('tags') or []
        if 'metadata' in request.data:
            repo.metadata = request.data.get('metadata') or {}
        if 'cardSections' in request.data:
            repo.card_sections = request.data.get('cardSections') or []
        if 'vectorStore' in request.data:
            repo.vector_store = request.data.get('vectorStore') or {}
        if 'pipeline' in request.data:
            repo.pipeline = request.data.get('pipeline') or {}
        if 'knowledgeGraph' in request.data:
            repo.knowledge_graph = request.data.get('knowledgeGraph') or {}
        if 'retrieval' in request.data:
            repo.retrieval = request.data.get('retrieval') or {}
        if 'mcp' in request.data:
            repo.mcp = request.data.get('mcp') or {}
        if 'hfCompatible' in request.data:
            repo.hf_compatible = bool(request.data.get('hfCompatible'))
        repo.save()

    if request.method == 'DELETE':
        denied = _ensure_write_access(request, repo)
        if denied:
            return denied
        repo.delete()
        return Response({'code': 0, 'msg': 'success', 'data': {}})

    selected_version = _get_knowledge_version(repo, request.query_params.get('revision', ''))
    versions = list(repo.versions.all())
    files = list(selected_version.files.all()) if selected_version else []
    preview_file = files[0] if files else None
    builds = list(repo.builds.all()[:10])

    payload = _knowledge_summary(repo)
    payload.update(
        {
            'cardSections': repo.card_sections,
            'versions': [_knowledge_version_payload(version) for version in versions],
            'files': [_file_payload(file_obj) for file_obj in files],
            'preview': _file_payload(preview_file) if preview_file else None,
            'builds': [_build_payload(build) for build in builds],
            'usage': {
                'hfDatasets': f'from datasets import load_dataset\n\nkb = load_dataset("{repo.repo_id}")',
                'gitClone': f'git clone https://your-hub.example/knowledge-bases/{repo.repo_id}',
                'notebook': f'Open /notebook?knowledge_base={repo.repo_id}',
            },
            'defaultRevision': selected_version.revision if selected_version else '',
            'features': _dataset_features(selected_version) if selected_version else {},
        }
    )
    return Response({'code': 0, 'msg': 'success', 'data': payload})


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_revisions_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if request.method == 'GET':
        if not can_read_repo(request, repo):
            return _forbidden('Knowledge repo is private')
        return Response({'code': 0, 'msg': 'success', 'data': [_knowledge_version_payload(version) for version in repo.versions.all()]})

    denied = _ensure_write_access(request, repo)
    if denied:
        return denied
    revision_name = (request.data.get('revision') or '').strip()
    if not revision_name:
        return _bad_request('revision is required')
    if repo.versions.filter(revision=revision_name).exists():
        return _bad_request('revision already exists')

    mark_latest = bool(request.data.get('markLatest', True))
    if mark_latest:
        repo.versions.update(is_latest=False)
    version = KnowledgeVersion.objects.create(
        repo=repo,
        revision=revision_name,
        commit_sha=(request.data.get('commitSha') or uuid.uuid4().hex[:12]).strip(),
        manifest=request.data.get('manifest') or {},
        is_latest=mark_latest,
    )
    files, total_size, total_rows = _save_revision_files('knowledge-bases', repo.repo_id, revision_name, KnowledgeFile, version, request.data.get('files') or [])
    repo.file_count = len(files)
    if total_rows:
        repo.document_count = total_rows
    repo.save(update_fields=['file_count', 'document_count', 'updated_at'])
    return Response({'code': 0, 'msg': 'success', 'data': {'version': _knowledge_version_payload(version), 'files': [_file_payload(item) for item in files], 'size': _size_label(total_size)}}, status=201)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_tree_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if not can_read_repo(request, repo):
        return _forbidden('Knowledge repo is private')
    version = _get_knowledge_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Knowledge version not found')
    current_path = request.query_params.get('path', '')
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, 'path': _normalize_path(current_path), 'items': _list_tree_children(version, current_path)}})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_preview_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if not can_read_repo(request, repo):
        return _forbidden('Knowledge repo is private')
    version = _get_knowledge_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Knowledge version not found')
    path = _normalize_path(request.query_params.get('path', ''))
    file_obj = version.files.filter(path=path).first() if path else version.files.first()
    if not file_obj:
        return _repo_not_found('Knowledge file not found')
    return Response({'code': 0, 'msg': 'success', 'data': _file_payload(file_obj)})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_rows_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if not can_read_repo(request, repo):
        return _forbidden('Knowledge repo is private')
    version = _get_knowledge_version(repo, request.query_params.get('revision', ''))
    if not version:
        return _repo_not_found('Knowledge version not found')
    payload = _dataset_rows_payload(
        version,
        path=request.query_params.get('path', ''),
        offset=request.query_params.get('offset', 0),
        length=request.query_params.get('length', 100),
    )
    return Response({'code': 0, 'msg': 'success', 'data': {'repoId': repo.repo_id, 'revision': version.revision, **payload}})


@api_view(['GET', 'POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_builds_v2(request, repo_id):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return _repo_not_found('Knowledge repo not found')
    if request.method == 'GET':
        if not can_read_repo(request, repo):
            return _forbidden('Knowledge repo is private')
        return Response({'code': 0, 'msg': 'success', 'data': [_build_payload(build) for build in repo.builds.all()]})

    denied = _ensure_write_access(request, repo)
    if denied:
        return denied

    stages = request.data.get('stages') or [
        {'name': 'parse', 'status': 'running', 'label': 'Document Parsing'},
        {'name': 'chunk', 'status': 'pending', 'label': 'Text Chunking'},
        {'name': 'embed', 'status': 'pending', 'label': 'Embedding'},
        {'name': 'index', 'status': 'pending', 'label': 'Index Building'},
        {'name': 'graph', 'status': 'pending', 'label': 'Knowledge Graph'},
    ]
    build = KnowledgeBuild.objects.create(
        repo=repo,
        trigger=(request.data.get('trigger') or 'manual').strip(),
        status=(request.data.get('status') or 'running').strip(),
        progress=int(request.data.get('progress') or 5),
        stages=stages,
        error_message=(request.data.get('errorMessage') or '').strip(),
    )
    repo.status = 'processing' if build.status in {'queued', 'running'} else build.status
    repo.pipeline = {
        'stages': stages,
        'progress': build.progress,
        'lastRun': build.created_at.isoformat(),
        'error': build.error_message,
    }
    repo.save(update_fields=['status', 'pipeline', 'updated_at'])
    return Response({'code': 0, 'msg': 'success', 'data': _build_payload(build)}, status=201)


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def knowledge_resolve_v2(request, repo_id, revision, file_path):
    repo = _get_knowledge_repo(repo_id)
    if not repo:
        return HttpResponse('Knowledge repo not found', status=404)
    if not can_read_repo(request, repo):
        return HttpResponse('Knowledge repo is private', status=403)
    version = _get_knowledge_version(repo, revision)
    if not version:
        return HttpResponse('Knowledge version not found', status=404)
    file_obj = version.files.filter(path=_normalize_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    return _file_response('knowledge-bases', version, file_obj)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_list_datasets(request):
    search = (request.query_params.get('search') or '').strip().lower()
    limit = min(_int_param(request.query_params.get('limit'), 100, 1), 200)

    items = []
    for repo in _visible_queryset(request, DatasetRepo.objects.all()).order_by('repo_id'):
        if search and search not in repo.repo_id.lower() and search not in repo.name.lower():
            continue
        items.append({'id': repo.repo_id, 'name': repo.name, 'author': repo.author, 'pipeline_tag': repo.task, 'downloads': repo.downloads, 'likes': repo.likes, 'private': repo.visibility != 'public', 'tags': repo.tags, 'num_rows': repo.row_count, 'description': repo.description})
    for repo in _visible_queryset(request, KnowledgeRepo.objects.all()).order_by('repo_id'):
        if not repo.hf_compatible:
            continue
        if search and search not in repo.repo_id.lower() and search not in repo.name.lower():
            continue
        items.append({'id': repo.repo_id, 'name': repo.name, 'author': repo.author, 'pipeline_tag': 'knowledge-base', 'downloads': repo.downloads, 'likes': repo.likes, 'private': repo.visibility != 'public', 'tags': repo.tags, 'num_rows': repo.document_count, 'description': repo.description})
    return Response(items[:limit])


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_dataset_metadata(request, repo_id):
    repo_type, repo = _dataset_like_repo(repo_id)
    if not repo:
        return Response({'error': f'Dataset {repo_id} not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': f'Dataset {repo_id} is private'}, status=403)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    version = _dataset_like_version(repo_type, repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    base_payload = _dataset_summary(repo) if repo_type == 'dataset' else _knowledge_summary(repo)
    payload = dict(base_payload)
    payload.update({'sha': version.commit_sha, 'siblings': [{'rfilename': file_obj.path, 'size': file_obj.size_bytes} for file_obj in version.files.all()], 'cardData': repo.card_sections, 'dataset_info': _dataset_info_payload(repo, version)['dataset_info']})
    return Response(payload)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_dataset_tree(request, repo_id, revision):
    repo_type, repo = _dataset_like_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    items = _list_tree_children(version, request.query_params.get('path', ''))
    return Response([{'type': item['type'], 'path': item['path'], 'size': item.get('sizeBytes', 0), 'oid': item.get('sha256', '') or version.commit_sha} for item in items])


@api_view(['POST'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_dataset_paths_info(request, repo_id, revision):
    repo_type, repo = _dataset_like_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    paths = request.data.get('paths') or []
    if isinstance(paths, str):
        paths = [paths]
    results = []
    for path in paths:
        normalized = _normalize_path(path)
        direct_file = version.files.filter(path=normalized).first()
        if direct_file:
            results.append({'type': 'file', 'path': normalized, 'size': direct_file.size_bytes, 'oid': direct_file.sha256 or version.commit_sha})
            continue
        children = _list_tree_children(version, normalized)
        if children:
            results.append({'type': 'directory', 'path': normalized, 'size': 0, 'oid': version.commit_sha})
    return Response(results)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_dataset_commits(request, repo_id, revision):
    repo_type, repo = _dataset_like_repo(repo_id)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, revision)
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response([{'id': version.commit_sha, 'authors': [{'name': repo.author}], 'date': version.created_at.isoformat(), 'title': f'{repo.repo_id}@{version.revision}', 'message': f'Hub revision {version.revision}'}])


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_resolve_file(request, repo_id, revision, file_path):
    repo_type, repo = _dataset_like_repo(repo_id)
    if not repo:
        return HttpResponse('Dataset not found', status=404)
    if not can_read_repo(request, repo):
        return HttpResponse('Dataset is private', status=403)
    version = _dataset_like_version(repo_type, repo, revision)
    if not version:
        return HttpResponse('Dataset version not found', status=404)
    file_obj = version.files.filter(path=_normalize_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    storage_type = 'datasets' if repo_type == 'dataset' else 'knowledge-bases'
    return _file_response(storage_type, version, file_obj)


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_is_valid(request):
    dataset = request.query_params.get('dataset', '')
    repo_type, repo = _dataset_like_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    return Response({'preview': True, 'viewer': True, 'search': False, 'filter': False, 'statistics': False})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_get_splits(request):
    dataset = request.query_params.get('dataset', '')
    repo_type, repo = _dataset_like_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response({'dataset': repo.repo_id, 'default_config': 'default', 'splits': _dataset_split_items(version)})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_dataset_info(request):
    dataset = request.query_params.get('dataset', '')
    repo_type, repo = _dataset_like_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response(_dataset_info_payload(repo, version))


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_get_rows(request):
    dataset = request.query_params.get('dataset', '')
    repo_type, repo = _dataset_like_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)
    return Response(_dataset_rows_payload(version, split=request.query_params.get('split', ''), path=request.query_params.get('path', ''), offset=request.query_params.get('offset', 0), length=request.query_params.get('length', 100)))


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_parquet_list(request):
    dataset = request.query_params.get('dataset', '')
    repo_type, repo = _dataset_like_repo(dataset)
    if not repo:
        return Response({'error': 'Dataset not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': 'Dataset is private'}, status=403)
    version = _dataset_like_version(repo_type, repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Dataset version not found'}, status=404)

    items = []
    for file_obj in version.files.filter(file_type='parquet'):
        items.append({'dataset': repo.repo_id, 'config': 'default', 'split': getattr(file_obj, 'split', '') or 'default', 'url': f'/api/v2/hf/datasets/{repo.repo_id}/resolve/{version.revision}/{file_obj.path}', 'filename': Path(file_obj.path).name, 'size': file_obj.size_bytes})
    return Response({'parquet_files': items})


@api_view(['GET'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_list_models(request):
    search = (request.query_params.get('search') or '').strip().lower()
    limit = min(_int_param(request.query_params.get('limit'), 100, 1), 200)
    items = []
    for repo in _visible_queryset(request, ModelRepo.objects.all()).order_by('repo_id'):
        if search and search not in repo.repo_id.lower() and search not in repo.name.lower():
            continue
        items.append({'id': repo.repo_id, 'name': repo.name, 'author': repo.author, 'pipeline_tag': repo.pipeline_tag, 'downloads': repo.downloads, 'likes': repo.likes, 'private': repo.visibility != 'public', 'tags': repo.tags, 'library_name': repo.library, 'description': repo.description})
    return Response(items[:limit])


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_model_metadata(request, repo_id):
    repo = _get_model_repo(repo_id)
    if not repo:
        return Response({'error': f'Model {repo_id} not found'}, status=404)
    if not can_read_repo(request, repo):
        return Response({'error': f'Model {repo_id} is private'}, status=403)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    version = _get_model_version(repo, request.query_params.get('revision', ''))
    if not version:
        return Response({'error': 'Model version not found'}, status=404)

    payload = _model_summary(repo)
    payload.update({'sha': version.commit_sha, 'siblings': [{'rfilename': file_obj.path, 'size': file_obj.size_bytes} for file_obj in version.files.all()], 'cardData': repo.card_sections})
    return Response(payload)


@api_view(['GET', 'HEAD'])
@authentication_classes(AUTH_CLASSES)
@permission_classes([AllowAny])
def hf_model_resolve_file(request, repo_id, revision, file_path):
    repo = _get_model_repo(repo_id)
    if not repo:
        return HttpResponse('Model not found', status=404)
    if not can_read_repo(request, repo):
        return HttpResponse('Model is private', status=403)
    version = _get_model_version(repo, revision)
    if not version:
        return HttpResponse('Model version not found', status=404)
    file_obj = version.files.filter(path=_normalize_path(file_path)).first()
    if not file_obj:
        return HttpResponse('File not found', status=404)
    if request.method == 'HEAD':
        return HttpResponse(status=200)
    return _file_response('models', version, file_obj)
