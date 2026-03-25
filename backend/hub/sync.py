import csv
import hashlib
import io
import json
import shutil
import subprocess
from pathlib import Path

from django.conf import settings
from django.db import transaction

from .models import (
    DatasetFile,
    DatasetRepo,
    DatasetVersion,
    KnowledgeFile,
    KnowledgeRepo,
    KnowledgeVersion,
    ModelFile,
    ModelRepo,
    ModelVersion,
)


REPO_TYPES = {
    'datasets': {
        'repo_model': DatasetRepo,
        'version_model': DatasetVersion,
        'file_model': DatasetFile,
        'storage_key': 'datasets',
    },
    'models': {
        'repo_model': ModelRepo,
        'version_model': ModelVersion,
        'file_model': ModelFile,
        'storage_key': 'models',
    },
    'knowledge-bases': {
        'repo_model': KnowledgeRepo,
        'version_model': KnowledgeVersion,
        'file_model': KnowledgeFile,
        'storage_key': 'knowledge-bases',
    },
}

TEXT_PREVIEW_TYPES = {
    'cfg',
    'csv',
    'json',
    'jsonl',
    'md',
    'py',
    'js',
    'ts',
    'toml',
    'tsv',
    'txt',
    'yaml',
    'yml',
}

PREVIEW_ROW_LIMIT = 20
PREVIEW_TEXT_LIMIT = 4000


def _normalize_binding(binding, state='ready', error_message=''):
    payload = dict(binding or {})
    payload['state'] = state
    if error_message:
        payload['errorMessage'] = error_message
    else:
        payload.pop('errorMessage', None)
    return payload


def _derive_sync_status(bindings):
    items = [value for value in (bindings or {}).values() if isinstance(value, dict)]
    if not items:
        return 'local'
    states = {item.get('state', 'ready') for item in items}
    if states == {'ready'}:
        return 'synced'
    if 'ready' in states:
        return 'partial'
    if states == {'disabled'}:
        return 'local'
    return 'error'


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


def _file_type_from_path(path):
    suffix = Path(path or '').suffix.lower().lstrip('.')
    return suffix or 'text'


def _decode_file_content(item):
    if 'raw_bytes' in item:
        return item.get('raw_bytes') or b''
    content = item.get('content')
    if content is None:
        return b''
    encoding = (item.get('encoding') or 'utf-8').lower()
    if encoding == 'base64':
        import base64

        return base64.b64decode(content)
    return str(content).encode('utf-8')


def _stored_file_path(repo_type, repo_id, revision, file_path):
    namespace, slug = repo_id.split('/', 1) if '/' in repo_id else ('default', repo_id)
    return Path(settings.MEDIA_ROOT) / 'hub' / repo_type / namespace / slug / revision / _normalize_path(file_path)


def _write_file_to_storage(repo_type, repo_id, revision, path, raw_bytes):
    target = _stored_file_path(repo_type, repo_id, revision, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw_bytes)
    return target


def _revision_storage_root(repo_type, repo_id, revision):
    namespace, slug = repo_id.split('/', 1) if '/' in repo_id else ('default', repo_id)
    return Path(settings.MEDIA_ROOT) / 'hub' / repo_type / namespace / slug / revision


def _normalize_row(value):
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        return {'items': value}
    return {'value': value}


def _safe_json_loads(text, fallback=None):
    try:
        return json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError):
        return fallback


def _infer_split(path):
    normalized = f'/{path.lower().strip("/")}/'
    split_markers = {
        'train': 'train',
        'validation': 'validation',
        'valid': 'validation',
        'val': 'validation',
        'dev': 'validation',
        'test': 'test',
    }
    for marker, split_name in split_markers.items():
        patterns = [
            f'/{marker}/',
            f'/{marker}.',
            f'/{marker}_',
            f'/{marker}-',
            f'_{marker}.',
            f'_{marker}_',
            f'_{marker}-',
            f'-{marker}.',
            f'-{marker}_',
            f'-{marker}-',
        ]
        if any(pattern in normalized for pattern in patterns):
            return split_name
    return ''


