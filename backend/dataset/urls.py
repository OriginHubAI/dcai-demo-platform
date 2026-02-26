"""
Dataset URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dataset_list(request, dataset_id=None):
    """Dataset list/detail"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [], 'total': 0}})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, dataset_id):
    """Dataset CRUD"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['GET'])
@permission_classes([AllowAny])
def third_party_list(request):
    """Third party datasets"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': []}})


@api_view(['GET'])
@permission_classes([AllowAny])
def third_party_detail(request, dataset_name):
    """Third party dataset detail"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


urlpatterns = [
    path('dataset', dataset_list, name='dataset-list'),
    path('dataset/<str:dataset_id>', dataset_detail, name='dataset-detail'),
    path('third-party/list', third_party_list, name='third-party-list'),
    path('third-party/detail/<str:dataset_name>', third_party_detail, name='third-party-detail'),
]
