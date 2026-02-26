"""
Chat models for ADP Backend
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversation(models.Model):
    """Chat conversation model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    agent_id = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title or f"Conversation {self.conversation_id}"


class Question(models.Model):
    """Chat question/answer model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    collection_and_kbs = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'questions'
        ordering = ['created_at']
    
    def __str__(self):
        return self.question[:50]


class ChatShare(models.Model):
    """Chat share model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    share_id = models.CharField(max_length=100, unique=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='shares')
    question_ids = models.JSONField(default=list)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'chat_shares'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Share {self.share_id}"
