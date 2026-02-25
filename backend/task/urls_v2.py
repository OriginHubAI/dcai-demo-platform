"""
Task V2 URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_list_v2(request):
    """List tasks V2"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    task_type = request.query_params.get('type')
    status = request.query_params.get('status')
    search = request.query_params.get('search')
    
    # Placeholder response
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': [],
            'total': 0,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create_v2(request):
    """Create task V2"""
    task_type = request.data.get('type')
    config = request.data.get('config', {})
    
    if not task_type:
        return Response({
            'code': 400,
            'msg': 'type is required',
            'data': {}
        })
    
    # Placeholder response
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'id': 'new-task-id',
            'type': task_type,
            'status': 'pending',
            'config': config,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_detail_v2(request, task_id):
    """Get task detail V2"""
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'id': task_id,
            'type': 'data_processing',
            'status': 'running',
            'progress': 50,
            'result': {},
        }
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def task_delete_v2(request, task_id):
    """Delete task V2"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


urlpatterns = [
    path('tasks', task_list_v2, name='task-list-v2'),
    path('tasks/create', task_create_v2, name='task-create-v2'),
    path('tasks/<str:task_id>', task_detail_v2, name='task-detail-v2'),
    path('tasks/<str:task_id>/delete', task_delete_v2, name='task-delete-v2'),
]
