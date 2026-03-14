"""
Main URL Configuration for ADP Backend
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import services_health
from dataset.hf_views import hf_list_datasets, hf_dataset_metadata, hf_resolve_file, hf_parquet_list, hf_dataset_info

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', lambda request: __import__('django.http', fromlist=['HttpResponse']).HttpResponse('OK'), name='health'),
    path('api/v2/services/health', services_health, name='services-health'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # HF-compatible hub APIs
    path('api/hf/', include('dataset.hf_urls')),

    # API v1 endpoints
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('agent.urls')),
    path('api/v1/', include('chat.urls')),
    path('api/v1/', include('collection.urls')),
    path('api/v1/', include('knowledgebase.urls')),
    path('api/v1/', include('document.urls')),
    path('api/v1/', include('dataset.urls')),
    path('api/v1/', include('task.urls')),
    path('api/v1/', include('template.urls')),
    path('api/v1/', include('organization.urls')),
    path('api/v1/', include('systemconfig.urls')),
    path('api/v1/', include('openapi.urls')),
    path('api/v1/', include('df_conversation.urls')),
    path('api/v1/', include('third_party.urls')),
    
    # API v2 endpoints
    path('api/v2/', include('dataset.urls_v2')),
    path('api/v2/', include('task.urls_v2')),
    path('api/v2/dataflow/', include('df.urls')),
    path('api/v2/loopai/', include('loopai_proxy.urls')),
    path('api/v2/dfagent/', include('dfagent_proxy.urls')),
    path('api/v2/', include('knowledgebase.urls')),
    path('api/v2/', include('apps.urls')),
    
    # API admin endpoints
    path('api/admin/', include('customadmin.urls')),
    
    # LLM Chat
    path('llm_chat/', include('llm_chat.urls')),
    
    # Train
    path('api/v1/train/', include('train.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
