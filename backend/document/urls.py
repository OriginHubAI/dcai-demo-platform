"""
Document URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def document_detail(request, kb_type, kb_id, doc_id):
    """Document detail"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def document_search(request):
    """Search documents"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': []}})


@api_view(['GET'])
@permission_classes([AllowAny])
def document_pub_agents(request):
    """Get public agents for document"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': []}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def presigned_url(request):
    """Generate presigned URL"""
    return Response({'code': 0, 'msg': 'success', 'data': {'url': ''}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_url(request, kb_type, kb_id, doc_id):
    """Get document URL"""
    return Response({'code': 0, 'msg': 'success', 'data': {'url': ''}})


urlpatterns = [
    path('documents', document_search, name='document-search'),
    path('documents/<str:kb_type>/<str:kb_id>/<int:doc_id>', document_detail, name='document-detail'),
    path('documents/<str:kb_type>/<str:kb_id>/<int:doc_id>/url', document_url, name='document-url'),
    path('documents/pub-agents', document_pub_agents, name='document-pub-agents'),
    path('documents/presigned-url', presigned_url, name='presigned-url'),
]