def _preview_payload(file_type, raw_bytes):
    preview_text = ''
    preview_rows = []
    row_count = None
    if file_type not in TEXT_PREVIEW_TYPES:
        return preview_text, preview_rows, row_count

    text = raw_bytes.decode('utf-8', errors='replace')
    preview_text = text[:PREVIEW_TEXT_LIMIT]

    if file_type == 'jsonl':
        rows = []
        total = 0
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            total += 1
            if len(rows) < PREVIEW_ROW_LIMIT:
                rows.append(_normalize_row(_safe_json_loads(line, fallback=line)))
        return preview_text, rows, total

    if file_type == 'json':
        data = _safe_json_loads(text)
        if isinstance(data, list):
            return preview_text, [_normalize_row(item) for item in data[:PREVIEW_ROW_LIMIT]], len(data)
        return preview_text, [], row_count

    if file_type in {'csv', 'tsv'}:
        delimiter = '\t' if file_type == 'tsv' else ','
        rows = []
        total = 0
        try:
            reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
            for row in reader:
                total += 1
                if len(rows) < PREVIEW_ROW_LIMIT:
                    rows.append({key: value for key, value in row.items()})
        except csv.Error:
            return preview_text, [], row_count
        return preview_text, rows, total

    return preview_text, preview_rows, row_count


def prepare_sync_file_payloads(repo_type, files):
    prepared = []
    for item in files or []:
        path = _normalize_path(item.get('path'))
        if not path:
            continue
        raw_bytes = _decode_file_content(item)
        file_type = item.get('fileType') or item.get('file_type') or _file_type_from_path(path)
        preview_text = item.get('previewText') or item.get('preview_text') or ''
        preview_rows = item.get('previewRows') or item.get('preview_rows') or []
        row_count = item.get('rowCount')
        if row_count is None:
            row_count = item.get('rows')

        if raw_bytes and (not preview_text or not preview_rows or row_count is None):
            inferred_text, inferred_rows, inferred_row_count = _preview_payload(file_type, raw_bytes)
            if not preview_text:
                preview_text = inferred_text
            if not preview_rows:
                preview_rows = inferred_rows
            if row_count is None:
                row_count = inferred_row_count

        payload = {
            'path': path,
            'raw_bytes': raw_bytes,
            'fileType': file_type,
            'sizeBytes': int(item.get('sizeBytes') or item.get('size_bytes') or len(raw_bytes)),
            'size': item.get('size') or _size_label(len(raw_bytes)),
            'sha256': item.get('sha256') or hashlib.sha256(raw_bytes).hexdigest(),
            'previewText': preview_text,
            'previewRows': preview_rows,
        }
        if row_count is not None:
            payload['rowCount'] = int(row_count)
        if repo_type == 'datasets':
            payload['split'] = item.get('split') or _infer_split(path)
        prepared.append(payload)
    return prepared


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
        size_bytes = int(item.get('sizeBytes') or item.get('size_bytes') or len(raw_bytes))
        sha256 = item.get('sha256') or hashlib.sha256(raw_bytes).hexdigest()

        _write_file_to_storage(repo_type, repo_id, revision_name, path, raw_bytes)

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
            kwargs['row_count'] = int(row_count or 0)
            kwargs['preview_rows'] = preview_rows
            total_rows += int(row_count or 0)

        total_size += size_bytes
        created.append(file_model.objects.create(**kwargs))

    return created, total_size, total_rows


