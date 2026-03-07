"""
Apps URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Sample Apps data
SAMPLE_APPS = [
    {
        'id': 'OpenDCAI/DocDancer-DataGenerator',
        'author': 'OpenDCAI',
        'title': 'DocDancer Data Generator',
        'emoji': '📚',
        'colorFrom': 'amber',
        'colorTo': 'orange',
        'description': 'Generate high-quality reinforcement learning training data for document understanding agents using multi-modal trajectory synthesis and QA generation.',
        'category': 'agent-based',
        'sdk': 'gradio',
        'likes': 3800,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 98000,
        'lastModified': '2025-04-16',
        'tags': ['document-understanding', 'rl-data', 'agent-training', 'multimodal', 'trajectory-synthesis'],
        'license': 'apache-2.0',
    },
    {
        'id': 'OpenDCAI/Open-NotebookLM',
        'author': 'OpenDCAI',
        'title': 'Open-NotebookLM',
        'emoji': '📓',
        'colorFrom': 'indigo',
        'colorTo': 'purple',
        'description': 'Convert PDFs into podcast-style audio conversations using open-source LLMs and TTS models.',
        'category': 'text-generation',
        'sdk': 'gradio',
        'likes': 3200,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 125000,
        'lastModified': '2025-04-15',
        'tags': ['pdf', 'audio', 'tts', 'llm'],
        'license': 'apache-2.0',
    },
    {
        'id': 'SciDCAI/CAD-DataMaster',
        'author': 'SciDCAI',
        'title': 'CAD DataMaster',
        'emoji': '🏗️',
        'colorFrom': 'blue',
        'colorTo': 'cyan',
        'description': 'Comprehensive CAD data processing platform supporting CAD file parsing, format conversion, 3D visualization, and intelligent analysis.',
        'category': 'cad',
        'sdk': 'gradio',
        'likes': 4200,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 89000,
        'lastModified': '2025-04-12',
        'tags': ['cad', '3d', 'visualization', 'engineering'],
        'license': 'mit',
    },
    {
        'id': 'KupasAI/MultiModal-DataAgent',
        'author': 'KupasAI',
        'title': 'MultiModal DataAgent',
        'emoji': '🤖',
        'colorFrom': 'purple',
        'colorTo': 'indigo',
        'description': 'Agent-based multimodal data processing application powered by intelligent agents for handling text, image, audio, and video data.',
        'category': 'agent-based',
        'sdk': 'gradio',
        'likes': 3500,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 156000,
        'lastModified': '2025-04-10',
        'tags': ['multimodal', 'agent', 'image', 'video', 'audio'],
        'license': 'apache-2.0',
    },
    {
        'id': 'OpenDCAI/Paper2Any',
        'author': 'OpenDCAI',
        'title': 'Paper2Any',
        'emoji': '📄',
        'colorFrom': 'blue',
        'colorTo': 'cyan',
        'description': 'Convert academic papers into various formats including podcasts, presentations, and summaries.',
        'category': 'text-generation',
        'sdk': 'gradio',
        'likes': 2800,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 78000,
        'lastModified': '2025-04-08',
        'tags': ['academic', 'paper', 'summary', 'podcast'],
        'license': 'apache-2.0',
    },
    {
        'id': 'HuggingFaceH4/chat-ui',
        'author': 'HuggingFaceH4',
        'title': 'HuggingChat',
        'emoji': '💬',
        'colorFrom': 'yellow',
        'colorTo': 'orange',
        'description': 'Open-source chat interface powered by the best open LLMs available.',
        'category': 'text-generation',
        'sdk': 'docker',
        'likes': 22000,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 1250000,
        'lastModified': '2025-04-14',
        'tags': ['chat', 'llm', 'conversation', 'ui'],
        'license': 'apache-2.0',
    },
    {
        'id': 'OpenDCAI/MCP-VectorSQL',
        'author': 'OpenDCAI',
        'title': 'MCP-VectorSQL',
        'emoji': '🔍',
        'colorFrom': 'green',
        'colorTo': 'teal',
        'description': 'Convert natural language questions into high-quality SQL queries for vector databases.',
        'category': 'text-generation',
        'sdk': 'gradio',
        'likes': 1900,
        'status': 'running',
        'hardware': 'A10G',
        'downloads': 45000,
        'lastModified': '2025-04-05',
        'tags': ['sql', 'vector-database', 'nlp', 'query'],
        'license': 'mit',
    },
    {
        'id': 'OpenDCAI/Dataflow-LoopAI',
        'author': 'OpenDCAI',
        'title': 'DataFlow-LoopAI',
        'emoji': '🔄',
        'colorFrom': 'purple',
        'colorTo': 'pink',
        'description': 'AI-powered dataflow automation tool for building intelligent workflows and pipelines.',
        'category': 'text-generation',
        'sdk': 'gradio',
        'likes': 1500,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 32000,
        'lastModified': '2025-04-11',
        'tags': ['dataflow', 'workflow', 'automation', 'pipeline'],
        'license': 'apache-2.0',
    },
    {
        'id': 'OpenDCAI/Chem-CoT-Generator',
        'author': 'OpenDCAI',
        'title': 'Chemistry CoT Data Generator',
        'emoji': '🧪',
        'colorFrom': 'teal',
        'colorTo': 'green',
        'description': 'Generate high-quality chemical chain-of-thought (CoT) data for training and fine-tuning chemistry-focused LLMs.',
        'category': 'text-generation',
        'sdk': 'gradio',
        'likes': 2100,
        'status': 'running',
        'hardware': 'A100',
        'downloads': 56000,
        'lastModified': '2025-04-13',
        'tags': ['chemistry', 'cot', 'training-data', 'llm'],
        'license': 'apache-2.0',
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])
def apps_list(request):
    """List Apps"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    category = request.query_params.get('category', None)
    sdk = request.query_params.get('sdk', None)
    
    # Filter by category if provided
    filtered_apps = SAMPLE_APPS
    if category:
        filtered_apps = [s for s in filtered_apps if s['category'] == category]
    if sdk:
        filtered_apps = [s for s in filtered_apps if s['sdk'] == sdk]
    
    total = len(filtered_apps)
    start = (page - 1) * page_size
    end = start + page_size
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': filtered_apps[start:end],
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def apps_detail(request, app_id):
    """Get App detail"""
    app = next((s for s in SAMPLE_APPS if s['id'] == app_id), None)
    
    if app:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': app
        })
    
    return Response({
        'code': 404,
        'msg': 'app not found',
        'data': {}
    })


urlpatterns = [
    path('apps', apps_list, name='apps-list'),
    path('apps/<str:app_id>', apps_detail, name='apps-detail'),
]
