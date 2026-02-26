"""
Knowledgebase models for ADP Backend
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class KnowledgeBase(models.Model):
    """Knowledge base model"""
    
    STATUS_CHOICES = [
        ('ready', 'Ready'),
        ('processing', 'Processing'),
        ('error', 'Error'),
        ('pending', 'Pending'),
    ]
    
    TYPE_CHOICES = [
        ('general', 'General'),
        ('domain', 'Domain'),
        ('private', 'Private'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kb_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='knowledge_bases')
    file_count = models.IntegerField(default=0)
    vector_store = models.JSONField(default=dict, blank=True)
    pipeline = models.JSONField(default=dict, blank=True)
    knowledge_graph = models.JSONField(default=dict, blank=True)
    mcp = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'knowledge_bases'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class KnowledgeBaseDocument(models.Model):
    """Knowledge base document model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    knowledge_base = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE, related_name='documents')
    document_id = models.CharField(max_length=100)
    name = models.CharField(max_length=500)
    size = models.BigIntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'kb_documents'
        unique_together = ['knowledge_base', 'document_id']
    
    def __str__(self):
        return self.name
