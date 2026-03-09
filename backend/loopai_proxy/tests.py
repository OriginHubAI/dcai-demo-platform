from unittest.mock import patch

from django.test import TestCase


class LoopAIProxyTests(TestCase):
    @patch('loopai_proxy.views.httpx.Client')
    def test_sse_proxy_accepts_event_stream_header(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        response = mock_client.send.return_value
        response.status_code = 200
        response.headers = {'content-type': 'text/event-stream'}
        response.iter_bytes.return_value = iter([b'data: {"message":"ok"}\n\n'])

        result = self.client.get(
            '/api/v2/loopai/starter/agent/message/stream',
            HTTP_ACCEPT='text/event-stream',
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result['Content-Type'], 'text/event-stream')

    def test_options_request_returns_allow_header(self):
        result = self.client.options('/api/v2/loopai/starter/agent/message/stream')

        self.assertEqual(result.status_code, 204)
        self.assertIn('GET', result['Allow'])
