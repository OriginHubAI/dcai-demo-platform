import base64
import copy
import hashlib
import hmac
import mimetypes
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote, urlparse

import httpx
from django.conf import settings

from .sync import export_bare_git_revision


PLACEHOLDER_VALUES = {
    '',
    'your-api-key',
    'change-me',
    'changeme',
    'replace-me',
}


class HubProviderSyncError(RuntimeError):
    pass


def _trimmed(value, default=''):
    return str(value or default).strip()


def _is_placeholder(value):
    return _trimmed(value).lower() in PLACEHOLDER_VALUES


def _quote_path(path):
    return quote(str(path).strip('/'), safe='/')


def _repo_slug(repo_id):
    return _trimmed(repo_id).replace('/', '--')


def _stored_file_path(repo_type, repo_id, revision, file_path):
    namespace, slug = repo_id.split('/', 1) if '/' in repo_id else ('default', repo_id)
    return Path(settings.MEDIA_ROOT) / 'hub' / repo_type / namespace / slug / revision / str(file_path).strip('/')


def _materialize_revision_files(repo_type, repo_id, revision, files):
    items = []
    for file_obj in files:
        stored_path = _stored_file_path(repo_type, repo_id, revision, file_obj.path)
        if not stored_path.exists():
            continue
        items.append(
            {
                'path': file_obj.path,
                'fileType': getattr(file_obj, 'file_type', ''),
                'sizeBytes': getattr(file_obj, 'size_bytes', stored_path.stat().st_size),
                'raw_bytes': stored_path.read_bytes(),
            }
        )
    return items


def _raw_bytes_from_payload(item):
    if item is None:
        return b''
    if 'raw_bytes' in item:
        return item['raw_bytes'] or b''
    content = item.get('content')
    if content is None:
        return b''
    if _trimmed(item.get('encoding'), 'utf-8').lower() == 'base64':
        return base64.b64decode(content)
    return str(content).encode('utf-8')


def _content_base64(item):
    return base64.b64encode(_raw_bytes_from_payload(item)).decode('ascii')


def _normalize_binding(binding, state='ready', error_message=''):
    payload = dict(binding or {})
    payload['state'] = state
    if error_message:
        payload['errorMessage'] = error_message
    elif 'errorMessage' in payload:
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
    if 'disabled' in states and len(states) == 1:
        return 'local'
    return 'error'


def _local_git_remote_root():
    return Path(getattr(settings, 'LOCAL_GIT_REMOTE_ROOT', '') or '')


def _local_git_repo_path(repo_type, namespace, slug):
    return _local_git_remote_root() / repo_type / namespace / f'{slug}.git'


class BaseHubClient:
    def __init__(self, base_url, timeout=30):
        self.base_url = _trimmed(base_url).rstrip('/')
        self.timeout = timeout

    @property
    def configured(self):
        return bool(self.base_url)

    def _trust_env(self):
        host = (urlparse(self.base_url).hostname or '').lower()
        return host not in {'localhost', '127.0.0.1', '::1'}

    def _request(self, method, path, *, headers=None, params=None, json=None, files=None, auth=None):
        if not self.configured:
            raise HubProviderSyncError('Provider is not configured')
        with httpx.Client(timeout=self.timeout, trust_env=self._trust_env()) as client:
            response = client.request(
                method,
                f'{self.base_url}{path}',
                headers=headers,
                params=params,
                json=json,
                files=files,
                auth=auth,
            )
        if response.status_code >= 400:
            detail = ''
            try:
                payload = response.json()
                detail = payload.get('message') or payload.get('error') or payload.get('msg') or ''
            except Exception:
                detail = response.text.strip()
            raise HubProviderSyncError(detail or f'{method} {path} failed with HTTP {response.status_code}')
        if not response.content:
            return {}
        try:
            return response.json()
        except Exception:
            return {'raw': response.text}


