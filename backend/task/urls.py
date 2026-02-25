"""
Task URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request, task_id=None):
    """Task list/create"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [], 'total': 0}})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    """Task CRUD"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_create_from_template(request):
    """Create task from template"""
    return Response({'code': 0, 'msg': 'success', 'data': {'task_id': ''}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_start(request, task_id):
    """Start task"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_stop(request, task_id):
    """Stop task"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_resume(request, task_id):
    """Resume task"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_restart(request, task_id):
    """Restart task"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_status(request, task_id):
    """Get task status"""
    return Response({'code': 0, 'msg': 'success', 'data': {'status': 'pending'}})


urlpatterns = [
    path('task', task_list, name='task-list'),
    path('task/<str:task_id>', task_detail, name='task-detail'),
    path('task/<str:task_id>/status', task_status, name='task-status'),
    path('task/<str:task_id>/start', task_start, name='task-start'),
    path('task/<str:task_id>/stop', task_stop, name='task-stop'),
    path('task/<str:task_id>/resume', task_resume, name='task-resume'),
    path('task/<str:task_id>/restart', task_restart, name='task-restart'),
    path('task/create-from-template', task_create_from_template, name='task-create-from-template'),
]
