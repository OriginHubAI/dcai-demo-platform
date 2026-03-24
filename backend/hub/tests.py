from django.test import TestCase

from openapi.models import OpenAPIKey
from user.models import User

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


def json_dumps(payload):
    import json

    return json.dumps(payload)
