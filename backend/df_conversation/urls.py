"""
DataFlow Conversation URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DFConversationViewSet, DFMessageViewSet

router = DefaultRouter()
router.register(r'conversation', DFConversationViewSet, basename='df-conversation')
router.register(r'message', DFMessageViewSet, basename='df-message')

urlpatterns = [
    path('', include(router.urls)),
]
