"""
DataFlow Conversation Models
"""
import uuid
from django.db import models
from django.conf import settings


class DFConversation(models.Model):
    """DataFlow conversation model"""
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='df_conversations'
    )
    title = models.CharField(max_length=255, default='Untitled Conversation')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    config = models.JSONField(default=dict, help_text='Conversation configuration')
    total_messages = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'df_conversation'
        verbose_name = 'DataFlow Conversation'
        verbose_name_plural = 'DataFlow Conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title


class DFMessage(models.Model):
    """DataFlow conversation message model"""
    
    class Role(models.TextChoices):
        USER = 'user', 'User'
        ASSISTANT = 'assistant', 'Assistant'
        SYSTEM = 'system', 'System'
        TOOL = 'tool', 'Tool'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        DFConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    tool_calls = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'df_message'
        verbose_name = 'DataFlow Message'
        verbose_name_plural = 'DataFlow Messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
