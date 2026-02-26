"""
Example URL Configuration showing how to route Django API to FastAPI
Copy the relevant parts to your urls.py
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Import the proxy view
from fastapi_proxy import FastAPIProxyView, FastAPIAgentProxyView, FastAPITaskProxyView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health check
    path('health/', lambda request: __import__('django.http', fromlist=['HttpResponse']).HttpResponse('OK'), name='health'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API v1 endpoints - Original Django implementations
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
    # Option 1: Proxy to FastAPI (using proxy view)
    path('api/v2/agents/', FastAPIAgentProxyView.as_view()),
    path('api/v2/tasks/', FastAPITaskProxyView.as_view()),
    
    # Option 2: Keep Django v2 endpoints for gradual migration
    path('api/v2/', include('dataset.urls_v2')),
    path('api/v2/', include('task.urls_v2')),
    
    # Option 3: Generic proxy for any path
    path('api/v2/fastapi/<path:path>', FastAPIProxyView.as_view()),
    
    # API admin endpoints
    path('api/admin/', include('customadmin.urls')),
    
    # LLM Chat
    path('llm_chat/', include('llm_chat.urls')),
    
    # Train
    path('api/v1/train/', include('train.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