def sync_repo_revision(
    repo_type,
    repo,
    revision,
    commit_sha,
    files,
    *,
    provider_name,
    artifact_uri='',
    provider_binding=None,
    provider_payload=None,
    mark_latest=None,
):
    config = REPO_TYPES[repo_type]
    version_model = config['version_model']
    file_model = config['file_model']
    prepared_files = prepare_sync_file_payloads(repo_type, files)

    with transaction.atomic():
        version_defaults = {
            'commit_sha': commit_sha,
            'provider_revision': revision,
            'provider_commit': commit_sha,
            'artifact_uri': artifact_uri or '',
            'provider_payload': {},
            'is_latest': False,
        }
        if repo_type == 'datasets':
            version_defaults.update({'manifest': {}, 'row_count': 0, 'size_label': '0B'})
        elif repo_type == 'knowledge-bases':
            version_defaults.update({'manifest': {}})
        elif repo_type == 'models':
            version_defaults.update({'framework': getattr(repo, 'library', '') or 'transformers'})

        version, _ = version_model.objects.get_or_create(repo=repo, revision=revision, defaults=version_defaults)

        if mark_latest is None:
            mark_latest = revision == (getattr(repo, 'default_revision', '') or 'main')
            if not mark_latest:
                mark_latest = not repo.versions.exclude(pk=version.pk).filter(is_latest=True).exists()
        if mark_latest:
            repo.versions.exclude(pk=version.pk).update(is_latest=False)

        version.commit_sha = commit_sha
        version.provider_revision = revision
        version.provider_commit = commit_sha
        version.artifact_uri = artifact_uri or getattr(version, 'artifact_uri', '')
        version.is_latest = bool(mark_latest)
        version.provider_payload = dict(version.provider_payload or {})
        version.provider_payload[provider_name] = dict(provider_payload or {})

        if hasattr(version, 'manifest'):
            manifest = dict(version.manifest or {})
            manifest.update(
                {
                    'provider': provider_name,
                    'commitSha': commit_sha,
                    'fileCount': len(prepared_files),
                }
            )
            version.manifest = manifest
        if hasattr(version, 'framework') and not getattr(version, 'framework', ''):
            version.framework = getattr(repo, 'library', '') or 'transformers'
        version.save()

        storage_root = _revision_storage_root(repo_type, repo.repo_id, revision)
        if storage_root.exists():
            shutil.rmtree(storage_root)
        file_model.objects.filter(version=version).delete()

        created_files, total_size, total_rows = _save_revision_files(
            config['storage_key'],
            repo.repo_id,
            revision,
            file_model,
            version,
            prepared_files,
        )

        version_update_fields = ['commit_sha', 'provider_revision', 'provider_commit', 'artifact_uri', 'provider_payload', 'is_latest', 'updated_at']
        if hasattr(version, 'manifest'):
            version_update_fields.append('manifest')
        if repo_type == 'datasets':
            version.row_count = total_rows
            version.size_label = _size_label(total_size)
            version_update_fields.extend(['row_count', 'size_label'])
        elif repo_type == 'models' and hasattr(version, 'framework'):
            version_update_fields.append('framework')
        version.save(update_fields=list(dict.fromkeys(version_update_fields)))

        bindings = dict(repo.provider_bindings or {})
        if provider_binding:
            bindings[provider_name] = _normalize_binding(provider_binding)
            repo.provider_bindings = bindings
            repo.sync_status = _derive_sync_status(bindings)

        repo_update_fields = ['updated_at']
        if provider_binding:
            repo_update_fields.extend(['provider_bindings', 'sync_status'])
        if not getattr(repo, 'default_revision', ''):
            repo.default_revision = revision
            repo_update_fields.append('default_revision')
        if version.is_latest:
            repo.default_revision = revision
            if 'default_revision' not in repo_update_fields:
                repo_update_fields.append('default_revision')
        if repo_type == 'datasets' and version.is_latest:
            repo.row_count = total_rows
            repo.size_label = _size_label(total_size)
            repo_update_fields.extend(['row_count', 'size_label'])
        elif repo_type == 'knowledge-bases':
            repo.file_count = len(created_files)
            repo.document_count = total_rows or len(created_files)
            repo_update_fields.extend(['file_count', 'document_count'])
            if version.is_latest:
                repo.status = 'ready'
                repo_update_fields.append('status')
        repo.save(update_fields=list(dict.fromkeys(repo_update_fields)))

    return {
        'repo': repo,
        'version': version,
        'files': created_files,
        'preparedFiles': prepared_files,
    }


def revision_from_ref(refname):
    prefix = 'refs/heads/'
    if not str(refname or '').startswith(prefix):
        return ''
    return str(refname)[len(prefix):].strip()


def _run_git_dir(git_dir, *args, text=False):
    command = ['git', f'--git-dir={git_dir}', *args]
    result = subprocess.run(command, capture_output=True, text=text, check=False)
    if result.returncode != 0:
        stderr = result.stderr.decode('utf-8', errors='replace') if isinstance(result.stderr, bytes) else (result.stderr or '')
        stdout = result.stdout.decode('utf-8', errors='replace') if isinstance(result.stdout, bytes) else (result.stdout or '')
        raise RuntimeError((stderr or stdout or f'git {" ".join(args)} failed').strip())
    return result.stdout or ('' if text else b'')


def export_bare_git_revision(git_dir, revision):
    refname = f'refs/heads/{revision}'
    commit_sha = _run_git_dir(git_dir, 'rev-parse', refname, text=True).strip()
    paths_output = _run_git_dir(git_dir, 'ls-tree', '-r', '--name-only', '-z', commit_sha)
    paths = [item.decode('utf-8', errors='surrogateescape') for item in paths_output.split(b'\0') if item]
    files = []
    for path in paths:
        raw_bytes = _run_git_dir(git_dir, 'show', f'{commit_sha}:{path}')
        files.append({'path': path, 'raw_bytes': raw_bytes})
    return {
        'revision': revision,
        'commitSha': commit_sha,
        'files': files,
        'refname': refname,
    }
