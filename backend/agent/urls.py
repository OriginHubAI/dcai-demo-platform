"""
Agent URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'agents', views.AgentViewSet, basename='agent')
router.register(r'agents/tools', views.AgentToolViewSet, basename='agent-tool')

urlpatterns = [
    path('', include(router.urls)),
]
