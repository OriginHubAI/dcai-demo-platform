"""
User models for ADP Backend
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=128, blank=True, null=True)
    avatar = models.URLField(max_length=4096, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Extended fields from pg_schema
    register_source = models.JSONField(default=dict, blank=True, null=True)
    inviter_id = models.CharField(max_length=36, blank=True, null=True)
    extension = models.JSONField(default=dict, blank=True, null=True)
    api_key = models.CharField(max_length=255, default='', blank=True)
    
    # OAuth fields
    wechat_avatar = models.CharField(max_length=4096, blank=True, null=True)
    wechat_openid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    wechat_unionid = models.CharField(max_length=128, unique=True, blank=True, null=True)
    
    # Legacy/External IDs
    user_id = models.IntegerField(unique=True, blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    
    # GitHub OAuth fields
    github_avatar = models.CharField(max_length=4096, blank=True, null=True)
    github_email = models.EmailField(blank=True, null=True)
    github_id = models.CharField(max_length=64, unique=True, blank=True, null=True)
    github_login = models.CharField(max_length=128, blank=True, null=True)
    
    is_virtual_api_user = models.BooleanField(default=False)
    
    # Override first_name and last_name from AbstractUser to be nullable
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'my_user'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email or self.username
    
    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name or ''} {self.last_name or ''}".strip()
        return self.nickname or self.email or self.username
    
    @property
    def name(self):
        return self.get_full_name()


class InviteCode(models.Model):
    """Invite code model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    max_uses = models.IntegerField(default=1)
    used_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invite_codes')
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invite_code'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def is_exhausted(self):
        return self.used_count >= self.max_uses


class VerificationCode(models.Model):
    """Verification code model for email/phone verification"""
    
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]
    
    PURPOSE_CHOICES = [
        ('register', 'Register'),
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'verification_codes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.type}: {self.email or self.phone} - {self.code}"
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class EmailVerificationCode(models.Model):
    """Specific model for email verification codes as per schema references"""
    
    # SQL uses bigint primary key
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'email_verification_code'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.code}"


class Feedback(models.Model):
    """User feedback model"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    contact = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'feedbacks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback from {self.user.email}"
