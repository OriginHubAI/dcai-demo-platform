"""
Agent serializers for ADP Backend
"""
from rest_framework import serializers
from .models import Agent, AgentTool, AgentSubscription


class AgentSerializer(serializers.ModelSerializer):
    """Agent serializer"""
    
    owner_email = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = Agent
        fields = ['id', 'agent_id', 'title', 'description', 'type', 'owner', 'owner_email',
                  'is_public', 'is_published', 'subscribers_count', 'tools', 
                  'collection_and_kbs', 'created_at', 'updated_at', 'is_subscribed']
        read_only_fields = ['id', 'owner', 'subscribers_count', 'created_at', 'updated_at']
    
    def get_owner_email(self, obj):
        return obj.owner.email
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AgentSubscription.objects.filter(
                user=request.user, 
                agent=obj
            ).exists()
        return False


class AgentCreateSerializer(serializers.ModelSerializer):
    """Agent creation serializer"""
    
    class Meta:
        model = Agent
        fields = ['title', 'description', 'type', 'tools', 'collection_and_kbs']
    
    def create(self, validated_data):
        import uuid
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        validated_data['agent_id'] = agent_id
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class AgentToolSerializer(serializers.ModelSerializer):
    """Agent tool serializer"""
    
    class Meta:
        model = AgentTool
        fields = ['id', 'tool_id', 'agent', 'name', 'url', 'openapi_json_path', 'endpoints', 'created_at', 'updated_at']
        read_only_fields = ['id', 'tool_id', 'created_at', 'updated_at']


class AgentToolCreateSerializer(serializers.ModelSerializer):
    """Agent tool creation serializer"""
    
    class Meta:
        model = AgentTool
        fields = ['agent_id', 'name', 'url', 'openapi_json_path', 'endpoints']
    
    def create(self, validated_data):
        import uuid
        tool_id = f"tool_{uuid.uuid4().hex[:8]}"
        validated_data['tool_id'] = tool_id
        return super().create(validated_data)
