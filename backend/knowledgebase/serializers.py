"""
Knowledgebase serializers for ADP Backend
"""
from rest_framework import serializers
from .models import KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    """Knowledge base serializer"""
    
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'kb_id', 'name', 'description', 'type', 'status', 'owner',
                  'file_count', 'vector_store', 'pipeline', 'knowledge_graph', 'mcp',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'kb_id', 'file_count', 'created_at', 'updated_at']


class KnowledgeBaseCreateSerializer(serializers.ModelSerializer):
    """Knowledge base creation serializer"""
    
    class Meta:
        model = KnowledgeBase
        fields = ['name', 'description', 'type']
