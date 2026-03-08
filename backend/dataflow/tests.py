from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import override_settings
from rest_framework.test import APITestCase

from dataflow.services import DataFlowCatalog


class DataFlowWorkspaceTests(APITestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        operators_root = Path(self.tempdir.name)
        package_root = operators_root / 'core_text'
        package_root.mkdir(parents=True)
        (package_root / 'sample_operator.py').write_text('print("ok")\n', encoding='utf-8')
        self.override = override_settings(DATAFLOW_OPERATORS_ROOT=str(operators_root))
        self.override.enable()

        from dataflow import views as dataflow_views

        self.original_catalog = dataflow_views.catalog
        self.original_binary = dataflow_views.code_server_manager._binary
        self.original_sessions = dict(dataflow_views.code_server_manager._sessions)
        dataflow_views.catalog = DataFlowCatalog()
        dataflow_views.code_server_manager._sessions.clear()
        dataflow_views.code_server_manager._binary = None

    def tearDown(self):
        from dataflow import views as dataflow_views

        dataflow_views.catalog = self.original_catalog
        dataflow_views.code_server_manager._binary = self.original_binary
        dataflow_views.code_server_manager._sessions.clear()
        dataflow_views.code_server_manager._sessions.update(self.original_sessions)
        self.override.disable()
        self.tempdir.cleanup()

    def test_package_listing_and_file_content(self):
        listing = self.client.get('/api/v2/dataflow/packages')
        self.assertEqual(listing.status_code, 200)
        items = listing.json()['data']['list']
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['id'], 'core_text')
        self.assertNotIn('repo_path', items[0])

        tree = self.client.get('/api/v2/dataflow/packages/core_text/files')
        self.assertEqual(tree.status_code, 200)
        self.assertEqual(tree.json()['data']['type'], 'directory')

        content = self.client.get('/api/v2/dataflow/packages/core_text/file', {'path': 'sample_operator.py'})
        self.assertEqual(content.status_code, 200)
        self.assertIn('print("ok")', content.json()['data']['content'])

    def test_editor_start_falls_back_to_preview_mode(self):
        response = self.client.post('/api/v2/dataflow/packages/core_text/editor/start')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['mode'], 'preview')
        self.assertIn('code-server', payload['reason'])

    def test_package_test_runs_compileall(self):
        response = self.client.post('/api/v2/dataflow/packages/core_text/test')
        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertTrue(payload['success'])
        self.assertIn('compileall', payload['command'])

    @patch('dataflow.proxy_views.httpx.Client')
    def test_proxy_view_uses_sync_client(self, mock_client_cls):
        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_client.request.return_value.status_code = 200
        mock_client.request.return_value.content = b'{"ok": true}'
        mock_client.request.return_value.headers = {'content-type': 'application/json'}

        response = self.client.get('/api/v2/dataflow/operators/list')

        self.assertEqual(response.status_code, 200)
        mock_client.request.assert_called_once()
