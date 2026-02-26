"""
LLM Chat URL Configuration
OpenAI-compatible endpoints
"""
from django.urls import path
from . import views

urlpatterns = [
    # OpenAI-compatible endpoints
    path('v1/chat/completions', views.chat_completions, name='chat-completions'),
    path('v1/models', views.list_models, name='list-models'),
    path('v1/embeddings', views.embeddings, name='embeddings'),
]