class GiteaHubClient(BaseHubClient):
    def __init__(self):
        super().__init__(getattr(settings, 'GITEA_BASE_URL', ''), getattr(settings, 'GITEA_TIMEOUT', 30))
        self.token = _trimmed(getattr(settings, 'GITEA_TOKEN', ''))
        self.org = _trimmed(getattr(settings, 'GITEA_ORG', ''))

    @property
    def configured(self):
        return super().configured and not _is_placeholder(self.token)

    def _headers(self):
        return {'Authorization': f'token {self.token}', 'Content-Type': 'application/json'}

    def create_repo(self, namespace, slug, description, private=False, default_branch='main'):
        owner = self.org or _trimmed(namespace)
        payload = {
            'name': slug,
            'description': description,
            'private': bool(private),
            'auto_init': True,
            'default_branch': default_branch or 'main',
        }
        if self.org:
            response = self._request('POST', f'/api/v1/orgs/{quote(owner)}/repos', headers=self._headers(), json=payload)
        else:
            response = self._request('POST', '/api/v1/user/repos', headers=self._headers(), json=payload)
        return {
            'provider': 'gitea',
            'owner': response.get('owner', {}).get('login') or owner,
            'name': response.get('name') or slug,
            'fullName': response.get('full_name') or f'{owner}/{slug}',
            'cloneUrl': response.get('clone_url') or '',
            'sshUrl': response.get('ssh_url') or '',
            'htmlUrl': response.get('html_url') or response.get('website') or '',
            'defaultBranch': response.get('default_branch') or default_branch or 'main',
            'private': response.get('private', bool(private)),
        }

    def publish_revision(self, binding, revision, files, *, default_branch='main', message='Publish revision'):
        owner = binding.get('owner')
        repo_name = binding.get('name')
        branch = revision or binding.get('defaultBranch') or default_branch or 'main'
        base_branch = binding.get('defaultBranch') or default_branch or 'main'
        last_commit = ''
        first_request = branch != base_branch
        for item in files:
            path = _trimmed(item.get('path'))
            if not path:
                continue
            payload = {
                'content': _content_base64(item),
                'message': f'{message}: {path}',
            }
            if first_request:
                payload['branch'] = base_branch
                payload['new_branch'] = branch
                first_request = False
            else:
                payload['branch'] = branch
            response = self._request(
                'POST',
                f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/contents/{_quote_path(path)}',
                headers=self._headers(),
                json=payload,
            )
            commit = response.get('commit') or {}
            last_commit = commit.get('sha') or last_commit
        html_url = _trimmed(binding.get('htmlUrl'))
        return {
            'branch': branch,
            'commitSha': last_commit,
            'treeUrl': f'{html_url}/src/branch/{quote(branch)}' if html_url and branch else html_url,
        }

    def ensure_push_webhook(self, binding, repo_type, repo_id):
        webhook_base_url = _trimmed(getattr(settings, 'GITEA_WEBHOOK_BASE_URL', '') or getattr(settings, 'DCAI_WEBHOOK_BASE_URL', ''))
        if not webhook_base_url:
            return {}
        owner = binding.get('owner')
        repo_name = binding.get('name')
        secret = _trimmed(getattr(settings, 'GITEA_WEBHOOK_SECRET', ''))
        target_url = f"{webhook_base_url.rstrip('/')}/api/v2/integrations/gitea/webhook"
        authorization_header = _trimmed(getattr(settings, 'GITEA_WEBHOOK_AUTHORIZATION_HEADER', ''))
        desired_events = ['push']
        desired_branch_filter = '*'
        payload = {
            'type': 'gitea',
            'config': {
                'content_type': 'json',
                'url': target_url,
            },
            'events': desired_events,
            'branch_filter': desired_branch_filter,
            'active': True,
        }
        if secret:
            payload['config']['secret'] = secret
        if authorization_header:
            payload['authorization_header'] = authorization_header

        hooks = self._request('GET', f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/hooks', headers=self._headers())
        existing = None
        for hook in hooks if isinstance(hooks, list) else []:
            config = hook.get('config') or {}
            if _trimmed(config.get('url')) == target_url:
                existing = hook
                break

        if existing:
            existing_config = existing.get('config') or {}
            existing_events = sorted(_trimmed(item) for item in (existing.get('events') or []) if _trimmed(item))
            needs_update = any(
                [
                    _trimmed(existing_config.get('content_type'), 'json') != 'json',
                    _trimmed(existing.get('branch_filter')) != desired_branch_filter,
                    bool(existing.get('active', False)) is not True,
                    existing_events != sorted(desired_events),
                    _trimmed(existing.get('authorization_header')) != authorization_header,
                ]
            )
            if needs_update:
                existing = self._request(
                    'PATCH',
                    f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/hooks/{existing.get("id")}',
                    headers=self._headers(),
                    json=payload,
                )
            return {
                'webhookId': existing.get('id'),
                'webhookUrl': target_url,
                'webhookSecret': bool(secret),
            }

        response = self._request(
            'POST',
            f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/hooks',
            headers=self._headers(),
            json=payload,
        )
        return {
            'webhookId': response.get('id'),
            'webhookUrl': target_url,
            'webhookSecret': bool(secret),
        }

    def export_revision(self, binding, revision=''):
        owner = binding.get('owner')
        repo_name = binding.get('name')
        branch = revision or binding.get('defaultBranch') or 'main'
        branch_payload = self._request(
            'GET',
            f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/branches/{quote(branch)}',
            headers=self._headers(),
        )
        commit_payload = branch_payload.get('commit') or {}
        commit_sha = (
            commit_payload.get('id')
            or commit_payload.get('sha')
            or ((commit_payload.get('commit') or {}).get('id'))
            or ((commit_payload.get('commit') or {}).get('sha'))
            or ''
        )
        if not commit_sha:
            raise HubProviderSyncError(f'Unable to resolve head commit for branch {branch}')

        tree_payload = self._request(
            'GET',
            f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/git/trees/{quote(commit_sha)}',
            headers=self._headers(),
            params={'recursive': 'true'},
        )
        tree = tree_payload.get('tree') or []
        files = []
        for item in tree:
            if item.get('type') != 'blob':
                continue
            path = _trimmed(item.get('path'))
            if not path:
                continue
            content_payload = self._request(
                'GET',
                f'/api/v1/repos/{quote(owner)}/{quote(repo_name)}/contents/{_quote_path(path)}',
                headers=self._headers(),
                params={'ref': branch},
            )
            content = content_payload.get('content')
            encoding = _trimmed(content_payload.get('encoding'), 'base64').lower()
            if content is not None and encoding == 'base64':
                raw_bytes = base64.b64decode(content)
            elif content is not None:
                raw_bytes = str(content).encode('utf-8')
            else:
                download_url = _trimmed(content_payload.get('download_url'))
                if not download_url:
                    raise HubProviderSyncError(f'Unable to read repository file: {path}')
                with httpx.Client(timeout=self.timeout, trust_env=self._trust_env()) as client:
                    response = client.get(download_url, headers={'Authorization': self._headers()['Authorization']})
                if response.status_code >= 400:
                    raise HubProviderSyncError(f'Unable to download repository file: {path}')
                raw_bytes = response.content
            files.append({'path': path, 'raw_bytes': raw_bytes})

        html_url = _trimmed(binding.get('htmlUrl'))
        return {
            'branch': branch,
            'commitSha': commit_sha,
            'treeUrl': f'{html_url}/src/branch/{quote(branch)}' if html_url else '',
            'artifactUri': f'{html_url}/src/branch/{quote(branch)}' if html_url else '',
            'files': files,
        }


class LocalGitHubClient:
    def __init__(self):
        self.enabled = bool(getattr(settings, 'LOCAL_GIT_REMOTE_ENABLED', False))
        self.root = _local_git_remote_root()
        self.git_binary = shutil.which('git') or ''

    @property
    def configured(self):
        return self.enabled and bool(self.git_binary)

    def create_repo(self, repo_type, namespace, slug, repo_id, description='', private=False, default_branch='main'):
        if not self.configured:
            raise HubProviderSyncError('Local git remote is not configured')
        target = _local_git_repo_path(repo_type, namespace, slug)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            self._run('init', '--bare', '--initial-branch', default_branch or 'main', str(target))
        self._write_post_receive_hook(target, repo_type, repo_id)
        return {
            'provider': 'localgit',
            'repoType': repo_type,
            'cloneUrl': str(target),
            'pushUrl': str(target),
            'localPath': str(target),
            'defaultBranch': default_branch or 'main',
            'private': bool(private),
            'description': description,
        }

    def publish_revision(self, binding, revision, files, *, message='Publish revision'):
        if not self.configured:
            raise HubProviderSyncError('Local git remote is not configured')
        remote_path = _trimmed(binding.get('localPath') or binding.get('cloneUrl'))
        if not remote_path:
            raise HubProviderSyncError('Local git remote path is missing')
        branch = revision or binding.get('defaultBranch') or 'main'
        with tempfile.TemporaryDirectory(prefix='dcai-localgit-publish-') as temp_dir:
            self._run('clone', remote_path, temp_dir)
            branch_exists = self._git(['-C', temp_dir, 'show-ref', '--verify', '--quiet', f'refs/heads/{branch}'], check=False).returncode == 0
            if branch_exists:
                self._run('-C', temp_dir, 'checkout', branch)
            else:
                checkout = self._git(['-C', temp_dir, 'checkout', '--orphan', branch], check=False)
                if checkout.returncode != 0:
                    self._run('-C', temp_dir, 'checkout', '-b', branch)
            self._git(['-C', temp_dir, 'rm', '-r', '--ignore-unmatch', '.'], check=False)
            for item in files:
                relative_path = _trimmed(item.get('path'))
                if not relative_path:
                    continue
                target = Path(temp_dir) / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(_raw_bytes_from_payload(item))
            self._run('-C', temp_dir, 'add', '.')
            commit = self._git(
                ['-C', temp_dir, 'commit', '-m', message],
                check=False,
                env={
                    'GIT_AUTHOR_NAME': 'DCAI',
                    'GIT_AUTHOR_EMAIL': 'dcai-localgit@example.com',
                    'GIT_COMMITTER_NAME': 'DCAI',
                    'GIT_COMMITTER_EMAIL': 'dcai-localgit@example.com',
                },
            )
            if commit.returncode != 0 and 'nothing to commit' not in (commit.stderr or '').lower():
                raise HubProviderSyncError((commit.stderr or commit.stdout or '').strip() or 'git commit failed')
            self._run('-C', temp_dir, 'push', 'origin', f'HEAD:{branch}')
            commit_sha = self._run('-C', temp_dir, 'rev-parse', 'HEAD').stdout.strip()
        return {
            'branch': branch,
            'commitSha': commit_sha,
            'treeUrl': remote_path,
        }

    def export_revision(self, binding, revision=''):
        if not self.configured:
            raise HubProviderSyncError('Local git remote is not configured')
        remote_path = _trimmed(binding.get('localPath') or binding.get('cloneUrl'))
        if not remote_path:
            raise HubProviderSyncError('Local git remote path is missing')
        branch = revision or binding.get('defaultBranch') or 'main'
        exported = export_bare_git_revision(remote_path, branch)
        return {
            'branch': branch,
            'commitSha': exported['commitSha'],
            'treeUrl': remote_path,
            'artifactUri': remote_path,
            'files': exported['files'],
        }

    def _write_post_receive_hook(self, repo_path, repo_type, repo_id):
        hooks_dir = Path(repo_path) / 'hooks'
        hooks_dir.mkdir(parents=True, exist_ok=True)
        hook_path = hooks_dir / 'post-receive'
        log_dir = self.root / '_logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        backend_dir = Path(settings.BASE_DIR)
        python_bin = backend_dir / '.venv' / 'bin' / 'python'
        log_file = log_dir / f"{repo_type}-{_repo_slug(repo_id)}.log"
        script = f"""#!/usr/bin/env bash
set -euo pipefail
while read -r oldrev newrev refname; do
  if [[ -z "${{newrev}}" || "${{newrev}}" =~ ^0+$ ]]; then
    continue
  fi
  "{python_bin}" "{backend_dir / 'manage.py'}" sync_local_git_repo --repo-type "{repo_type}" --repo-id "{repo_id}" --git-dir "{repo_path}" --refname "${{refname}}" >> "{log_file}" 2>&1 || true
done
"""
        hook_path.write_text(script, encoding='utf-8')
        os.chmod(hook_path, 0o755)

    def _run(self, *args, env=None):
        result = self._git(list(args), env=env)
        if result.returncode != 0:
            raise HubProviderSyncError((result.stderr or result.stdout or '').strip() or f'git {" ".join(args)} failed')
        return result

    def _git(self, args, *, check=True, env=None):
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            [self.git_binary, *args],
            capture_output=True,
            text=True,
            env=merged_env,
            check=False,
        )


