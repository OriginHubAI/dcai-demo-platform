from unittest.mock import patch

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from chat.models import Conversation
from chat.provider import OpenAICompatibleChatProvider
from df_conversation.models import DFConversation


class ChatRoutingTests(APITestCase):
    def test_dataflow_route_creates_tool_call(self):
        response = self.client.post('/api/v1/chat', {'question': '@DataFlow build a chemistry pipeline'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['type'], 'tool_call')
        self.assertEqual(payload['action'], 'open_iframe')
        self.assertEqual(payload['iframe_url'], '/dataflow/canvas')
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(DFConversation.objects.count(), 1)

    def test_dfagent_submodule_route_sets_tab(self):
        response = self.client.post('/api/v1/chat', {'question': '@DFAgent:operator_qa help me inspect operators'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['agent'], 'DFAgent')
        self.assertEqual(payload['iframe_url'], '/apps/OpenDCAI/DataFlow-Agent?tab=operator_qa')

    def test_keyword_routing_is_case_insensitive(self):
        response = self.client.post('/api/v1/chat', {'question': 'Build DataFlow Pipeline for chemistry'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['agent'], 'DataFlow-Agent')

    def test_anonymous_sessions_get_distinct_demo_users(self):
        second_client = self.client_class()

        first = self.client.post('/api/v1/chat', {'question': '@DataFlow create pipeline'}, format='json')
        second = second_client.post('/api/v1/chat', {'question': '@DataFlow create pipeline'}, format='json')

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(Conversation.objects.count(), 2)

        users = list(get_user_model().objects.filter(email__contains='demo+').order_by('email'))
        self.assertEqual(len(users), 2)

    @patch('chat.views.chat_provider.complete')
    def test_plain_chat_uses_llm_provider(self, mock_complete):
        mock_complete.return_value.model = 'gpt-4o'
        mock_complete.return_value.content = 'hello from llm'
        mock_complete.return_value.usage = {'total_tokens': 12}

        response = self.client.post('/api/v1/chat', {
            'question': 'hello there',
            'model': 'gpt-4o',
        }, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['answer'], 'hello from llm')
        self.assertEqual(payload['model'], 'gpt-4o')

    @patch('chat.views.chat_provider.list_models', return_value=['gpt-4o', 'deepseek-chat'])
    def test_chat_models_endpoint(self, _mock_models):
        response = self.client.get('/api/v1/chat/models')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['models'], ['gpt-4o', 'deepseek-chat'])

    @patch('chat.provider.httpx.Client')
    def test_provider_stream_ignores_usage_only_chunk(self, mock_client_cls):
        lines = [
            'data: {"choices":[{"delta":{"role":"assistant","content":""}}]}',
            '',
            'data: {"choices":[{"delta":{"content":"测试"}}]}',
            '',
            'data: {"choices":[{"delta":{"content":"成功。"}}]}',
            '',
            'data: {"choices":[],"usage":{"total_tokens":18}}',
            '',
            'data: [DONE]',
        ]

        mock_client = mock_client_cls.return_value.__enter__.return_value
        mock_response = mock_client.stream.return_value.__enter__.return_value
        mock_response.iter_lines.return_value = lines

        provider = OpenAICompatibleChatProvider()
        provider.base_url = 'http://example.com'
        provider.api_key = 'test-key'

        chunks = list(provider.stream([{'role': 'user', 'content': 'hello'}], model='gpt-4o'))
        self.assertEqual(''.join(chunks), '测试成功。')
