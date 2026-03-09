"""
DataFlow URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import views

# Sample DataFlow packages
SAMPLE_PACKAGES = [
    {
        'id': 'dataflow',
        'name': 'DataFlow',
        'author': 'DCAI',
        'description': 'Core data processing and pipeline framework for building efficient, scalable data workflows. Provides foundational APIs for data ingestion, transformation, and output.',
        'downloads': 3200000,
        'likes': 4800,
        'lastModified': '2025-04-10',
        'version': '2.4.0',
        'tags': ['core', 'pipeline', 'data-processing'],
        'license': 'apache-2.0',
        'category': 'all',
    },
    {
        'id': 'dataflow-mm',
        'name': 'DataFlow-MM',
        'author': 'DCAI',
        'description': 'Multimodal data processing extension for DataFlow. Supports image, video, audio, and text data in unified pipelines with cross-modal alignment and fusion.',
        'downloads': 1800000,
        'likes': 3200,
        'lastModified': '2025-03-28',
        'version': '1.6.0',
        'tags': ['multimodal', 'image', 'video', 'audio'],
        'license': 'apache-2.0',
        'category': 'multimodal',
    },
    {
        'id': 'dataflow-material',
        'name': 'DataFlow-Material',
        'author': 'DCAI',
        'description': 'Material science data processing toolkit. Handles crystal structures, molecular dynamics simulations, spectroscopy data, and materials property prediction pipelines.',
        'downloads': 420000,
        'likes': 1100,
        'lastModified': '2025-04-02',
        'version': '1.2.0',
        'tags': ['material-science', 'crystal', 'molecular'],
        'license': 'apache-2.0',
        'category': 'science',
    },
    {
        'id': 'dataflow-math',
        'name': 'DataFlow-Math',
        'author': 'DCAI',
        'description': 'Mathematical and numerical computing extension for DataFlow. Provides symbolic computation, numerical optimization, and statistical analysis pipelines.',
        'downloads': 960000,
        'likes': 1800,
        'lastModified': '2025-03-15',
        'version': '1.4.0',
        'tags': ['math', 'numerical', 'statistics', 'optimization'],
        'license': 'apache-2.0',
        'category': 'science',
    },
    {
        'id': 'dataflow-timeseries',
        'name': 'DataFlow-TimeSeries',
        'author': 'DCAI',
        'description': 'Time series data processing and analysis toolkit. Supports forecasting, anomaly detection, feature extraction, and streaming data pipelines.',
        'downloads': 1400000,
        'likes': 2500,
        'lastModified': '2025-04-05',
        'version': '1.5.0',
        'tags': ['time-series', 'forecasting', 'anomaly-detection', 'streaming'],
        'license': 'apache-2.0',
        'category': 'time-series',
    },
    {
        'id': 'dataflow-geology',
        'name': 'DataFlow-Geology',
        'author': 'DCAI',
        'description': 'Geological data processing and analysis framework. Handles seismic data, well logs, geospatial analysis, and subsurface modeling pipelines.',
        'downloads': 280000,
        'likes': 720,
        'lastModified': '2025-03-20',
        'version': '1.1.0',
        'tags': ['geology', 'seismic', 'geospatial', 'subsurface'],
        'license': 'apache-2.0',
        'category': 'science',
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])
def package_list(request):
    """List DataFlow packages"""
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': SAMPLE_PACKAGES,
            'total': len(SAMPLE_PACKAGES),
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def package_detail(request, package_id):
    """Get package detail"""
    package = next((p for p in SAMPLE_PACKAGES if p['id'] == package_id), None)
    
    if package:
        return Response({
            'code': 0,
            'msg': 'success',
            'data': package
        })
    
    return Response({
        'code': 404,
        'msg': 'package not found',
        'data': {}
    })


urlpatterns = [
    path('packages', package_list, name='package-list'),
    path('packages/<str:package_id>', package_detail, name='package-detail'),
    
    # Dataflow System Integration
    path('operators', views.OperatorListView.as_view(), name='operator-list'),
    path('pipelines/<uuid:pipeline_id>/status', views.PipelineStatusView.as_view(), name='pipeline-status'),
]
