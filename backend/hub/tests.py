import hashlib
import hmac
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings

from openapi.models import OpenAPIKey
from user.models import User

from . import providers
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


class HubApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            email='hub-owner@example.com',
            username='hub-owner',
            password='secret123',
        )
        cls.read_key = OpenAPIKey.objects.create(
            user=cls.owner,
            name='hub-read',
            key='sk-test-read-key',
            key_type=OpenAPIKey.KeyType.READ,
        )
        cls.write_key = OpenAPIKey.objects.create(
            user=cls.owner,
            name='hub-write',
            key='sk-test-write-key',
            key_type=OpenAPIKey.KeyType.WRITE,
        )

        dataset = DatasetRepo.objects.create(
            repo_id='OpenDCAI/demo-dataset',
            namespace='OpenDCAI',
            slug='demo-dataset',
            author='OpenDCAI',
            name='Demo Dataset',
            task='text-generation',
            domain='nlp',
            modality='text',
            language='en',
            license='apache-2.0',
            description='Demo dataset description',
            summary='Demo dataset summary',
            size_label='12MB',
            row_count=1200,
            tags=['demo', 'sft'],
        )
        dataset_version = DatasetVersion.objects.create(
            repo=dataset,
            revision='main',
            commit_sha='abc1234',
            row_count=1200,
            size_label='12MB',
            is_latest=True,
        )
        DatasetFile.objects.create(
            version=dataset_version,
            path='train.jsonl',
            file_type='jsonl',
            size_bytes=1024,
            size_label='1KB',
            split='train',
            row_count=100,
            preview_rows=[{'prompt': 'hello', 'response': 'world'}],
        )
        DatasetFile.objects.create(
            version=dataset_version,
            path='README.md',
            file_type='markdown',
            size_bytes=512,
            size_label='512B',
            preview_text='# Demo Dataset\n\nDataset readme preview.',
        )

        model = ModelRepo.objects.create(
            repo_id='OpenDCAI/demo-model',
            namespace='OpenDCAI',
            slug='demo-model',
            author='OpenDCAI',
            name='Demo Model',
            pipeline_tag='text-generation',
            library='transformers',
            language='en',
            license='apache-2.0',
            description='Demo model description',
            summary='Demo model summary',
            tags=['demo'],
        )
        model_version = ModelVersion.objects.create(
            repo=model,
            revision='main',
            commit_sha='def5678',
            framework='transformers',
            params_label='7B',
            is_latest=True,
        )
        ModelFile.objects.create(
            version=model_version,
            path='config.json',
            file_type='json',
            size_bytes=2048,
            size_label='2KB',
            preview_text='{"architectures":["DemoForCausalLM"]}',
        )

        private_dataset = DatasetRepo.objects.create(
            repo_id='hub-owner/private-dataset',
            namespace='hub-owner',
            slug='private-dataset',
            author='hub-owner',
            name='Private Dataset',
            task='text-classification',
            domain='nlp',
            modality='text',
            language='en',
            license='apache-2.0',
            description='Private dataset',
            summary='Private dataset summary',
            visibility='private',
            size_label='4KB',
            row_count=50,
            tags=['private'],
        )
        private_version = DatasetVersion.objects.create(
            repo=private_dataset,
            revision='main',
            commit_sha='private001',
            row_count=50,
            size_label='4KB',
            is_latest=True,
        )
        DatasetFile.objects.create(
            version=private_version,
            path='train.jsonl',
            file_type='jsonl',
            size_bytes=128,
            size_label='128B',
            split='train',
            row_count=2,
            preview_rows=[{'text': 'secret'}, {'text': 'hidden'}],
        )

        knowledge = KnowledgeRepo.objects.create(
            repo_id='OpenDCAI/demo-knowledge-base',
            namespace='OpenDCAI',
            slug='demo-knowledge-base',
            author='hub-owner',
            name='Demo Knowledge Base',
            description='Knowledge base description',
            summary='Knowledge base summary',
            visibility='public',
            status='ready',
            source_dataset='OpenDCAI/demo-dataset',
            source_files=['train.jsonl'],
            file_count=2,
            document_count=120,
            tags=['knowledge-base', 'demo'],
            vector_store={'provider': 'faiss', 'vectorCount': 120, 'collection': 'demo_kb'},
            pipeline={'stages': [{'name': 'parse', 'status': 'completed'}], 'progress': 100},
            knowledge_graph={'enabled': True, 'entityCount': 12, 'relationCount': 24},
            retrieval={'topK': 6},
            mcp={'enabled': True, 'endpoint': '/mcp/kb/demo'},
        )
        knowledge_version = KnowledgeVersion.objects.create(
            repo=knowledge,
            revision='main',
            commit_sha='kb001',
            manifest={'sourceDataset': 'OpenDCAI/demo-dataset'},
            is_latest=True,
        )
        KnowledgeFile.objects.create(
            version=knowledge_version,
            path='README.md',
            file_type='markdown',
            size_bytes=256,
            size_label='256B',
            preview_text='# Demo KB',
        )
        KnowledgeFile.objects.create(
            version=knowledge_version,
            path='chunks/preview.jsonl',
            file_type='jsonl',
            size_bytes=512,
            size_label='512B',
            row_count=2,
            preview_rows=[{'chunk': 'alpha'}, {'chunk': 'beta'}],
        )
        KnowledgeBuild.objects.create(
            repo=knowledge,
            trigger='seed',
            status='completed',
            progress=100,
            stages=[{'name': 'parse', 'status': 'completed'}],
        )

    def test_dataset_list_endpoint(self):
        response = self.client.get('/api/v2/datasets')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        ids = [item['id'] for item in payload['data']['list']]
        self.assertGreaterEqual(payload['data']['total'], 1)
        self.assertIn('OpenDCAI/demo-dataset', ids)

    def test_dataset_detail_endpoint(self):
        response = self.client.get('/api/v2/datasets/OpenDCAI/demo-dataset')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['id'], 'OpenDCAI/demo-dataset')
        self.assertEqual(len(payload['files']), 2)
        paths = [item['path'] for item in payload['files']]
        self.assertIn('train.jsonl', paths)
        self.assertIn('README.md', paths)

    def test_dataset_preview_endpoint(self):
        response = self.client.get('/api/v2/datasets/OpenDCAI/demo-dataset/preview', {'path': 'train.jsonl'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['path'], 'train.jsonl')
        self.assertEqual(payload['previewRows'][0]['prompt'], 'hello')

    def test_model_list_endpoint(self):
        response = self.client.get('/api/v2/models')
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['code'], 0)
        ids = [item['id'] for item in payload['data']['list']]
        self.assertIn('OpenDCAI/demo-model', ids)

    def test_model_detail_endpoint(self):
        response = self.client.get('/api/v2/models/OpenDCAI/demo-model')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['id'], 'OpenDCAI/demo-model')
        self.assertEqual(payload['files'][0]['path'], 'config.json')

    def test_model_tree_and_preview_endpoints(self):
        tree_response = self.client.get('/api/v2/models/OpenDCAI/demo-model/tree')
        self.assertEqual(tree_response.status_code, 200)
        tree_payload = tree_response.json()['data']
        self.assertEqual(tree_payload['revision'], 'main')
        self.assertTrue(any(item['path'] == 'config.json' for item in tree_payload['items']))

        preview_response = self.client.get('/api/v2/models/OpenDCAI/demo-model/preview', {'path': 'config.json'})
        self.assertEqual(preview_response.status_code, 200)
        self.assertIn('DemoForCausalLM', preview_response.json()['data']['previewText'])

    def test_dataset_tree_endpoint(self):
        response = self.client.get('/api/v2/datasets/OpenDCAI/demo-dataset/tree')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['revision'], 'main')
        paths = [item['path'] for item in payload['items']]
        self.assertIn('README.md', paths)
        self.assertIn('train.jsonl', paths)

    def test_dataset_rows_endpoint(self):
        response = self.client.get('/api/v2/datasets/OpenDCAI/demo-dataset/rows', {'split': 'train'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['num_rows_total'], 100)
        self.assertEqual(payload['rows'][0]['row']['prompt'], 'hello')
        self.assertEqual(payload['file']['path'], 'train.jsonl')

    def test_hf_viewer_endpoints(self):
        splits_response = self.client.get('/api/v2/hf/splits', {'dataset': 'OpenDCAI/demo-dataset'})
        self.assertEqual(splits_response.status_code, 200)
        split_payload = splits_response.json()
        self.assertEqual(split_payload['dataset'], 'OpenDCAI/demo-dataset')
        self.assertEqual(split_payload['splits'][0]['split'], 'train')

        rows_response = self.client.get('/api/v2/hf/rows', {'dataset': 'OpenDCAI/demo-dataset', 'split': 'train'})
        self.assertEqual(rows_response.status_code, 200)
        rows_payload = rows_response.json()
        self.assertEqual(rows_payload['rows'][0]['row']['response'], 'world')

    def test_hf_tree_and_resolve_endpoints(self):
        tree_response = self.client.get('/api/v2/hf/api/datasets/OpenDCAI/demo-dataset/tree/main')
        self.assertEqual(tree_response.status_code, 200)
        tree_payload = tree_response.json()
        self.assertTrue(any(item['path'] == 'train.jsonl' for item in tree_payload))

        resolve_response = self.client.get('/api/v2/hf/datasets/OpenDCAI/demo-dataset/resolve/main/train.jsonl')
        self.assertEqual(resolve_response.status_code, 200)
        self.assertIn(b'"prompt": "hello"', resolve_response.content)

    def test_model_hf_metadata_and_resolve_endpoints(self):
        metadata_response = self.client.get('/api/v2/hf/api/models/OpenDCAI/demo-model')
        self.assertEqual(metadata_response.status_code, 200)
        metadata_payload = metadata_response.json()
        self.assertEqual(metadata_payload['id'], 'OpenDCAI/demo-model')
        self.assertEqual(metadata_payload['sha'], 'def5678')

        resolve_response = self.client.get('/api/v2/hf/models/OpenDCAI/demo-model/resolve/main/config.json')
        self.assertEqual(resolve_response.status_code, 200)
        self.assertIn(b'DemoForCausalLM', resolve_response.content)

    def test_knowledge_list_and_detail_endpoints(self):
        list_response = self.client.get('/api/v2/knowledge-bases')
        self.assertEqual(list_response.status_code, 200)
        list_payload = list_response.json()['data']['list']
        self.assertTrue(any(item['id'] == 'OpenDCAI/demo-knowledge-base' for item in list_payload))

        detail_response = self.client.get('/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base')
        self.assertEqual(detail_response.status_code, 200)
        detail_payload = detail_response.json()['data']
        self.assertEqual(detail_payload['sourceDataset'], 'OpenDCAI/demo-dataset')
        self.assertEqual(detail_payload['builds'][0]['status'], 'completed')

    def test_sync_local_git_repo_command_upserts_dataset_revision(self):
        repo = DatasetRepo.objects.create(
            repo_id='OpenDCAI/git-backed-dataset',
            namespace='OpenDCAI',
            slug='git-backed-dataset',
            author='OpenDCAI',
            name='Git Backed Dataset',
            task='text-classification',
            domain='nlp',
            modality='text',
            language='en',
            license='apache-2.0',
            description='Dataset synced from bare git repo',
            summary='',
            default_revision='main',
        )

        with tempfile.TemporaryDirectory(prefix='hub-sync-media-') as media_dir, tempfile.TemporaryDirectory(
            prefix='hub-sync-git-'
        ) as work_dir:
            bare_dir = Path(work_dir) / 'remote.git'
            checkout_dir = Path(work_dir) / 'checkout'
            self._git('init', '--bare', '--initial-branch', 'main', str(bare_dir))
            self._git('clone', str(bare_dir), str(checkout_dir))

            self._write_text(checkout_dir / 'README.md', '# Git Backed Dataset\n')
            self._write_text(
                checkout_dir / 'train.jsonl',
                '{"text":"alpha","label":1}\n{"text":"beta","label":0}\n',
            )
            self._git_commit_and_push(checkout_dir, 'Initial dataset push')

            with override_settings(MEDIA_ROOT=media_dir):
                call_command(
                    'sync_local_git_repo',
                    repo_type='datasets',
                    repo_id=repo.repo_id,
                    git_dir=str(bare_dir),
                    refname='refs/heads/main',
                )

                version = repo.versions.get(revision='main')
                repo.refresh_from_db()
                self.assertEqual(version.row_count, 2)
                self.assertTrue(version.is_latest)
                self.assertEqual(version.files.count(), 2)
                train_file = version.files.get(path='train.jsonl')
                self.assertEqual(train_file.row_count, 2)
                self.assertEqual(train_file.preview_rows[0]['text'], 'alpha')
                self.assertEqual(repo.provider_bindings['localgit']['cloneUrl'], str(bare_dir))

                self._write_text(
                    checkout_dir / 'train.jsonl',
                    '{"text":"alpha","label":1}\n{"text":"beta","label":0}\n{"text":"gamma","label":1}\n',
                )
                self._git_commit_and_push(checkout_dir, 'Update dataset rows')
                call_command(
                    'sync_local_git_repo',
                    repo_type='datasets',
                    repo_id=repo.repo_id,
                    git_dir=str(bare_dir),
                    refname='refs/heads/main',
                )

                repo.refresh_from_db()
                version.refresh_from_db()
                self.assertEqual(repo.versions.count(), 1)
                self.assertEqual(version.row_count, 3)
                self.assertEqual(repo.row_count, 3)
                self.assertEqual(version.files.get(path='train.jsonl').row_count, 3)

    @patch('hub.api.get_hub_provider_manager')
    def test_dataset_manual_sync_endpoint_persists_provider_files(self, mock_get_provider_manager):
        repo = DatasetRepo.objects.get(repo_id='hub-owner/private-dataset')
        manager = Mock()
        manager.pull_dataset_revision.return_value = {
            'provider': 'gitea',
            'revision': 'main',
            'commitSha': 'sync-main-001',
            'artifactUri': 'https://git.example.com/hub-owner/private-dataset/src/branch/main',
            'files': [
                {'path': 'README.md', 'raw_bytes': b'# Private Dataset\n'},
                {
                    'path': 'train.jsonl',
                    'raw_bytes': b'{"text":"alpha","label":1}\n{"text":"beta","label":0}\n',
                },
            ],
            'providerBinding': {
                'state': 'ready',
                'provider': 'gitea',
                'fullName': repo.repo_id,
                'cloneUrl': 'https://git.example.com/hub-owner/private-dataset.git',
            },
            'providerPayload': {
                'branch': 'main',
                'commitSha': 'sync-main-001',
                'treeUrl': 'https://git.example.com/hub-owner/private-dataset/src/branch/main',
                'fileCount': 2,
                'source': 'gitea-sync',
            },
            'repo_provider_bindings': {
                'gitea': {
                    'state': 'ready',
                    'provider': 'gitea',
                    'fullName': repo.repo_id,
                    'cloneUrl': 'https://git.example.com/hub-owner/private-dataset.git',
                }
            },
            'repo_sync_status': 'synced',
        }
        mock_get_provider_manager.return_value = manager

        with tempfile.TemporaryDirectory(prefix='hub-manual-sync-media-') as media_dir, override_settings(MEDIA_ROOT=media_dir):
            response = self.client.post(
                f'/api/v2/datasets/{repo.repo_id}/sync',
                data=json_dumps({'revision': 'main'}),
                content_type='application/json',
                HTTP_AUTHORIZATION='Bearer sk-test-write-key',
            )

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['provider'], 'gitea')
        self.assertEqual(payload['version']['revision'], 'main')
        self.assertEqual(payload['version']['providerCommit'], 'sync-main-001')
        self.assertEqual(payload['files'][1]['path'], 'train.jsonl')

        repo.refresh_from_db()
        version = DatasetVersion.objects.get(repo=repo, revision='main')
        self.assertEqual(repo.sync_status, 'synced')
        self.assertEqual(repo.provider_bindings['gitea']['cloneUrl'], 'https://git.example.com/hub-owner/private-dataset.git')
        self.assertEqual(version.provider_commit, 'sync-main-001')
        self.assertEqual(version.artifact_uri, 'https://git.example.com/hub-owner/private-dataset/src/branch/main')
        self.assertEqual(version.files.count(), 2)
        self.assertEqual(version.files.get(path='train.jsonl').row_count, 2)
        manager.pull_dataset_revision.assert_called_once_with(repo, 'main')

    @patch('hub.api.get_hub_provider_manager')
    def test_gitea_push_webhook_syncs_dataset(self, mock_get_provider_manager):
        repo = DatasetRepo.objects.get(repo_id='hub-owner/private-dataset')
        repo.provider_bindings = {
            'gitea': {
                'state': 'ready',
                'provider': 'gitea',
                'fullName': repo.repo_id,
                'owner': 'hub-owner',
                'name': 'private-dataset',
                'cloneUrl': 'https://git.example.com/hub-owner/private-dataset.git',
            }
        }
        repo.sync_status = 'synced'
        repo.save(update_fields=['provider_bindings', 'sync_status', 'updated_at'])

        manager = Mock()
        manager.pull_dataset_revision.return_value = {
            'provider': 'gitea',
            'revision': 'main',
            'commitSha': 'webhook-main-001',
            'artifactUri': 'https://git.example.com/hub-owner/private-dataset/src/branch/main',
            'files': [
                {
                    'path': 'train.jsonl',
                    'raw_bytes': b'{"text":"webhook","label":1}\n',
                }
            ],
            'providerBinding': repo.provider_bindings['gitea'],
            'providerPayload': {
                'branch': 'main',
                'commitSha': 'webhook-main-001',
                'treeUrl': 'https://git.example.com/hub-owner/private-dataset/src/branch/main',
                'fileCount': 1,
                'source': 'gitea-sync',
            },
            'repo_provider_bindings': repo.provider_bindings,
            'repo_sync_status': 'synced',
        }
        mock_get_provider_manager.return_value = manager

        body = json_dumps(
            {
                'ref': 'refs/heads/main',
                'repository': {'full_name': repo.repo_id},
            }
        )
        signature = hmac.new(b'super-secret', body.encode('utf-8'), hashlib.sha256).hexdigest()

        with tempfile.TemporaryDirectory(prefix='hub-webhook-sync-media-') as media_dir, override_settings(
            MEDIA_ROOT=media_dir,
            GITEA_WEBHOOK_SECRET='super-secret',
        ):
            response = self.client.post(
                '/api/v2/integrations/gitea/webhook',
                data=body,
                content_type='application/json',
                HTTP_X_GITEA_EVENT='push',
                HTTP_X_GITEA_SIGNATURE=signature,
            )

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['repository'], repo.repo_id)
        self.assertEqual(payload['revision'], 'main')
        self.assertEqual(payload['provider'], 'gitea')

        repo.refresh_from_db()
        version = DatasetVersion.objects.get(repo=repo, revision='main')
        self.assertEqual(version.provider_commit, 'webhook-main-001')
        self.assertEqual(version.files.count(), 1)
        self.assertEqual(version.files.get(path='train.jsonl').preview_rows[0]['text'], 'webhook')
        manager.pull_dataset_revision.assert_called_once_with(repo, 'main')

    def _write_text(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def _git_commit_and_push(self, checkout_dir, message):
        self._git('-C', str(checkout_dir), 'add', '.')
        self._git(
            '-C',
            str(checkout_dir),
            '-c',
            'user.name=Hub Tests',
            '-c',
            'user.email=hub-tests@example.com',
            'commit',
            '-m',
            message,
        )
        self._git('-C', str(checkout_dir), 'push', 'origin', 'main')

    def _git(self, *args):
        result = subprocess.run(['git', *args], capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout or f'git {" ".join(args)} failed')
        return result

    def test_knowledge_tree_and_preview_endpoints(self):
        tree_response = self.client.get('/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base/tree')
        self.assertEqual(tree_response.status_code, 200)
        tree_payload = tree_response.json()['data']
        self.assertTrue(any(item['path'] == 'README.md' for item in tree_payload['items']))
        self.assertTrue(any(item['path'] == 'chunks' and item['type'] == 'directory' for item in tree_payload['items']))

        preview_response = self.client.get(
            '/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base/preview',
            {'path': 'chunks/preview.jsonl'},
        )
        self.assertEqual(preview_response.status_code, 200)
        self.assertEqual(preview_response.json()['data']['previewRows'][0]['chunk'], 'alpha')

    def test_knowledge_build_creation_endpoint(self):
        response = self.client.post(
            '/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base/builds',
            data=json_dumps({'trigger': 'manual'}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )
        self.assertEqual(response.status_code, 201)
        payload = response.json()['data']
        self.assertEqual(payload['trigger'], 'manual')
        self.assertIn(payload['status'], {'running', 'queued'})

    def test_private_dataset_requires_token(self):
        anonymous_response = self.client.get('/api/v2/datasets/hub-owner/private-dataset')
        self.assertEqual(anonymous_response.status_code, 403)

        authorized_response = self.client.get(
            '/api/v2/datasets/hub-owner/private-dataset',
            HTTP_AUTHORIZATION='Bearer sk-test-read-key',
        )
        self.assertEqual(authorized_response.status_code, 200)
        self.assertEqual(authorized_response.json()['data']['visibility'], 'private')

    def test_private_dataset_revision_write_requires_write_token(self):
        read_response = self.client.post(
            '/api/v2/datasets/hub-owner/private-dataset/revisions',
            data=json_dumps({'revision': 'v2', 'files': [{'path': 'extra.jsonl', 'fileType': 'jsonl', 'previewRows': [{'x': 1}]}]}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-read-key',
        )
        self.assertEqual(read_response.status_code, 403)

        write_response = self.client.post(
            '/api/v2/datasets/hub-owner/private-dataset/revisions',
            data=json_dumps({'revision': 'v2', 'files': [{'path': 'extra.jsonl', 'fileType': 'jsonl', 'previewRows': [{'x': 1}]}]}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )
        self.assertEqual(write_response.status_code, 201)
        self.assertEqual(write_response.json()['data']['version']['revision'], 'v2')

    def test_dataset_revision_infers_row_count_from_content(self):
        response = self.client.post(
            '/api/v2/datasets/hub-owner/private-dataset/revisions',
            data=json_dumps(
                {
                    'revision': 'v3',
                    'files': [
                        {
                            'path': 'train.jsonl',
                            'fileType': 'jsonl',
                            'content': '{"x": 1}\n{"x": 2}\n{"x": 3}\n',
                            'encoding': 'utf-8',
                            'previewRows': [{'x': 1}, {'x': 2}],
                        }
                    ],
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['data']['version']['rows'], 3)

    def test_knowledge_revision_infers_document_count_from_content(self):
        response = self.client.post(
            '/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base/revisions',
            data=json_dumps(
                {
                    'revision': 'v2',
                    'files': [
                        {
                            'path': 'chunks/new.jsonl',
                            'fileType': 'jsonl',
                            'content': '{"chunk": "a"}\n{"chunk": "b"}\n{"chunk": "c"}\n',
                            'encoding': 'utf-8',
                            'previewRows': [{'chunk': 'a'}, {'chunk': 'b'}],
                        }
                    ],
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )
        self.assertEqual(response.status_code, 201)
        detail_response = self.client.get('/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base')
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.json()['data']['documentCount'], 3)

    @patch('hub.api.get_hub_provider_manager')
    def test_dataset_create_persists_provider_bindings(self, mock_get_provider_manager):
        manager = Mock()
        manager.bind_dataset_repo.return_value = {
            'provider_bindings': {
                'gitea': {
                    'state': 'ready',
                    'provider': 'gitea',
                    'cloneUrl': 'https://git.example.com/OpenDCAI/new-dataset.git',
                },
                'lakefs': {
                    'state': 'ready',
                    'provider': 'lakefs',
                    'repository': 'OpenDCAI--new-dataset',
                },
            },
            'sync_status': 'synced',
            'default_revision': 'main',
        }
        mock_get_provider_manager.return_value = manager

        response = self.client.post(
            '/api/v2/datasets',
            data=json_dumps(
                {
                    'namespace': 'OpenDCAI',
                    'slug': 'new-dataset',
                    'name': 'New Dataset',
                    'description': 'Dataset with provider bindings',
                    'defaultRevision': 'main',
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()['data']
        self.assertEqual(payload['syncStatus'], 'synced')
        self.assertEqual(payload['providerBindings']['gitea']['cloneUrl'], 'https://git.example.com/OpenDCAI/new-dataset.git')
        repo = DatasetRepo.objects.get(repo_id='OpenDCAI/new-dataset')
        self.assertEqual(repo.sync_status, 'synced')
        self.assertEqual(repo.provider_bindings['lakefs']['repository'], 'OpenDCAI--new-dataset')
        self.assertEqual(repo.default_revision, 'main')

    @patch('hub.api.get_hub_provider_manager')
    def test_dataset_revision_persists_provider_fields(self, mock_get_provider_manager):
        manager = Mock()
        manager.sync_dataset_version.return_value = {
            'provider_payload': {
                'gitea': {'treeUrl': 'https://git.example.com/hub-owner/private-dataset/src/branch/v-provider'},
                'lakefs': {'commitId': 'lakefs-commit-001', 'branch': 'v-provider'},
            },
            'provider_revision': 'v-provider',
            'provider_commit': 'lakefs-commit-001',
            'artifact_uri': 'https://git.example.com/hub-owner/private-dataset/src/branch/v-provider',
            'repo_provider_bindings': {
                'gitea': {'state': 'ready', 'provider': 'gitea'},
                'lakefs': {'state': 'ready', 'provider': 'lakefs'},
            },
            'repo_sync_status': 'synced',
        }
        mock_get_provider_manager.return_value = manager

        response = self.client.post(
            '/api/v2/datasets/hub-owner/private-dataset/revisions',
            data=json_dumps(
                {
                    'revision': 'v-provider',
                    'files': [
                        {
                            'path': 'train.jsonl',
                            'fileType': 'jsonl',
                            'content': '{"prompt":"a","response":"b"}\n',
                            'encoding': 'utf-8',
                            'previewRows': [{'prompt': 'a', 'response': 'b'}],
                        }
                    ],
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()['data']['version']
        self.assertEqual(payload['providerRevision'], 'v-provider')
        self.assertEqual(payload['providerCommit'], 'lakefs-commit-001')
        self.assertEqual(payload['artifactUri'], 'https://git.example.com/hub-owner/private-dataset/src/branch/v-provider')

        version = DatasetVersion.objects.get(repo__repo_id='hub-owner/private-dataset', revision='v-provider')
        repo = DatasetRepo.objects.get(repo_id='hub-owner/private-dataset')
        self.assertEqual(version.provider_revision, 'v-provider')
        self.assertEqual(version.provider_commit, 'lakefs-commit-001')
        self.assertEqual(version.provider_payload['lakefs']['branch'], 'v-provider')
        self.assertEqual(repo.sync_status, 'synced')

    @patch('hub.api.get_hub_provider_manager')
    def test_model_revision_persists_provider_fields(self, mock_get_provider_manager):
        owned_model = ModelRepo.objects.create(
            repo_id='hub-owner/private-model',
            namespace='hub-owner',
            slug='private-model',
            author='hub-owner',
            name='Private Model',
            pipeline_tag='text-generation',
            library='transformers',
            language='en',
            license='apache-2.0',
            description='Owned model for revision publishing',
            summary='Owned model summary',
            visibility='private',
            tags=['private'],
        )
        manager = Mock()
        manager.sync_model_version.return_value = {
            'provider_payload': {
                'mlflow': {'version': '5', 'currentStage': 'Staging'},
                'gitea': {'treeUrl': 'https://git.example.com/hub-owner/private-model/src/branch/v2'},
            },
            'provider_revision': '5',
            'provider_commit': 'provider-model-001',
            'artifact_uri': 's3://mlflow-artifacts/private-model/v2',
            'repo_provider_bindings': {
                'gitea': {'state': 'ready', 'provider': 'gitea'},
                'mlflow': {'state': 'ready', 'provider': 'mlflow', 'modelName': 'hub-owner/private-model'},
            },
            'repo_sync_status': 'synced',
        }
        mock_get_provider_manager.return_value = manager

        response = self.client.post(
            f'/api/v2/models/{owned_model.repo_id}/revisions',
            data=json_dumps(
                {
                    'revision': 'v2',
                    'framework': 'transformers',
                    'params': '7B',
                    'artifactUri': 's3://mlflow-artifacts/private-model/v2',
                    'stage': 'Staging',
                    'files': [
                        {
                            'path': 'README.md',
                            'fileType': 'md',
                            'content': '# Demo Model v2',
                            'encoding': 'utf-8',
                        }
                    ],
                }
            ),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()['data']['version']
        self.assertEqual(payload['providerRevision'], '5')
        self.assertEqual(payload['providerCommit'], 'provider-model-001')
        self.assertEqual(payload['artifactUri'], 's3://mlflow-artifacts/private-model/v2')
        self.assertEqual(payload['providerPayload']['mlflow']['currentStage'], 'Staging')

        version = ModelVersion.objects.get(repo__repo_id='hub-owner/private-model', revision='v2')
        repo = ModelRepo.objects.get(repo_id='hub-owner/private-model')
        self.assertEqual(version.artifact_uri, 's3://mlflow-artifacts/private-model/v2')
        self.assertEqual(version.provider_revision, '5')
        self.assertEqual(repo.provider_bindings['mlflow']['modelName'], 'hub-owner/private-model')
        self.assertEqual(repo.sync_status, 'synced')

    @patch('hub.api.get_hub_provider_manager')
    def test_knowledge_build_persists_provider_fields(self, mock_get_provider_manager):
        manager = Mock()
        manager.trigger_knowledge_build.return_value = {
            'provider_job_id': 'ragflow-dataset-001:99',
            'provider_status': 'submitted',
            'provider_payload': {
                'ragflow': {
                    'datasetId': 'ragflow-dataset-001',
                    'documents': [{'id': 'doc-1', 'name': 'README.md'}],
                    'response': {'task_id': 'parse-123'},
                }
            },
            'repo_provider_bindings': {
                'ragflow': {'state': 'ready', 'provider': 'ragflow', 'datasetId': 'ragflow-dataset-001'},
            },
            'repo_sync_status': 'synced',
        }
        mock_get_provider_manager.return_value = manager

        response = self.client.post(
            '/api/v2/knowledge-bases/OpenDCAI/demo-knowledge-base/builds',
            data=json_dumps({'trigger': 'manual', 'revision': 'main'}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer sk-test-write-key',
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()['data']
        self.assertEqual(payload['providerStatus'], 'submitted')
        self.assertEqual(payload['providerJobId'], 'ragflow-dataset-001:99')
        self.assertEqual(payload['providerPayload']['ragflow']['datasetId'], 'ragflow-dataset-001')

        build = KnowledgeBuild.objects.get(id=payload['id'])
        repo = KnowledgeRepo.objects.get(repo_id='OpenDCAI/demo-knowledge-base')
        self.assertEqual(build.provider_status, 'submitted')
        self.assertEqual(build.provider_job_id, 'ragflow-dataset-001:99')
        self.assertEqual(build.provider_payload['ragflow']['response']['task_id'], 'parse-123')
        self.assertEqual(repo.pipeline['providerStatus'], 'submitted')
        self.assertEqual(repo.provider_bindings['ragflow']['datasetId'], 'ragflow-dataset-001')


class GiteaHubClientTests(TestCase):
    @override_settings(
        GITEA_BASE_URL='https://git.example.com',
        GITEA_TOKEN='gitea-token',
        GITEA_WEBHOOK_BASE_URL='https://dcai.example.com',
        GITEA_WEBHOOK_SECRET='webhook-secret',
    )
    def test_ensure_push_webhook_creates_wildcard_branch_filter(self):
        client = providers.GiteaHubClient()
        requests = []

        def fake_request(method, path, **kwargs):
            requests.append((method, path, kwargs.get('json')))
            if method == 'GET':
                return []
            if method == 'POST':
                return {'id': 9}
            raise AssertionError(f'unexpected request: {method} {path}')

        client._request = Mock(side_effect=fake_request)

        payload = client.ensure_push_webhook({'owner': 'dcai', 'name': 'demo-repo'}, 'datasets', 'dcai/demo-repo')

        self.assertEqual(payload['webhookId'], 9)
        self.assertEqual(requests[1][0], 'POST')
        self.assertEqual(requests[1][2]['branch_filter'], '*')
        self.assertEqual(requests[1][2]['events'], ['push'])

    @override_settings(
        GITEA_BASE_URL='https://git.example.com',
        GITEA_TOKEN='gitea-token',
        GITEA_WEBHOOK_BASE_URL='https://dcai.example.com',
        GITEA_WEBHOOK_SECRET='webhook-secret',
    )
    def test_ensure_push_webhook_updates_legacy_branch_filter(self):
        client = providers.GiteaHubClient()
        requests = []

        def fake_request(method, path, **kwargs):
            requests.append((method, path, kwargs.get('json')))
            if method == 'GET':
                return [
                    {
                        'id': 5,
                        'config': {
                            'url': 'https://dcai.example.com/api/v2/integrations/gitea/webhook',
                            'content_type': 'json',
                        },
                        'events': ['push'],
                        'branch_filter': 'refs/heads/*',
                        'active': True,
                        'authorization_header': '',
                    }
                ]
            if method == 'PATCH':
                return {'id': 5}
            raise AssertionError(f'unexpected request: {method} {path}')

        client._request = Mock(side_effect=fake_request)

        payload = client.ensure_push_webhook({'owner': 'dcai', 'name': 'demo-repo'}, 'datasets', 'dcai/demo-repo')

        self.assertEqual(payload['webhookId'], 5)
        self.assertEqual(requests[1][0], 'PATCH')
        self.assertEqual(requests[1][1], '/api/v1/repos/dcai/demo-repo/hooks/5')
        self.assertEqual(requests[1][2]['branch_filter'], '*')


def json_dumps(payload):
    import json

    return json.dumps(payload)
