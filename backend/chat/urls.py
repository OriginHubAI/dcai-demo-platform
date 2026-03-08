"""
Chat URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'chat/conversations', views.ConversationViewSet, basename='conversation')
router.register(r'chat/share', views.ChatShareViewSet, basename='chat-share')

urlpatterns = [
    path('chat/models', views.ChatModelsView.as_view(), name='chat-models'),
    path('chat/stream', views.ChatStreamView.as_view(), name='chat-stream'),
    path('chat', views.ChatMessageView.as_view(), name='chat-message'),
    path('chat/conversations/<str:conversation_id>/questions', views.QuestionListView.as_view(), name='question-list'),
    path('', include(router.urls)),
]
