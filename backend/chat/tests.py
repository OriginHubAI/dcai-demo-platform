import uuid
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from chat.models import Conversation
from chat.provider import OpenAICompatibleChatProvider
from df_conversation.models import DFConversation


class ChatRoutingTests(SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        self.catalog_patcher = patch('dataflow.services.catalog')
        self.mock_catalog = self.catalog_patcher.start()
        self.mock_catalog.list_packages.return_value = []

    def tearDown(self):
        self.catalog_patcher.stop()

    @patch('chat.views.transaction.atomic')
    @patch('chat.views.ChatMessageView._resolve_user')
    @patch('chat.views.Conversation.objects')
    @patch('chat.views.Question.objects')
    @patch('chat.views.DFConversation.objects')
    @patch('chat.views.DFMessage.objects')
    def test_dataflow_route_creates_tool_call(self, mock_df_msg, mock_df_conv, mock_q, mock_conv, mock_resolve_user, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = MagicMock()
        mock_resolve_user.return_value = MagicMock()
        mock_conv.create.return_value = MagicMock(conversation_id='conv_123')
        mock_df_conv.create.return_value = MagicMock(id=uuid.UUID('e063cb5b-10b8-4b43-91be-65e460e80730'))
        
        response = self.client.post('/api/v1/chat', {'question': '@DataFlow build a chemistry pipeline'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['type'], 'tool_call')
        self.assertEqual(payload['action'], 'open_iframe')
        self.assertEqual(payload['iframe_url'], '/dataflow/canvas')
        self.assertEqual(mock_conv.create.call_count, 1)
        self.assertEqual(mock_df_conv.create.call_count, 1)

    @patch('chat.views.transaction.atomic')
    @patch('chat.views.ChatMessageView._resolve_user')
    @patch('chat.views.Conversation.objects')
    @patch('chat.views.Question.objects')
    @patch('chat.views.DFConversation.objects')
    @patch('chat.views.DFMessage.objects')
    def test_dfagent_submodule_route_sets_tab(self, mock_df_msg, mock_df_conv, mock_q, mock_conv, mock_resolve_user, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = MagicMock()
        mock_resolve_user.return_value = MagicMock()
        mock_conv.create.return_value = MagicMock(conversation_id='conv_123')
        
        response = self.client.post('/api/v1/chat', {'question': '@DFAgent:operator_qa help me inspect operators'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['agent'], 'DFAgent')
        self.assertEqual(payload['iframe_url'], '/apps/OpenDCAI/DataFlow-Agent?tab=operator_qa')

    @patch('chat.views.transaction.atomic')
    @patch('chat.views.ChatMessageView._resolve_user')
    @patch('chat.views.Conversation.objects')
    @patch('chat.views.Question.objects')
    @patch('chat.views.DFConversation.objects')
    @patch('chat.views.DFMessage.objects')
    def test_keyword_routing_is_case_insensitive(self, mock_df_msg, mock_df_conv, mock_q, mock_conv, mock_resolve_user, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = MagicMock()
        mock_resolve_user.return_value = MagicMock()
        mock_conv.create.return_value = MagicMock(conversation_id='conv_123')
        
        response = self.client.post('/api/v1/chat', {'question': 'Build DataFlow Pipeline for chemistry'}, format='json')

        self.assertEqual(response.status_code, 200)
        payload = response.json()['data']
        self.assertEqual(payload['agent'], 'DataFlow-Agent')

    @patch('chat.views.transaction.atomic')
    @patch('chat.views.ChatMessageView._resolve_user')
    @patch('chat.views.Conversation.objects')
    @patch('chat.views.Question.objects')
    @patch('chat.views.DFConversation.objects')
    @patch('chat.views.DFMessage.objects')
    def test_anonymous_sessions_get_distinct_demo_users(self, mock_df_msg, mock_df_conv, mock_q, mock_conv, mock_resolve_user, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = MagicMock()

        # Return a different user mock for each call to simulate distinct users
        user1 = MagicMock()
        user2 = MagicMock()
        mock_resolve_user.side_effect = [user1, user2]

        mock_conv.create.return_value = MagicMock(conversation_id='conv_123')
        mock_df_conv.create.return_value = MagicMock(id=uuid.UUID('e063cb5b-10b8-4b43-91be-65e460e80731'))

        first = self.client.post('/api/v1/chat', {'question': '@DataFlow create pipeline'}, format='json')
        second = self.client.post('/api/v1/chat', {'question': '@DataFlow create pipeline'}, format='json')

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)

        # Verify that Conversation.objects.create was called twice
        self.assertEqual(mock_conv.create.call_count, 2)

        # Verify that it was called with different users
        calls = mock_conv.create.call_args_list
        self.assertEqual(calls[0][1]['user'], user1)
        self.assertEqual(calls[1][1]['user'], user2)
    @patch('chat.views.transaction.atomic')
    @patch('chat.views.ChatMessageView._resolve_user')
    @patch('chat.views.Conversation.objects')
    @patch('chat.views.Question.objects')
    @patch('chat.views.chat_provider.complete')
    def test_plain_chat_uses_llm_provider(self, mock_complete, mock_q, mock_conv, mock_resolve_user, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = MagicMock()
        mock_resolve_user.return_value = MagicMock()
        mock_conv.create.return_value = MagicMock(conversation_id='conv_123')
        
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
