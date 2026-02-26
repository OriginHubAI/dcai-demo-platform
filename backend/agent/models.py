"""
Agent models for ADP Backend
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Agent(models.Model):
    """Agent model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agents')
    is_public = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    subscribers_count = models.IntegerField(default=0)
    tools = models.JSONField(default=list, blank=True)
    collection_and_kbs = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agents'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class AgentTool(models.Model):
    """Agent tool model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tool_id = models.CharField(max_length=100, unique=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='agent_tools', null=True, blank=True)
    name = models.CharField(max_length=100)
    url = models.URLField()
    openapi_json_path = models.TextField(blank=True, null=True)
    endpoints = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agent_tools'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class AgentSubscription(models.Model):
    """Agent subscription model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_subscriptions')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='subscriptions')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'agent_subscriptions'
        unique_together = ['user', 'agent']
    
    def __str__(self):
        return f"{self.user.email} - {self.agent.title}"
