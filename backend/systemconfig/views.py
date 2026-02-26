"""
System Configuration Views
"""
from django.db import models
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import SystemConfig, Announcement, EmailTemplate
from .serializers import (
    SystemConfigSerializer, SystemConfigCreateSerializer,
    AnnouncementSerializer, EmailTemplateSerializer
)


class SystemConfigViewSet(viewsets.ModelViewSet):
    """System configuration viewset"""
    
    queryset = SystemConfig.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SystemConfigCreateSerializer
        return SystemConfigSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'public_config']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by key
        key = self.request.query_params.get('key')
        if key:
            queryset = queryset.filter(key__icontains=key)
        
        # Public configs can be accessed by anyone
        # Private configs only by admin
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_public=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def public_config(self, request):
        """Get public configuration"""
        configs = SystemConfig.objects.filter(is_public=True)
        serializer = self.get_serializer(configs, many=True)
        
        # Convert to key-value dict
        result = {}
        for item in serializer.data:
            result[item['key']] = item['value']
        
        return Response({'code': 0, 'msg': 'success', 'data': result})


class AnnouncementViewSet(viewsets.ModelViewSet):
    """Announcement viewset"""
    
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'active']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-admin users only see published announcements
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=Announcement.Status.PUBLISHED)
            
            # Filter by time
            now = timezone.now()
            queryset = queryset.filter(
                models.Q(start_time__isnull=True) | models.Q(start_time__lte=now),
                models.Q(end_time__isnull=True) | models.Q(end_time__gte=now)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active announcements"""
        now = timezone.now()
        announcements = Announcement.objects.filter(
            status=Announcement.Status.PUBLISHED,
        ).filter(
            models.Q(start_time__isnull=True) | models.Q(start_time__lte=now),
            models.Q(end_time__isnull=True) | models.Q(end_time__gte=now)
        ).order_by('-priority', '-created_at')
        
        serializer = self.get_serializer(announcements, many=True)
        return Response({'code': 0, 'msg': 'success', 'data': serializer.data})


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """Email template viewset"""
    
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
