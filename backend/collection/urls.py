"""
Collection URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'collections', views.CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]
