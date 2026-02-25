"""
OpenAPI Models
"""
import uuid
import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone


class OpenAPIKey(models.Model):
    """OpenAPI key model for external API access"""
    
    class KeyType(models.TextChoices):
        READ = 'read', 'Read Only'
        WRITE = 'write', 'Read & Write'
        ADMIN = 'admin', 'Admin'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        EXPIRED = 'expired', 'Expired'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='openapi_keys'
    )
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=64, unique=True, db_index=True)
    key_hash = models.CharField(max_length=128, blank=True, default='')
    key_type = models.CharField(max_length=20, choices=KeyType.choices, default=KeyType.READ)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    rate_limit = models.IntegerField(default=100, help_text='Requests per minute')
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'openapi_key'
        verbose_name = 'OpenAPI Key'
        verbose_name_plural = 'OpenAPI Keys'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self._generate_key()
        super().save(*args, **kwargs)
    
    def _generate_key(self):
        """Generate a secure API key"""
        return f"sk-{secrets.token_urlsafe(32)}"
    
    def regenerate(self):
        """Regenerate the API key"""
        self.key = self._generate_key()
        self.usage_count = 0
        self.save(update_fields=['key', 'usage_count', 'updated_at'])
        return self.key
    
    def is_valid(self):
        """Check if the key is valid"""
        if self.status != self.Status.ACTIVE:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            self.status = self.Status.EXPIRED
            self.save(update_fields=['status'])
            return False
        return True


class OpenAPIAccessLog(models.Model):
    """OpenAPI access log"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.ForeignKey(
        OpenAPIKey,
        on_delete=models.CASCADE,
        related_name='access_logs'
    )
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=500)
    query_params = models.JSONField(default=dict, blank=True)
    request_body = models.TextField(blank=True, default='')
    response_status = models.IntegerField()
    response_time = models.IntegerField(help_text='Response time in milliseconds')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'openapi_access_log'
        verbose_name = 'OpenAPI Access Log'
        verbose_name_plural = 'OpenAPI Access Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['api_key', '-created_at']),
        ]
