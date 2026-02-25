"""
Agent views for ADP Backend
"""
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q

from .models import Agent, AgentTool, AgentSubscription
from .serializers import AgentSerializer, AgentCreateSerializer, AgentToolSerializer, AgentToolCreateSerializer


class AgentViewSet(viewsets.ModelViewSet):
    """Agent CRUD"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'agent_id'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AgentCreateSerializer
        return AgentSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Agent.objects.all()
        
        # Filter by list_type
        list_type = self.request.query_params.get('list_type')
        if list_type == 'my':
            queryset = queryset.filter(owner=user)
        elif list_type == 'share':
            queryset = queryset.filter(is_public=True)
        
        # Search by keyword
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | 
                Q(description__icontains=keyword)
            )
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def subscribe(self, request, agent_id=None):
        """Subscribe to an agent"""
        agent = self.get_object()
        action = int(request.data.get('action', 1))
        
        if action == 1:  # Subscribe
            subscription, created = AgentSubscription.objects.get_or_create(
                user=request.user,
                agent=agent
            )
            if created:
                agent.subscribers_count += 1
                agent.save()
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {'subscribed': True}
            })
        else:  # Unsubscribe
            AgentSubscription.objects.filter(
                user=request.user,
                agent=agent
            ).delete()
            if agent.subscribers_count > 0:
                agent.subscribers_count -= 1
                agent.save()
            return Response({
                'code': 0,
                'msg': 'success',
                'data': {'subscribed': False}
            })


class AgentToolViewSet(viewsets.ModelViewSet):
    """Agent tool CRUD"""
    serializer_class = AgentToolSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'tool_id'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AgentToolCreateSerializer
        return AgentToolSerializer
    
    def get_queryset(self):
        return AgentTool.objects.all()
    
    def perform_create(self, serializer):
        tool_id = f"tool_{uuid.uuid4().hex[:8]}"
        serializer.save(tool_id=tool_id)
