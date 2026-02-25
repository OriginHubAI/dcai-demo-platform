"""
Third Party URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # Webhooks (no auth required)
    path('webhook/github', views.webhook_github, name='webhook-github'),
    path('webhook/slack', views.webhook_slack, name='webhook-slack'),
    path('webhook/discord', views.webhook_discord, name='webhook-discord'),
    
    # Integrations
    path('integrations', views.integrations_list, name='integrations-list'),
    path('oauth/connect', views.oauth_connect, name='oauth-connect'),
    path('oauth/disconnect/<str:provider>', views.oauth_disconnect, name='oauth-disconnect'),
]
