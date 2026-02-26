"""
OpenAPI URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpenAPIKeyViewSet, OpenAPIAccessLogViewSet

router = DefaultRouter()
router.register(r'apikey', OpenAPIKeyViewSet, basename='openapi-key')
router.register(r'logs', OpenAPIAccessLogViewSet, basename='openapi-log')

urlpatterns = [
    path('', include(router.urls)),
]