class LakeFSHubClient(BaseHubClient):
    def __init__(self):
        super().__init__(getattr(settings, 'LAKEFS_ENDPOINT', ''), getattr(settings, 'LAKEFS_TIMEOUT', 30))
        self.access_key = _trimmed(getattr(settings, 'LAKEFS_ACCESS_KEY', ''))
        self.secret_key = _trimmed(getattr(settings, 'LAKEFS_SECRET_KEY', ''))
        self.storage_namespace_prefix = _trimmed(getattr(settings, 'LAKEFS_STORAGE_NAMESPACE_PREFIX', ''))

    @property
    def configured(self):
        return (
            super().configured
            and not _is_placeholder(self.access_key)
            and not _is_placeholder(self.secret_key)
            and bool(self.storage_namespace_prefix)
        )

    def _auth(self):
        return (self.access_key, self.secret_key)

    def create_repository(self, repo_id, default_branch='main'):
        repo_name = _repo_slug(repo_id)
        storage_namespace = f'{self.storage_namespace_prefix.rstrip("/")}/{repo_name}/'
        payload = {
            'name': repo_name,
            'storage_namespace': storage_namespace,
            'default_branch': default_branch or 'main',
        }
        response = self._request('POST', '/api/v1/repositories', json=payload, auth=self._auth())
        return {
            'provider': 'lakefs',
            'repository': response.get('id') or response.get('name') or repo_name,
            'defaultBranch': response.get('default_branch') or default_branch or 'main',
            'storageNamespace': response.get('storage_namespace') or storage_namespace,
            'endpoint': self.base_url,
        }

    def ensure_branch(self, repository, branch, source):
        try:
            self._request('GET', f'/api/v1/repositories/{quote(repository)}/branches/{quote(branch)}', auth=self._auth())
            return branch
        except HubProviderSyncError:
            payload = {'name': branch, 'source': source}
            self._request('POST', f'/api/v1/repositories/{quote(repository)}/branches', json=payload, auth=self._auth())
            return branch

    def commit(self, repository, branch, message, metadata=None):
        payload = {'message': message, 'metadata': metadata or {}, 'allow_empty': True}
        response = self._request(
            'POST',
            f'/api/v1/repositories/{quote(repository)}/branches/{quote(branch)}/commits',
            json=payload,
            auth=self._auth(),
        )
        return {
            'commitId': response.get('id') or response.get('commit_id') or response.get('reference', ''),
            'branch': branch,
        }


