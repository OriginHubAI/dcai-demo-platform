"""
Chat views for ADP Backend
"""
import uuid
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q

from .models import Conversation, Question, ChatShare
from .serializers import ConversationSerializer, ConversationCreateSerializer, QuestionSerializer, ChatShareSerializer


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
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Placeholder for chat functionality
        # This would integrate with LLM service
        agent_id = request.data.get('agent_id')
        conversation_id = request.data.get('conversation_id')
        question = request.data.get('question')
        
        # Create or get conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id, user=request.user)
            except Conversation.DoesNotExist:
                return Response({
                    'code': 100002,
                    'msg': 'Conversation not found',
                    'data': {}
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            conversation = Conversation.objects.create(
                conversation_id=f"conv_{uuid.uuid4().hex[:8]}",
                user=request.user,
                agent_id=agent_id,
                title=question[:50] if question else "New Chat"
            )
        
        # Create question
        q = Question.objects.create(
            conversation=conversation,
            question=question,
            collection_and_kbs=request.data.get('collection_and_kbs', [])
        )
        
        # TODO: Integrate with LLM service for streaming response
        # This is a placeholder response
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {
                'conversation_id': conversation.conversation_id,
                'answer': 'This is a placeholder response. Integrate with LLM service for actual chat functionality.'
            }
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
