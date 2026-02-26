"""
Knowledge Base URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Sample knowledge base data
SAMPLE_KNOWLEDGE_BASES = [
    {
        'id': 'kb-medical-research',
        'name': 'Medical Research Papers',
        'description': 'Comprehensive collection of medical research papers covering clinical trials, drug discovery, and treatment protocols.',
        'author': 'medical-ai-team',
        'status': 'ready',
        'type': 'academic',
        'lastModified': '2025-04-15T10:30:00Z',
        'vectorStore': {
            'type': 'chroma',
            'vectorCount': 125000
        },
        'documents': {
            'total': 8500,
            'processed': 8500,
            'indexed': 8500
        },
        'sources': [
            { 'type': 'dataset', 'id': 'clinical-trials-nlp', 'name': 'Clinical Trials NLP' },
            { 'type': 'dataset', 'id': 'medicine-textbooks', 'name': 'Medicine TextBooks' }
        ]
    },
    {
        'id': 'kb-materials-science',
        'name': 'Materials Science Corpus',
        'description': 'Research papers and datasets on materials science including crystal structures, properties, and computational models.',
        'author': 'materials-ai-lab',
        'status': 'ready',
        'type': 'academic',
        'lastModified': '2025-04-12T14:20:00Z',
        'vectorStore': {
            'type': 'chroma',
            'vectorCount': 89000
        },
        'documents': {
            'total': 6200,
            'processed': 6200,
            'indexed': 6200
        },
        'sources': [
            { 'type': 'dataset', 'id': 'materials-genome', 'name': 'Materials Genome' },
            { 'type': 'dataset', 'id': 'iron-steel-papers', 'name': 'Iron & Steel Papers' }
        ]
    },
    {
        'id': 'kb-biology-research',
        'name': 'Biology Research Collection',
        'description': 'Biological research data including protein structures, RNA sequences, and genomic variants.',
        'author': 'bio-ai-team',
        'status': 'ready',
        'type': 'academic',
        'lastModified': '2025-04-10T09:15:00Z',
        'vectorStore': {
            'type': 'chroma',
            'vectorCount': 210000
        },
        'documents': {
            'total': 15000,
            'processed': 15000,
            'indexed': 15000
        },
        'sources': [
            { 'type': 'dataset', 'id': 'protein-structures-3d', 'name': 'Protein Structures 3D' },
            { 'type': 'dataset', 'id': 'rna-sequences', 'name': 'RNA Sequences' }
        ]
    },
    {
        'id': 'kb-earth-science',
        'name': 'Earth Science Data Hub',
        'description': 'Geological, seismic, and climate data for earth science research and analysis.',
        'author': 'earth-science-team',
        'status': 'syncing',
        'type': 'research',
        'lastModified': '2025-04-14T16:45:00Z',
        'vectorStore': {
            'type': 'chroma',
            'vectorCount': 67000
        },
        'documents': {
            'total': 4200,
            'processed': 3800,
            'indexed': 3500
        },
        'sources': [
            { 'type': 'dataset', 'id': 'geoscience-maps', 'name': 'Geoscience Maps' },
            { 'type': 'dataset', 'id': 'ocean-climate-sensors', 'name': 'Ocean Climate Sensors' }
        ]
    },
    {
        'id': 'kb-chemistry-corpus',
        'name': 'Chemistry Research Corpus',
        'description': 'Chemistry research papers, quantum chemistry calculations, and molecular data.',
        'author': 'chem-ai-lab',
        'status': 'ready',
        'type': 'academic',
        'lastModified': '2025-04-08T11:20:00Z',
        'vectorStore': {
            'type': 'chroma',
            'vectorCount': 156000
        },
        'documents': {
            'total': 9800,
            'processed': 9800,
            'indexed': 9800
        },
        'sources': [
            { 'type': 'dataset', 'id': 'chemistry-books', 'name': 'Chemistry Books' },
            { 'type': 'dataset', 'id': 'quantum-chemistry-calcs', 'name': 'Quantum Chemistry Calcs' }
        ]
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])
def knowledgebase_list(request):
    """List knowledge bases"""
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': SAMPLE_KNOWLEDGE_BASES,
            'total': len(SAMPLE_KNOWLEDGE_BASES),
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def knowledgebase_detail(request, kb_id):
    """Get knowledge base detail"""
    kb = next((k for k in SAMPLE_KNOWLEDGE_BASES if k['id'] == kb_id), None)
    
    if kb:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': kb
        })
    
    return Response({
        'code': 404,
        'msg': 'knowledge base not found',
        'data': {}
    })


urlpatterns = [
    path('knowledgebase', knowledgebase_list, name='knowledgebase-list'),
    path('knowledgebase/<str:kb_id>', knowledgebase_detail, name='knowledgebase-detail'),
]