class MLflowHubClient(BaseHubClient):
    def __init__(self):
        base_url = _trimmed(getattr(settings, 'MLFLOW_REGISTRY_URI', '') or getattr(settings, 'MLFLOW_TRACKING_URI', ''))
        super().__init__(base_url, getattr(settings, 'MLFLOW_TIMEOUT', 30))
        self.token = _trimmed(getattr(settings, 'MLFLOW_TRACKING_TOKEN', ''))
        self.username = _trimmed(getattr(settings, 'MLFLOW_TRACKING_USERNAME', ''))
        self.password = _trimmed(getattr(settings, 'MLFLOW_TRACKING_PASSWORD', ''))

    def _headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token and not _is_placeholder(self.token):
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def _auth(self):
        if self.username and self.password:
            return (self.username, self.password)
        return None

    def _api_path(self, path):
        return f'/api/2.0/mlflow{path}'

    def create_registered_model(self, name, description='', tags=None):
        payload = {'name': name, 'description': description, 'tags': tags or []}
        response = self._request('POST', self._api_path('/registered-models/create'), headers=self._headers(), json=payload, auth=self._auth())
        model = response.get('registered_model') or {}
        return {
            'provider': 'mlflow',
            'modelName': model.get('name') or name,
            'description': model.get('description') or description,
        }

    def create_model_version(self, name, source, description='', run_id='', tags=None, stage=''):
        payload = {
            'name': name,
            'source': source,
            'description': description,
            'run_id': run_id or '',
            'tags': tags or [],
        }
        response = self._request('POST', self._api_path('/model-versions/create'), headers=self._headers(), json=payload, auth=self._auth())
        version = response.get('model_version') or {}
        created = {
            'version': str(version.get('version') or ''),
            'source': version.get('source') or source,
            'status': version.get('status') or '',
            'currentStage': version.get('current_stage') or '',
        }
        if stage:
            transition_payload = {'name': name, 'version': created['version'], 'stage': stage, 'archive_existing_versions': False}
            transition = self._request(
                'POST',
                self._api_path('/model-versions/transition-stage'),
                headers=self._headers(),
                json=transition_payload,
                auth=self._auth(),
            )
            transitioned = transition.get('model_version') or {}
            created['currentStage'] = transitioned.get('current_stage') or stage
        return created


