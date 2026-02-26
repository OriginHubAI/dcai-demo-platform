"""
Task V2 URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


# Sample task data for API mode
SAMPLE_TASKS = [
    {
        'id': 'task-027',
        'name': 'Qwen3 8B Performance Evaluation',
        'dataset': 'open-eval/general-benchmark',
        'package': 'ModelEvaluation',
        'type': 'Model Evaluation',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2026-02-07T10:00:00Z',
        'endedAt': '2026-02-07T12:30:00Z',
        'duration': '2h 30m',
        'author': 'zhangwei',
    },
    {
        'id': 'task-028',
        'name': 'LLaMA3 70B Benchmark Evaluation',
        'dataset': 'open-eval/reasoning-benchmark',
        'package': 'ModelEvaluation',
        'type': 'Model Evaluation',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2026-02-06T14:00:00Z',
        'endedAt': '2026-02-06T18:45:00Z',
        'duration': '4h 45m',
        'author': 'liuna',
    },
    {
        'id': 'task-029',
        'name': 'Qwen3 8B Med-SFT Evaluation',
        'dataset': 'open-eval/medical-benchmark',
        'package': 'ModelEvaluation-Med',
        'type': 'Model Evaluation',
        'status': 'running',
        'progress': 45,
        'startedAt': '2026-02-08T11:00:00Z',
        'endedAt': None,
        'duration': None,
        'author': 'wangfang',
    },
    {
        'id': 'task-025',
        'name': 'Qwen3 8B',
        'dataset': 'arxiv-community/arxiv-stem-papers',
        'package': 'ModelTuning',
        'baseModel': 'Qwen3-8B',
        'type': 'Model Tuning',
        'status': 'running',
        'progress': 42,
        'startedAt': '2026-02-08T13:30:00Z',
        'endedAt': None,
        'duration': None,
        'author': 'zhangwei',
    },
    {
        'id': 'task-001',
        'name': 'Protein Structure Feature Extraction',
        'dataset': 'alphafold-community/protein-structures-3d',
        'package': 'DataFlow-Material',
        'type': 'Data Processing',
        'status': 'running',
        'progress': 72,
        'startedAt': '2026-02-08T09:15:00Z',
        'endedAt': None,
        'duration': None,
        'author': 'zhangwei',
    },
    {
        'id': 'task-002',
        'name': 'RNA Sequence Classification Pipeline',
        'dataset': 'bioinfo-hub/rna-sequences',
        'package': 'DataFlow',
        'type': 'Data Processing',
        'status': 'running',
        'progress': 45,
        'startedAt': '2026-02-08T10:02:00Z',
        'endedAt': None,
        'duration': None,
        'author': 'liuna',
    },
    {
        'id': 'task-006',
        'name': 'Drug Molecule ADMET Annotation',
        'dataset': 'pharma-ai/drug-molecule-graphs',
        'package': 'DataFlow',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2026-02-07T09:10:00Z',
        'endedAt': '2026-02-07T11:48:00Z',
        'duration': '2h 38m',
        'author': 'liuna',
    },
    {
        'id': 'task-011',
        'name': 'Neuroscience EEG Signal Preprocessing',
        'dataset': 'brain-data-lab/neuroscience-eeg',
        'package': 'DataFlow-TimeSeries',
        'type': 'Data Processing',
        'status': 'failed',
        'progress': 63,
        'startedAt': '2026-02-07T13:00:00Z',
        'endedAt': '2026-02-07T14:10:00Z',
        'duration': '1h 10m',
        'author': 'chenming',
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])  # Allow any for demo purposes
# @permission_classes([IsAuthenticated])
def task_list_v2(request):
    """List tasks V2"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    task_type = request.query_params.get('type')
    status = request.query_params.get('status')
    search = request.query_params.get('search')
    
    # Filter tasks
    tasks = SAMPLE_TASKS.copy()
    
    if task_type:
        tasks = [t for t in tasks if t['type'].lower().replace(' ', '_') == task_type.lower()]
    
    if status:
        tasks = [t for t in tasks if t['status'].lower() == status.lower()]
    
    if search:
        search_lower = search.lower()
        tasks = [t for t in tasks if 
                 search_lower in t['name'].lower() or 
                 search_lower in t['dataset'].lower() or
                 search_lower in t['package'].lower()]
    
    total = len(tasks)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_tasks = tasks[start:end]
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': paginated_tasks,
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any for demo purposes
# @permission_classes([IsAuthenticated])
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
@permission_classes([AllowAny])  # Allow any for demo purposes
# @permission_classes([IsAuthenticated])
def task_detail_v2(request, task_id):
    """Get task detail V2"""
    # Find task by ID
    task = next((t for t in SAMPLE_TASKS if t['id'] == task_id), None)
    
    if task:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': task
        })
    
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
@permission_classes([AllowAny])  # Allow any for demo purposes
# @permission_classes([IsAuthenticated])
def task_delete_v2(request, task_id):
    """Delete task V2"""
    return Response({'code': 0, 'msg': 'success', 'data': {}})


urlpatterns = [
    path('tasks', task_list_v2, name='task-list-v2'),
    path('tasks/create', task_create_v2, name='task-create-v2'),
    path('tasks/<str:task_id>', task_detail_v2, name='task-detail-v2'),
    path('tasks/<str:task_id>/delete', task_delete_v2, name='task-delete-v2'),
]
