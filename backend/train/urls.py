"""
Train URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('start', views.start_training, name='train-start'),
    path('status/<uuid:job_id>', views.training_status, name='train-status'),
    path('cancel/<uuid:job_id>', views.cancel_training, name='train-cancel'),
    path('history', views.training_history, name='train-history'),
    path('config', views.training_config, name='train-config'),
]
