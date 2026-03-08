from unittest.mock import patch

from rest_framework.test import APITestCase


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class FakeAsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url):
        if ':8002/health' in url:
            return FakeResponse(200)
        if ':8003/health' in url or ':8003/' in url or ':18003/health' in url or ':18003/' in url:
            return FakeResponse(200)
        if ':7860/health' in url:
            return FakeResponse(404)
        if ':7860/' in url:
            return FakeResponse(200)
        return FakeResponse(503)


class ServicesHealthTests(APITestCase):
    @patch('core.views.httpx.AsyncClient', return_value=FakeAsyncClient())
    def test_services_health_endpoint(self, _mock_client):
        response = self.client.get('/api/v2/services/health')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertTrue(payload['ok'])
        self.assertIn('dataflow', payload['services'])
        self.assertEqual(payload['services']['dfagent']['status_code'], 200)
        self.assertTrue(payload['services']['dfagent']['url'].endswith('/'))
