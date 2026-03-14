"""
Chat serializers for ADP Backend
"""
from rest_framework import serializers
from .models import Conversation, Question, ChatShare


class ConversationSerializer(serializers.ModelSerializer):
    """Conversation serializer"""
    
    class Meta:
        model = Conversation
        fields = ['id', 'conversation_id', 'agent_id', 'title', 'created_at', 'updated_at']
        read_only_fields = ['id', 'conversation_id', 'created_at', 'updated_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Conversation creation serializer"""

    class Meta:
        model = Conversation
        fields = ['agent_id', 'title']
    
    def create(self, validated_data):
        import uuid
        conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        validated_data['conversation_id'] = conversation_id
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer"""
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'answer', 'collection_and_kbs', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChatShareSerializer(serializers.ModelSerializer):
    """Chat share serializer"""
    
    class Meta:
        model = ChatShare
        fields = ['id', 'share_id', 'conversation', 'question_ids', 'created_by', 'created_at']
        read_only_fields = ['id', 'share_id', 'created_by', 'created_at']
