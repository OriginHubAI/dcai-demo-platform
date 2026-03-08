"""
Chat views for ADP Backend
"""
import json
import uuid
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse, StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
import httpx

from .models import Conversation, Question, ChatShare
from .serializers import ConversationSerializer, ConversationCreateSerializer, QuestionSerializer, ChatShareSerializer
from .agent_router import AgentRouter
from .provider import ChatProviderError, OpenAICompatibleChatProvider
from df_conversation.models import DFConversation, DFMessage


chat_provider = OpenAICompatibleChatProvider()


def _normalize_messages(messages):
    normalized = []
    for item in messages or []:
        role = item.get('role')
        content = item.get('content')
        if role not in {'system', 'user', 'assistant'}:
            continue
        if not isinstance(content, str) or not content.strip():
            continue
        normalized.append({
            'role': role,
            'content': content.strip(),
        })
    return normalized


def _sse_event(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


class ConversationViewSet(viewsets.ModelViewSet):
    """Conversation CRUD"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'conversation_id'
    serializer_class = ConversationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Conversation.objects.filter(user=user)
        
        # Filter by list_type
        list_type = self.request.query_params.get('list_type')
        if list_type:
            queryset = queryset.filter(list_type=list_type)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatMessageView(APIView):
    """Send chat message"""
    permission_classes = [AllowAny]

    def _resolve_user(self, request):
        if request.user and request.user.is_authenticated:
            return request.user

        session = getattr(request, 'session', None)
        if session is not None and not session.session_key:
            session.create()
        session_key = getattr(session, 'session_key', None) or uuid.uuid4().hex
        demo_suffix = session_key[:12]

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(
            email=f'demo+{session_key}@dcai.local',
            defaults={
                'username': f'demo_{demo_suffix}',
                'is_active': True,
            },
        )
        return user

    def post(self, request):
        current_user = self._resolve_user(request)
        agent_id = request.data.get('agent_id')
        conversation_id = request.data.get('conversation_id')
        question = request.data.get('question', '')
        messages = _normalize_messages(request.data.get('messages'))
        model = request.data.get('model') or chat_provider.default_model

        route = AgentRouter().route(question)
        collection_and_kbs = request.data.get('collection_and_kbs', [])

        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id, user=current_user)
            except Conversation.DoesNotExist:
                return Response({
                    'code': 100002,
                    'msg': 'Conversation not found',
                    'data': {}
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            conversation = None

        with transaction.atomic():
            if conversation is None:
                conversation = Conversation.objects.create(
                    conversation_id=f"conv_{uuid.uuid4().hex[:8]}",
                    user=current_user,
                    agent_id=agent_id,
                    title=question[:50] if question else "New Chat"
                )

            if route:
                Question.objects.create(
                    conversation=conversation,
                    question=question,
                    answer=route.hint,
                    collection_and_kbs=collection_and_kbs
                )
                df_conversation = DFConversation.objects.create(
                    user=current_user,
                    title=question[:50] or 'DataMaster Route',
                    config={'source_chat_conversation_id': conversation.conversation_id},
                )
                DFMessage.objects.create(
                    conversation=df_conversation,
                    role=DFMessage.Role.USER,
                    content=question,
                )
                DFMessage.objects.create(
                    conversation=df_conversation,
                    role=DFMessage.Role.TOOL,
                    content=route.hint,
                    tool_calls=[{
                        'agent': route.agent_name,
                        'tool': route.tool_name,
                        'tool_input': route.tool_input,
                        'action': route.action,
                        'iframe_url': route.iframe_url,
                        'stream_url': route.stream_url,
                    }],
                )
                return Response({
                    'code': 0,
                    'msg': 'success',
                    'data': {
                        'conversation_id': conversation.conversation_id,
                        'df_conversation_id': str(df_conversation.id),
                        'type': 'tool_call',
                        'agent': route.agent_name,
                        'tool': route.tool_name,
                        'tool_input': route.tool_input,
                        'action': route.action,
                        'iframe_url': route.iframe_url,
                        'stream_url': route.stream_url,
                        'answer': route.hint,
                    }
                })

            question_record = Question.objects.create(
                conversation=conversation,
                question=question,
                collection_and_kbs=collection_and_kbs
            )

        prompt_messages = messages or [{'role': 'user', 'content': question}]

        try:
            completion = chat_provider.complete(prompt_messages, model=model)
        except ChatProviderError as exc:
            return Response({
                'code': 100100,
                'msg': str(exc),
                'data': {},
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except httpx.HTTPError as exc:
            return Response({
                'code': 100101,
                'msg': f'LLM request failed: {exc}',
                'data': {},
            }, status=status.HTTP_502_BAD_GATEWAY)

        question_record.answer = completion.content
        question_record.save(update_fields=['answer'])

        return Response({
            'code': 0,
            'msg': 'success',
            'data': {
                'conversation_id': conversation.conversation_id,
                'answer': completion.content,
                'model': completion.model,
                'usage': completion.usage,
            }
        })


class ChatStreamView(ChatMessageView):
    """Stream chat response as SSE for homepage chat."""

    def post(self, request):
        current_user = self._resolve_user(request)
        question = (request.data.get('question') or '').strip()
        messages = _normalize_messages(request.data.get('messages'))
        model = request.data.get('model') or chat_provider.default_model

        if not question and not messages:
            return JsonResponse({
                'code': 100001,
                'msg': 'question or messages is required',
                'data': {},
            }, status=400)

        if not question and messages:
            question = messages[-1]['content']

        route = AgentRouter().route(question)
        if route:
            def _route_stream():
                yield _sse_event({
                    'type': 'route',
                    'data': {
                        'agent': route.agent_name,
                        'tool': route.tool_name,
                        'action': route.action,
                        'iframe_url': route.iframe_url,
                        'stream_url': route.stream_url,
                        'answer': route.hint,
                    },
                })
                yield _sse_event({'type': 'done'})

            return StreamingHttpResponse(_route_stream(), content_type='text/event-stream; charset=utf-8')

        conversation = Conversation.objects.create(
            conversation_id=f"conv_{uuid.uuid4().hex[:8]}",
            user=current_user,
            title=question[:50] if question else "New Chat",
        )
        question_record = Question.objects.create(
            conversation=conversation,
            question=question,
            collection_and_kbs=request.data.get('collection_and_kbs', []),
        )
        prompt_messages = messages or [{'role': 'user', 'content': question}]

        try:
            chat_provider._require_config()
        except ChatProviderError as exc:
            return JsonResponse({
                'code': 100100,
                'msg': str(exc),
                'data': {},
            }, status=503)

        def _stream():
            collected = ''
            yield _sse_event({
                'type': 'start',
                'conversation_id': conversation.conversation_id,
                'model': model,
            })
            try:
                for chunk in chat_provider.stream(prompt_messages, model=model):
                    collected += chunk
                    yield _sse_event({'type': 'delta', 'content': chunk})
                question_record.answer = collected
                question_record.save(update_fields=['answer'])
                yield _sse_event({
                    'type': 'done',
                    'conversation_id': conversation.conversation_id,
                    'model': model,
                })
            except Exception as exc:  # pragma: no cover - network failure path
                question_record.answer = collected
                question_record.save(update_fields=['answer'])
                yield _sse_event({
                    'type': 'error',
                    'message': f'LLM request failed: {exc}',
                })

        return StreamingHttpResponse(_stream(), content_type='text/event-stream; charset=utf-8')


class ChatModelsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        models = chat_provider.list_models()
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {
                'models': models,
                'default_model': chat_provider.default_model,
            },
        })


class QuestionListView(APIView):
    """Get questions in a conversation"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({
                'code': 100002,
                'msg': 'Conversation not found',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)
        
        questions = conversation.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': serializer.data
        })


class ChatShareViewSet(viewsets.ModelViewSet):
    """Chat share CRUD"""
    serializer_class = ChatShareSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'share_id'
    
    def get_queryset(self):
        return ChatShare.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        share_id = f"share_{uuid.uuid4().hex[:8]}"
        serializer.save(share_id=share_id, created_by=self.request.user)
