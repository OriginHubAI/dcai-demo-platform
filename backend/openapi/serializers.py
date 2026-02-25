"""
OpenAPI Serializers
"""
from rest_framework import serializers
from .models import OpenAPIKey, OpenAPIAccessLog


class OpenAPIKeySerializer(serializers.ModelSerializer):
    """OpenAPI key serializer"""
    
    class Meta:
        model = OpenAPIKey
        fields = [
            'id', 'name', 'key', 'key_type', 'status',
            'rate_limit', 'expires_at', 'last_used_at',
            'usage_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'key', 'usage_count', 'last_used_at', 'created_at', 'updated_at']


class OpenAPIKeyCreateSerializer(serializers.ModelSerializer):
    """OpenAPI key create serializer"""
    
    class Meta:
        model = OpenAPIKey
        fields = ['name', 'key_type', 'rate_limit', 'expires_at']


class OpenAPIKeyDetailSerializer(serializers.ModelSerializer):
    """OpenAPI key detail serializer with full key"""
    
    class Meta:
        model = OpenAPIKey
        fields = [
            'id', 'name', 'key', 'key_type', 'status',
            'rate_limit', 'expires_at', 'last_used_at',
            'usage_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'key', 'usage_count', 'last_used_at', 'created_at', 'updated_at']


class OpenAPIAccessLogSerializer(serializers.ModelSerializer):
    """OpenAPI access log serializer"""
    
    class Meta:
        model = OpenAPIAccessLog
        fields = [
            'id', 'method', 'path', 'query_params',
            'response_status', 'response_time', 'ip_address',
            'user_agent', 'created_at'
        ]
        read_only_fields = fields
