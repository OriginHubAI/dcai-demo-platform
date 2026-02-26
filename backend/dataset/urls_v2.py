"""
Dataset V2 URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Sample dataset data for API mode
SAMPLE_DATASETS = [
    {
        'id': 'math-olympiad-problems',
        'author': 'deepmind',
        'name': 'Math Olympiad Problems',
        'task': 'question-answering',
        'domain': 'mathematics',
        'downloads': 4800000,
        'likes': 3600,
        'lastModified': '2025-03-15',
        'rows': 125000,
        'size': '280MB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-by-4.0',
        'description': 'A curated collection of international math olympiad problems spanning algebra, geometry, number theory, and combinatorics with step-by-step solutions.'
    },
    {
        'id': 'iron-steel-papers',
        'author': 'metallurgy-institute',
        'name': 'Iron & Steel Papers',
        'task': 'text-classification',
        'domain': 'materials-science',
        'downloads': 1350000,
        'likes': 1820,
        'lastModified': '2025-02-20',
        'rows': 87500,
        'size': '4.2GB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-by-4.0',
        'description': 'Full-text research papers on iron and steel metallurgy covering alloy design, heat treatment, microstructure analysis, and mechanical properties.'
    },
    {
        'id': 'protein-structures-3d',
        'author': 'alphafold-community',
        'name': 'Protein Structures 3D',
        'task': 'feature-extraction',
        'domain': 'biology',
        'downloads': 3900000,
        'likes': 4200,
        'lastModified': '2025-03-01',
        'rows': 2300000,
        'size': '320GB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-by-4.0',
        'description': 'Three-dimensional protein structure predictions with amino acid sequences, folding annotations, and confidence scores from AlphaFold-derived pipelines.'
    },
    {
        'id': 'rna-sequences',
        'author': 'bioinfo-hub',
        'name': 'RNA Sequences',
        'task': 'text-classification',
        'domain': 'biology',
        'downloads': 2650000,
        'likes': 3400,
        'lastModified': '2025-03-12',
        'rows': 12500000,
        'size': '45GB',
        'modality': 'text',
        'language': 'en',
        'license': 'mit',
        'description': 'Curated RNA sequence data including mRNA, tRNA, and non-coding RNA with secondary structure annotations and functional classifications.'
    },
    {
        'id': 'astrophysics-spectra',
        'author': 'astro-data-lab',
        'name': 'Astrophysics Spectra',
        'task': 'feature-extraction',
        'domain': 'astronomy',
        'downloads': 870000,
        'likes': 1680,
        'lastModified': '2024-12-10',
        'rows': 4500000,
        'size': '95GB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-0',
        'description': 'Stellar and galactic spectral data from ground-based and space telescopes, annotated with redshift, chemical composition, and luminosity class.'
    },
    {
        'id': 'materials-genome',
        'author': 'nist-data',
        'name': 'Materials Genome',
        'task': 'feature-extraction',
        'domain': 'materials-science',
        'downloads': 740000,
        'likes': 1280,
        'lastModified': '2024-11-20',
        'rows': 3200000,
        'size': '28GB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-by-4.0',
        'description': 'Materials properties database covering crystal structures, band gaps, elastic constants, and thermodynamic stability from the Materials Genome Initiative.'
    },
    {
        'id': 'ocean-climate-sensors',
        'author': 'noaa-research',
        'name': 'Ocean Climate Sensors',
        'task': 'feature-extraction',
        'domain': 'earth-science',
        'downloads': 530000,
        'likes': 890,
        'lastModified': '2025-03-05',
        'rows': 56000000,
        'size': '72GB',
        'modality': 'text',
        'language': 'en',
        'license': 'cc-0',
        'description': 'Time-series oceanographic sensor data including sea surface temperature, salinity, dissolved oxygen, and current velocity from global buoy networks.'
    },
    {
        'id': 'drug-molecule-graphs',
        'author': 'pharma-ai',
        'name': 'Drug Molecule Graphs',
        'task': 'text-classification',
        'domain': 'medicine',
        'downloads': 2200000,
        'likes': 2850,
        'lastModified': '2025-02-22',
        'rows': 1800000,
        'size': '15GB',
        'modality': 'text',
        'language': 'en',
        'license': 'apache-2.0',
        'description': 'Molecular graph representations of drug compounds with SMILES notation, bioactivity labels, toxicity predictions, and ADMET property annotations.'
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_list_v2(request):
    """List datasets V2"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    
    total = len(SAMPLE_DATASETS)
    start = (page - 1) * page_size
    end = start + page_size
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': SAMPLE_DATASETS[start:end],
            'total': total,
            'page': page,
            'page_size': page_size,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_detail_v2(request, dataset_id):
    """Get dataset detail V2"""
    dataset = next((d for d in SAMPLE_DATASETS if d['id'] == dataset_id), None)
    
    if dataset:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': dataset
        })
    
    return Response({
        'code': 404,
        'msg': 'dataset not found',
        'data': {}
    })


urlpatterns = [
    path('datasets', dataset_list_v2, name='dataset-list-v2'),
    path('datasets/<str:dataset_id>', dataset_detail_v2, name='dataset-detail-v2'),
]