class RAGFlowHubClient(BaseHubClient):
    def __init__(self):
        super().__init__(getattr(settings, 'RAGFLOW_BASE_URL', ''), getattr(settings, 'RAGFLOW_TIMEOUT', 60))
        self.api_key = _trimmed(getattr(settings, 'RAGFLOW_API_KEY', ''))

    @property
    def configured(self):
        return super().configured and not _is_placeholder(self.api_key)

    def _headers(self):
        return {'Authorization': f'Bearer {self.api_key}'}

    def _data(self, response):
        if response.get('code') not in (None, 0):
            raise HubProviderSyncError(response.get('message') or 'RAGFlow request failed')
        return response.get('data')

    def create_dataset(self, name, description='', chunk_method='naive'):
        payload = {
            'name': name,
            'description': description,
            'permission': 'team',
            'chunk_method': chunk_method or 'naive',
        }
        response = self._request('POST', '/api/v1/datasets', headers=self._headers(), json=payload)
        dataset = self._data(response) or {}
        return {
            'provider': 'ragflow',
            'datasetId': dataset.get('id') or dataset.get('dataset_id') or dataset.get('kb_id') or '',
            'name': dataset.get('name') or name,
        }

    def upload_documents(self, dataset_id, files):
        if not files:
            return []
        multipart = []
        for item in files:
            raw_bytes = _raw_bytes_from_payload(item)
            if not raw_bytes:
                continue
            filename = Path(_trimmed(item.get('path'))).name or 'file.bin'
            mime_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            multipart.append(('file', (filename, raw_bytes, mime_type)))
        if not multipart:
            return []
        response = self._request(
            'POST',
            f'/api/v1/datasets/{quote(dataset_id)}/documents',
            headers={'Authorization': self._headers()['Authorization']},
            files=multipart,
        )
        return self._data(response) or []

    def start_parsing(self, dataset_id, document_ids):
        payload = {'document_ids': document_ids}
        response = self._request(
            'POST',
            f'/api/v1/datasets/{quote(dataset_id)}/chunks',
            headers=self._headers(),
            json=payload,
        )
        return self._data(response) or {}


