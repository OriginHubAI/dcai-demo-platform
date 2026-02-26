"""
Spaces (Apps) URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Sample Spaces (Apps) data
SAMPLE_SPACES = [
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
def spaces_list(request):
    """List Spaces (Apps)"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    category = request.query_params.get('category', None)
    sdk = request.query_params.get('sdk', None)
    
    # Filter by category if provided
    filtered_spaces = SAMPLE_SPACES
    if category:
        filtered_spaces = [s for s in filtered_spaces if s['category'] == category]
    if sdk:
        filtered_spaces = [s for s in filtered_spaces if s['sdk'] == sdk]
    
    total = len(filtered_spaces)
    start = (page - 1) * page_size
    end = start + page_size
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': filtered_spaces[start:end],
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def spaces_detail(request, space_id):
    """Get Space detail"""
    space = next((s for s in SAMPLE_SPACES if s['id'] == space_id), None)
    
    if space:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': space
        })
    
    return Response({
        'code': 404,
        'msg': 'space not found',
        'data': {}
    })


urlpatterns = [
    path('spaces', spaces_list, name='spaces-list'),
    path('spaces/<str:space_id>', spaces_detail, name='spaces-detail'),
]