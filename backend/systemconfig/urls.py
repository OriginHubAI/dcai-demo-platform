"""
System Configuration URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemConfigViewSet, AnnouncementViewSet, EmailTemplateViewSet

router = DefaultRouter()
router.register(r'config', SystemConfigViewSet, basename='system-config')
router.register(r'announcement', AnnouncementViewSet, basename='announcement')
router.register(r'email-template', EmailTemplateViewSet, basename='email-template')

urlpatterns = [
    path('', include(router.urls)),
]
