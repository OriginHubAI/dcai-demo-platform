"""
Collection models for ADP Backend
"""
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Collection(models.Model):
    """Collection model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')
    knowledge_bases = models.JSONField(default=list)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collections'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class CollectionDocument(models.Model):
    """Collection document model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='documents')
    document_id = models.CharField(max_length=100)
    kb_id = models.CharField(max_length=100)
    added_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'collection_documents'
        unique_together = ['collection', 'document_id']
    
    def __str__(self):
        return f"{self.collection.name} - {self.document_id}"
