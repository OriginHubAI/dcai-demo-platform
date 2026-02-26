"""
DataFlow Conversation Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DFConversation, DFMessage
from .serializers import (
    DFConversationSerializer, DFConversationCreateSerializer,
    DFMessageSerializer
)


class DFConversationViewSet(viewsets.ModelViewSet):
    """DataFlow conversation viewset"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = DFConversationSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DFConversationCreateSerializer
        return DFConversationSerializer
    
    def get_queryset(self):
        return DFConversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to the conversation"""
        conversation = self.get_object()
        content = request.data.get('content')
        role = request.data.get('role', DFMessage.Role.USER)
        
        if not content:
            return Response({
                'code': 400,
                'msg': 'Content is required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user message
        message = DFMessage.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            metadata=request.data.get('metadata', {}),
            tool_calls=request.data.get('tool_calls', [])
        )
        
        # Update conversation stats
        conversation.total_messages += 1
        conversation.save(update_fields=['total_messages', 'updated_at'])
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': DFMessageSerializer(message).data
        })
    
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        """Clear all messages in the conversation"""
        conversation = self.get_object()
        conversation.messages.all().delete()
        conversation.total_messages = 0
        conversation.save(update_fields=['total_messages', 'updated_at'])
        
        return Response({'code': 0, 'msg': 'success', 'data': {}})


class DFMessageViewSet(viewsets.ModelViewSet):
    """DataFlow message viewset"""
    
    serializer_class = DFMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DFMessage.objects.filter(
            conversation__user=self.request.user
        ).select_related('conversation')
