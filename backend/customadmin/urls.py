"""
Custom Admin URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/stats', views.dashboard_stats, name='admin-dashboard-stats'),
    path('system/health', views.system_health, name='admin-system-health'),
    path('users', views.user_list, name='admin-user-list'),
    path('users/<uuid:user_id>/action', views.user_action, name='admin-user-action'),
    path('analytics', views.analytics, name='admin-analytics'),
]
