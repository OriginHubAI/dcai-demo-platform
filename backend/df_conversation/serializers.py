"""
DataFlow Conversation Serializers
"""
from rest_framework import serializers
from .models import DFConversation, DFMessage


class DFMessageSerializer(serializers.ModelSerializer):
    """DataFlow message serializer"""
    
    class Meta:
        model = DFMessage
        fields = ['id', 'role', 'content', 'metadata', 'tool_calls', 'created_at']
        read_only_fields = ['id', 'created_at']


class DFConversationSerializer(serializers.ModelSerializer):
    """DataFlow conversation serializer"""
    
    messages = DFMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = DFConversation
        fields = [
            'id', 'title', 'status', 'config', 'total_messages',
            'messages', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_messages', 'created_at', 'updated_at']


class DFConversationCreateSerializer(serializers.ModelSerializer):
    """DataFlow conversation create serializer"""
    
    class Meta:
        model = DFConversation
        fields = ['title', 'config']
