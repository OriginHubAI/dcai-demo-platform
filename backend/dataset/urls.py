"""
Dataset URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .hf_views import hf_list_datasets, hf_dataset_metadata, hf_resolve_file


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
    # Standard dataset APIs
    path('dataset', dataset_list, name='dataset-list'),
    path('dataset/<str:dataset_id>', dataset_detail, name='dataset-detail'),
    path('third-party/list', third_party_list, name='third-party-list'),
    path('third-party/detail/<str:dataset_name>', third_party_detail, name='third-party-detail'),
    
    # HF-compatible hub APIs
    # These are usually expected at /api/datasets or /api/datasets/ namespace
    path('hf/api/datasets', hf_list_datasets, name='hf-list-datasets'),
    path('hf/api/datasets/<str:namespace>/<str:dataset_name>', hf_dataset_metadata, name='hf-dataset-metadata'),
    path('hf/datasets/<str:namespace>/<str:dataset_name>/resolve/<str:revision>/<path:path>', hf_resolve_file, name='hf-resolve-file'),
]
