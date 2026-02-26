"""
System Configuration Serializers
"""
from rest_framework import serializers
from .models import SystemConfig, Announcement, EmailTemplate


class SystemConfigSerializer(serializers.ModelSerializer):
    """System configuration serializer"""
    
    class Meta:
        model = SystemConfig
        fields = [
            'id', 'key', 'value', 'type', 'description',
            'is_public', 'is_system', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemConfigCreateSerializer(serializers.ModelSerializer):
    """System configuration create serializer"""
    
    class Meta:
        model = SystemConfig
        fields = ['key', 'value', 'type', 'description', 'is_public']


class AnnouncementSerializer(serializers.ModelSerializer):
    """Announcement serializer"""
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'status', 'priority',
            'start_time', 'end_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmailTemplateSerializer(serializers.ModelSerializer):
    """Email template serializer"""
    
    class Meta:
        model = EmailTemplate
        fields = [
            'id', 'name', 'subject', 'body', 'variables',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
