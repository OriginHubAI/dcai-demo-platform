"""
Organization URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def organization_create(request):
    """Create organization"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_list(request):
    """List organizations"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': []}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organization_detail(request, org_id):
    """Organization detail"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def organization_update(request, org_id):
    """Update organization"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def organization_delete(request, org_id):
    """Delete organization"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


urlpatterns = [
    path('organization/create', organization_create, name='organization-create'),
    path('organization/list', organization_list, name='organization-list'),
    path('organization/<str:org_id>', organization_detail, name='organization-detail'),
    path('organization/<str:org_id>/update', organization_update, name='organization-update'),
    path('organization/<str:org_id>/delete', organization_delete, name='organization-delete'),
]
