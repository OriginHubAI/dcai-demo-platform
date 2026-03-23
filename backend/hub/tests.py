from django.test import TestCase

from .models import DatasetRepo, DatasetVersion, DatasetFile, ModelRepo, ModelVersion, ModelFile


class HubApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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