class HubProviderManager:
    def __init__(self):
        self.gitea = GiteaHubClient()
        self.localgit = LocalGitHubClient()
        self.lakefs = LakeFSHubClient()
        self.mlflow = MLflowHubClient()
        self.ragflow = RAGFlowHubClient()

    def _next_bindings(self, repo):
        return copy.deepcopy(repo.provider_bindings or {})

    def bind_dataset_repo(self, repo):
        bindings = self._next_bindings(repo)
        default_revision = _trimmed(getattr(repo, 'default_revision', ''), 'main')
        if self.localgit.configured:
            try:
                bindings['localgit'] = _normalize_binding(
                    self.localgit.create_repo('datasets', repo.namespace, repo.slug, repo.repo_id, repo.description, repo.visibility != 'public', default_revision)
                )
            except HubProviderSyncError as exc:
                bindings['localgit'] = _normalize_binding(bindings.get('localgit'), state='error', error_message=str(exc))
        if self.gitea.configured:
            try:
                created = self.gitea.create_repo(repo.namespace, repo.slug, repo.description, repo.visibility != 'public', default_revision)
                try:
                    created.update(self.gitea.ensure_push_webhook(created, 'datasets', repo.repo_id))
                except HubProviderSyncError as exc:
                    created['webhookError'] = str(exc)
                bindings['gitea'] = _normalize_binding(created)
            except HubProviderSyncError as exc:
                bindings['gitea'] = _normalize_binding(bindings.get('gitea'), state='error', error_message=str(exc))
        if self.lakefs.configured:
            try:
                bindings['lakefs'] = _normalize_binding(self.lakefs.create_repository(repo.repo_id, default_revision))
            except HubProviderSyncError as exc:
                bindings['lakefs'] = _normalize_binding(bindings.get('lakefs'), state='error', error_message=str(exc))
        return {'provider_bindings': bindings, 'sync_status': _derive_sync_status(bindings), 'default_revision': default_revision}

    def sync_dataset_version(self, repo, version, files):
        bindings = self._next_bindings(repo)
        payload = copy.deepcopy(version.provider_payload or {})
        artifact_uri = version.artifact_uri
        provider_commit = version.provider_commit
        provider_revision = version.provider_revision or version.revision
        localgit_binding = bindings.get('localgit') or {}
        if localgit_binding.get('state') == 'ready' and files:
            try:
                published = self.localgit.publish_revision(
                    localgit_binding,
                    version.revision,
                    files,
                    message=f'Publish dataset revision {version.revision}',
                )
                payload['localgit'] = published
                artifact_uri = artifact_uri or published.get('treeUrl')
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['localgit'] = {'errorMessage': str(exc)}
                bindings['localgit'] = _normalize_binding(localgit_binding, state='error', error_message=str(exc))
        gitea_binding = bindings.get('gitea') or {}
        if gitea_binding.get('state') == 'ready' and files:
            try:
                published = self.gitea.publish_revision(
                    gitea_binding,
                    version.revision,
                    files,
                    default_branch=repo.default_revision,
                    message=f'Publish dataset revision {version.revision}',
                )
                payload['gitea'] = published
                artifact_uri = published.get('treeUrl') or artifact_uri
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['gitea'] = {'errorMessage': str(exc)}
                bindings['gitea'] = _normalize_binding(gitea_binding, state='error', error_message=str(exc))

        lakefs_binding = bindings.get('lakefs') or {}
        if lakefs_binding.get('state') == 'ready':
            try:
                repository = lakefs_binding.get('repository')
                branch = self.lakefs.ensure_branch(repository, version.revision, lakefs_binding.get('defaultBranch') or repo.default_revision)
                commit = self.lakefs.commit(
                    repository,
                    branch,
                    f'Publish dataset revision {version.revision}',
                    metadata={'repo_id': repo.repo_id, 'revision': version.revision},
                )
                payload['lakefs'] = commit
                provider_commit = commit.get('commitId') or provider_commit
                provider_revision = commit.get('branch') or provider_revision
            except HubProviderSyncError as exc:
                payload['lakefs'] = {'errorMessage': str(exc)}
                bindings['lakefs'] = _normalize_binding(lakefs_binding, state='error', error_message=str(exc))
        return {
            'provider_payload': payload,
            'provider_revision': provider_revision,
            'provider_commit': provider_commit,
            'artifact_uri': artifact_uri,
            'repo_provider_bindings': bindings,
            'repo_sync_status': _derive_sync_status(bindings),
        }

    def bind_model_repo(self, repo):
        bindings = self._next_bindings(repo)
        default_revision = _trimmed(getattr(repo, 'default_revision', ''), 'main')
        if self.localgit.configured:
            try:
                bindings['localgit'] = _normalize_binding(
                    self.localgit.create_repo('models', repo.namespace, repo.slug, repo.repo_id, repo.description, repo.visibility != 'public', default_revision)
                )
            except HubProviderSyncError as exc:
                bindings['localgit'] = _normalize_binding(bindings.get('localgit'), state='error', error_message=str(exc))
        if self.gitea.configured:
            try:
                created = self.gitea.create_repo(repo.namespace, repo.slug, repo.description, repo.visibility != 'public', default_revision)
                try:
                    created.update(self.gitea.ensure_push_webhook(created, 'models', repo.repo_id))
                except HubProviderSyncError as exc:
                    created['webhookError'] = str(exc)
                bindings['gitea'] = _normalize_binding(created)
            except HubProviderSyncError as exc:
                bindings['gitea'] = _normalize_binding(bindings.get('gitea'), state='error', error_message=str(exc))
        if self.mlflow.configured:
            try:
                tags = [{'key': 'repo_id', 'value': repo.repo_id}, {'key': 'pipeline_tag', 'value': repo.pipeline_tag}]
                bindings['mlflow'] = _normalize_binding(self.mlflow.create_registered_model(repo.repo_id, repo.description, tags=tags))
            except HubProviderSyncError as exc:
                bindings['mlflow'] = _normalize_binding(bindings.get('mlflow'), state='error', error_message=str(exc))
        return {'provider_bindings': bindings, 'sync_status': _derive_sync_status(bindings), 'default_revision': default_revision}

    def sync_model_version(self, repo, version, files, request_payload):
        bindings = self._next_bindings(repo)
        payload = copy.deepcopy(version.provider_payload or {})
        artifact_uri = _trimmed(request_payload.get('artifactUri') or request_payload.get('artifact_uri') or version.artifact_uri)
        provider_commit = version.provider_commit
        provider_revision = version.provider_revision or version.revision

        localgit_binding = bindings.get('localgit') or {}
        if localgit_binding.get('state') == 'ready' and files:
            try:
                published = self.localgit.publish_revision(
                    localgit_binding,
                    version.revision,
                    files,
                    message=f'Publish model revision {version.revision}',
                )
                payload['localgit'] = published
                artifact_uri = artifact_uri or published.get('treeUrl')
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['localgit'] = {'errorMessage': str(exc)}
                bindings['localgit'] = _normalize_binding(localgit_binding, state='error', error_message=str(exc))

        gitea_binding = bindings.get('gitea') or {}
        if gitea_binding.get('state') == 'ready' and files:
            try:
                published = self.gitea.publish_revision(
                    gitea_binding,
                    version.revision,
                    files,
                    default_branch=repo.default_revision,
                    message=f'Publish model revision {version.revision}',
                )
                payload['gitea'] = published
                artifact_uri = artifact_uri or published.get('treeUrl')
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['gitea'] = {'errorMessage': str(exc)}
                bindings['gitea'] = _normalize_binding(gitea_binding, state='error', error_message=str(exc))

        mlflow_binding = bindings.get('mlflow') or {}
        if mlflow_binding.get('state') == 'ready' and artifact_uri and self.mlflow.configured:
            try:
                created = self.mlflow.create_model_version(
                    mlflow_binding.get('modelName') or repo.repo_id,
                    artifact_uri,
                    description=f'{repo.repo_id}@{version.revision}',
                    tags=[{'key': 'repo_id', 'value': repo.repo_id}, {'key': 'revision', 'value': version.revision}],
                    stage=_trimmed(request_payload.get('stage')),
                )
                payload['mlflow'] = created
                provider_revision = created.get('version') or provider_revision
            except HubProviderSyncError as exc:
                payload['mlflow'] = {'errorMessage': str(exc)}
                bindings['mlflow'] = _normalize_binding(mlflow_binding, state='error', error_message=str(exc))
        return {
            'provider_payload': payload,
            'provider_revision': provider_revision,
            'provider_commit': provider_commit,
            'artifact_uri': artifact_uri,
            'repo_provider_bindings': bindings,
            'repo_sync_status': _derive_sync_status(bindings),
        }

    def bind_knowledge_repo(self, repo):
        bindings = self._next_bindings(repo)
        default_revision = _trimmed(getattr(repo, 'default_revision', ''), 'main')
        if self.localgit.configured:
            try:
                bindings['localgit'] = _normalize_binding(
                    self.localgit.create_repo('knowledge-bases', repo.namespace, repo.slug, repo.repo_id, repo.description, repo.visibility != 'public', default_revision)
                )
            except HubProviderSyncError as exc:
                bindings['localgit'] = _normalize_binding(bindings.get('localgit'), state='error', error_message=str(exc))
        if self.gitea.configured:
            try:
                created = self.gitea.create_repo(repo.namespace, repo.slug, repo.description, repo.visibility != 'public', default_revision)
                try:
                    created.update(self.gitea.ensure_push_webhook(created, 'knowledge-bases', repo.repo_id))
                except HubProviderSyncError as exc:
                    created['webhookError'] = str(exc)
                bindings['gitea'] = _normalize_binding(created)
            except HubProviderSyncError as exc:
                bindings['gitea'] = _normalize_binding(bindings.get('gitea'), state='error', error_message=str(exc))
        if self.ragflow.configured:
            try:
                bindings['ragflow'] = _normalize_binding(self.ragflow.create_dataset(repo.name, repo.description))
            except HubProviderSyncError as exc:
                bindings['ragflow'] = _normalize_binding(bindings.get('ragflow'), state='error', error_message=str(exc))
        return {'provider_bindings': bindings, 'sync_status': _derive_sync_status(bindings), 'default_revision': default_revision}

    def sync_knowledge_version(self, repo, version, files):
        bindings = self._next_bindings(repo)
        payload = copy.deepcopy(version.provider_payload or {})
        artifact_uri = version.artifact_uri
        provider_commit = version.provider_commit

        localgit_binding = bindings.get('localgit') or {}
        if localgit_binding.get('state') == 'ready' and files:
            try:
                published = self.localgit.publish_revision(
                    localgit_binding,
                    version.revision,
                    files,
                    message=f'Publish knowledge revision {version.revision}',
                )
                payload['localgit'] = published
                artifact_uri = artifact_uri or published.get('treeUrl')
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['localgit'] = {'errorMessage': str(exc)}
                bindings['localgit'] = _normalize_binding(localgit_binding, state='error', error_message=str(exc))

        gitea_binding = bindings.get('gitea') or {}
        if gitea_binding.get('state') == 'ready' and files:
            try:
                published = self.gitea.publish_revision(
                    gitea_binding,
                    version.revision,
                    files,
                    default_branch=repo.default_revision,
                    message=f'Publish knowledge revision {version.revision}',
                )
                payload['gitea'] = published
                artifact_uri = published.get('treeUrl') or artifact_uri
                provider_commit = published.get('commitSha') or provider_commit
            except HubProviderSyncError as exc:
                payload['gitea'] = {'errorMessage': str(exc)}
                bindings['gitea'] = _normalize_binding(gitea_binding, state='error', error_message=str(exc))

        ragflow_binding = bindings.get('ragflow') or {}
        if ragflow_binding.get('state') == 'ready' and files:
            try:
                uploaded = self.ragflow.upload_documents(ragflow_binding.get('datasetId'), files)
                payload['ragflow'] = {
                    'datasetId': ragflow_binding.get('datasetId'),
                    'documents': [
                        {
                            'id': item.get('id'),
                            'name': item.get('name'),
                            'run': item.get('run'),
                        }
                        for item in uploaded
                    ],
                }
            except HubProviderSyncError as exc:
                payload['ragflow'] = {'errorMessage': str(exc)}
                bindings['ragflow'] = _normalize_binding(ragflow_binding, state='error', error_message=str(exc))
        return {
            'provider_payload': payload,
            'provider_revision': version.revision,
            'provider_commit': provider_commit,
            'artifact_uri': artifact_uri,
            'repo_provider_bindings': bindings,
            'repo_sync_status': _derive_sync_status(bindings),
        }

    def trigger_knowledge_build(self, repo, build, version, request_payload=None):
        request_payload = request_payload or {}
        bindings = self._next_bindings(repo)
        payload = copy.deepcopy(build.provider_payload or {})
        ragflow_binding = bindings.get('ragflow') or {}
        documents = []
        if version:
            documents = ((version.provider_payload or {}).get('ragflow') or {}).get('documents') or []
        if ragflow_binding.get('state') == 'ready' and version and not documents:
            documents = self._hydrate_ragflow_documents(repo, version, ragflow_binding)
        if ragflow_binding.get('state') == 'ready' and documents:
            document_ids = [item.get('id') for item in documents if item.get('id')]
            try:
                response = self.ragflow.start_parsing(ragflow_binding.get('datasetId'), document_ids)
                payload['ragflow'] = {
                    'datasetId': ragflow_binding.get('datasetId'),
                    'documents': documents,
                    'response': response,
                }
                return {
                    'provider_job_id': f"{ragflow_binding.get('datasetId')}:{build.id}",
                    'provider_status': 'submitted',
                    'provider_payload': payload,
                    'repo_provider_bindings': bindings,
                    'repo_sync_status': _derive_sync_status(bindings),
                }
            except HubProviderSyncError as exc:
                payload['ragflow'] = {'errorMessage': str(exc), 'documents': documents}
                bindings['ragflow'] = _normalize_binding(ragflow_binding, state='error', error_message=str(exc))
        return {
            'provider_job_id': '',
            'provider_status': '',
            'provider_payload': payload,
            'repo_provider_bindings': bindings,
            'repo_sync_status': _derive_sync_status(bindings),
        }

    def pull_dataset_revision(self, repo, revision=''):
        return self._pull_revision('datasets', repo, revision)

    def pull_model_revision(self, repo, revision=''):
        return self._pull_revision('models', repo, revision)

    def pull_knowledge_revision(self, repo, revision=''):
        return self._pull_revision('knowledge-bases', repo, revision)

    def _hydrate_ragflow_documents(self, repo, version, ragflow_binding):
        files = _materialize_revision_files('knowledge-bases', repo.repo_id, version.revision, version.files.all())
        if not files:
            return []
        uploaded = self.ragflow.upload_documents(ragflow_binding.get('datasetId'), files)
        documents = [{'id': item.get('id'), 'name': item.get('name'), 'run': item.get('run')} for item in uploaded]
        version.provider_payload = copy.deepcopy(version.provider_payload or {})
        version.provider_payload['ragflow'] = {'datasetId': ragflow_binding.get('datasetId'), 'documents': documents}
        version.save(update_fields=['provider_payload', 'updated_at'])
        return documents

    def _pull_revision(self, repo_type, repo, revision=''):
        bindings = self._next_bindings(repo)
        for provider_key, client in (('gitea', self.gitea), ('localgit', self.localgit)):
            binding = bindings.get(provider_key) or {}
            if binding.get('state') != 'ready':
                continue
            try:
                exported = client.export_revision(binding, revision)
                if provider_key == 'gitea':
                    try:
                        binding.update(self.gitea.ensure_push_webhook(binding, repo_type, repo.repo_id))
                    except HubProviderSyncError as exc:
                        binding['webhookError'] = str(exc)
                bindings[provider_key] = _normalize_binding(binding)
                return {
                    'provider': provider_key,
                    'revision': exported.get('branch') or revision or repo.default_revision or 'main',
                    'commitSha': exported.get('commitSha') or '',
                    'artifactUri': exported.get('artifactUri') or exported.get('treeUrl') or '',
                    'files': exported.get('files') or [],
                    'providerBinding': bindings[provider_key],
                    'providerPayload': {
                        'branch': exported.get('branch') or revision or repo.default_revision or 'main',
                        'commitSha': exported.get('commitSha') or '',
                        'treeUrl': exported.get('treeUrl') or exported.get('artifactUri') or '',
                        'fileCount': len(exported.get('files') or []),
                        'source': f'{provider_key}-sync',
                    },
                    'repo_provider_bindings': bindings,
                    'repo_sync_status': _derive_sync_status(bindings),
                }
            except HubProviderSyncError as exc:
                bindings[provider_key] = _normalize_binding(binding, state='error', error_message=str(exc))
        raise HubProviderSyncError(f'No readable git-backed provider is configured for {repo.repo_id}')


def get_hub_provider_manager():
    return HubProviderManager()
