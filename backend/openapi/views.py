"""
OpenAPI Views
"""
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OpenAPIKey, OpenAPIAccessLog
from .serializers import (
    OpenAPIKeySerializer, OpenAPIKeyCreateSerializer,
    OpenAPIKeyDetailSerializer, OpenAPIAccessLogSerializer
)


class OpenAPIKeyViewSet(viewsets.ModelViewSet):
    """OpenAPI key viewset"""
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OpenAPIKeyCreateSerializer
        if self.action == 'retrieve':
            return OpenAPIKeyDetailSerializer
        return OpenAPIKeySerializer
    
    def get_queryset(self):
        return OpenAPIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def regenerate(self, request, pk=None):
        """Regenerate API key"""
        api_key = self.get_object()
        new_key = api_key.regenerate()
        return Response({
            'code': 0,
            'msg': 'success',
            'data': {'key': new_key}
        })
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Toggle API key status"""
        api_key = self.get_object()
        if api_key.status == OpenAPIKey.Status.ACTIVE:
            api_key.status = OpenAPIKey.Status.INACTIVE
        else:
            api_key.status = OpenAPIKey.Status.ACTIVE
        api_key.save(update_fields=['status', 'updated_at'])
        
        serializer = self.get_serializer(api_key)
        return Response({'code': 0, 'msg': 'success', 'data': serializer.data})
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Get API key access logs"""
        api_key = self.get_object()
        logs = OpenAPIAccessLog.objects.filter(api_key=api_key).order_by('-created_at')[:100]
        serializer = OpenAPIAccessLogSerializer(logs, many=True)
        return Response({'code': 0, 'msg': 'success', 'data': serializer.data})


class OpenAPIAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    """OpenAPI access log viewset"""
    
    serializer_class = OpenAPIAccessLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see logs for their own API keys
        return OpenAPIAccessLog.objects.filter(
            api_key__user=self.request.user
        ).select_related('api_key')
