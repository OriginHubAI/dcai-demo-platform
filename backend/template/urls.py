"""
Template URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def template_list(request, template_id=None):
    """Template list/create"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [], 'total': 0}})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def template_detail(request, template_id):
    """Template CRUD"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


urlpatterns = [
    path('templates', template_list, name='template-list'),
    path('templates/<int:config_id>', template_detail, name='template-detail'),
]
