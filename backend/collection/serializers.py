"""
Collection serializers for ADP Backend
"""
from rest_framework import serializers
from .models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    """Collection serializer"""
    
    class Meta:
        model = Collection
        fields = ['id', 'collection_id', 'name', 'description', 'knowledge_bases', 'created_at', 'updated_at']
        read_only_fields = ['id', 'collection_id', 'created_at', 'updated_at']


class CollectionCreateSerializer(serializers.ModelSerializer):
    """Collection creation serializer"""
    
    class Meta:
        model = Collection
        fields = ['name', 'description', 'knowledge_bases']
