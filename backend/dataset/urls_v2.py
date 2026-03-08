"""
Dataset V2 URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Sample tasks data for related tasks
SAMPLE_TASKS = [
    {
        'id': 'task-nuscenes-filter',
        'name': 'nuScenes Quality Filtering Pipeline',
        'dataset': 'autodrive-raw-nuscenes',
        'outputDataset': 'autodrive-derived-nuscenes-filtered',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2025-03-15T08:00:00Z',
        'endedAt': '2025-03-15T14:30:00Z',
        'duration': '6h 30m',
        'author': 'autodrive-ai',
    },
    {
        'id': 'task-nuscenes-label',
        'name': 'nuScenes VLM Labeling Pipeline',
        'dataset': 'autodrive-raw-nuscenes',
        'outputDataset': 'autodrive-derived-nuscenes-labeled',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2025-03-14T10:00:00Z',
        'endedAt': '2025-03-15T02:15:00Z',
        'duration': '16h 15m',
        'author': 'autodrive-ai',
    },
    {
        'id': 'task-waymo-motion',
        'name': 'Waymo Motion Forecasting Pipeline',
        'dataset': 'autodrive-raw-waymo-open',
        'outputDataset': 'autodrive-derived-waymo-motion',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2025-03-20T09:00:00Z',
        'endedAt': '2025-03-21T08:45:00Z',
        'duration': '23h 45m',
        'author': 'autodrive-ai',
    },
    {
        'id': 'task-waymo-perception',
        'name': 'Waymo Perception Enhancement Pipeline',
        'dataset': 'autodrive-raw-waymo-open',
        'outputDataset': 'autodrive-derived-waymo-perception',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'running',
        'progress': 78,
        'startedAt': '2025-03-21T10:00:00Z',
        'endedAt': None,
        'duration': None,
        'author': 'autodrive-ai',
    },
    {
        'id': 'task-kitti360-process',
        'name': 'KITTI-360 Enhancement Pipeline',
        'dataset': 'autodrive-raw-kitti-360',
        'outputDataset': 'autodrive-derived-kitti360-processed',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2025-03-08T14:00:00Z',
        'endedAt': '2025-03-09T02:30:00Z',
        'duration': '12h 30m',
        'author': 'autodrive-ai',
    },
    {
        'id': 'task-kitti360-semantic',
        'name': 'KITTI-360 Semantic Segmentation Pipeline',
        'dataset': 'autodrive-raw-kitti-360',
        'outputDataset': 'autodrive-derived-kitti360-semantic',
        'package': 'DataFlow-MM',
        'type': 'Data Processing',
        'status': 'completed',
        'progress': 100,
        'startedAt': '2025-03-06T08:00:00Z',
        'endedAt': '2025-03-07T18:20:00Z',
        'duration': '34h 20m',
        'author': 'autodrive-ai',
    },
]


# Sample dataset data for API mode - includes autodriving datasets
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
    # Autonomous Driving Datasets - Original
    {
        'id': 'autodrive-raw-nuscenes',
        'author': 'motional-labs',
        'name': 'AutoDrive Raw - nuScenes',
        'task': 'object-detection',
        'domain': 'autonomous-driving',
        'downloads': 2100000,
        'likes': 4200,
        'lastModified': '2025-03-15',
        'rows': 1400000,
        'size': '680GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-sa-4.0',
        'description': 'Original raw autonomous driving dataset from nuScenes. Contains 1000 scenes of multimodal sensor data including 6 cameras, 1 LiDAR, 5 radar, GPS and IMU. Supports 3D object detection, tracking, and trajectory prediction tasks.',
        'datasetType': 'original',
        'derivedDatasets': ['autodrive-derived-nuscenes-filtered', 'autodrive-derived-nuscenes-labeled'],
        'metadata': {
            'timeRange': {'start': '2025-01-01', 'end': '2025-03-15', 'timezone': 'UTC'},
            'spatial': {
                'regions': ['boston', 'singapore'],
                'coverage': 'urban and suburban areas',
                'coordinates': {'lat': [1.2, 42.4], 'lon': [103.8, 71.1]}
            },
            'sensors': ['camera', 'lidar', 'radar', 'gps', 'imu'],
            'conditions': ['day', 'night', 'rain', 'clear'],
            'annotations': ['raw', 'unannotated']
        }
    },
    {
        'id': 'autodrive-raw-kitti-360',
        'author': 'kit-vision',
        'name': 'AutoDrive Raw - KITTI-360',
        'task': 'object-detection',
        'domain': 'autonomous-driving',
        'downloads': 1850000,
        'likes': 3800,
        'lastModified': '2025-02-28',
        'rows': 980000,
        'size': '520GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-sa-3.0',
        'description': 'Original raw 360-degree autonomous driving dataset extending KITTI. Contains rich sensory data with 2 fisheye cameras, 2 perspective cameras, and 1 Velodyne LiDAR. Supports 360-degree perception and dense annotation tasks.',
        'datasetType': 'original',
        'derivedDatasets': ['autodrive-derived-kitti360-processed', 'autodrive-derived-kitti360-semantic'],
        'metadata': {
            'timeRange': {'start': '2024-06-01', 'end': '2024-12-31', 'timezone': 'CET'},
            'spatial': {
                'regions': ['karlsruhe', 'germany'],
                'coverage': 'urban, highway, and rural roads',
                'coordinates': {'lat': [49.0, 49.02], 'lon': [8.4, 8.42]}
            },
            'sensors': ['camera', 'lidar', 'gps', 'imu'],
            'conditions': ['day', 'clear', 'overcast'],
            'annotations': ['raw', 'unannotated']
        }
    },
    {
        'id': 'autodrive-raw-waymo-open',
        'author': 'waymo-research',
        'name': 'AutoDrive Raw - Waymo Open',
        'task': 'object-detection',
        'domain': 'autonomous-driving',
        'downloads': 3200000,
        'likes': 5800,
        'lastModified': '2025-03-20',
        'rows': 2300000,
        'size': '1.2TB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-4.0',
        'description': 'Original raw autonomous driving dataset from Waymo. High-resolution sensor data with 5 LiDARs and 5 cameras covering 360 degrees. Includes diverse geographic locations and weather conditions for robust perception research.',
        'datasetType': 'original',
        'derivedDatasets': ['autodrive-derived-waymo-motion', 'autodrive-derived-waymo-perception'],
        'metadata': {
            'timeRange': {'start': '2024-01-01', 'end': '2025-03-20', 'timezone': 'America/Los_Angeles'},
            'spatial': {
                'regions': ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
                'coverage': 'urban, suburban, highway',
                'coordinates': {'lat': [33.4, 37.8], 'lon': [112.0, 122.4]}
            },
            'sensors': ['camera', 'lidar', 'radar'],
            'conditions': ['day', 'night', 'dawn', 'dusk', 'rain', 'clear', 'overcast'],
            'annotations': ['raw', 'unannotated']
        }
    },
    # Autonomous Driving Datasets - Derived (Read-only)
    {
        'id': 'autodrive-derived-nuscenes-filtered',
        'author': 'autodrive-ai',
        'name': 'AutoDrive Derived - nuScenes Filtered',
        'task': 'object-detection',
        'domain': 'autonomous-driving',
        'downloads': 890000,
        'likes': 2100,
        'lastModified': '2025-03-18',
        'rows': 850000,
        'size': '280GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-sa-4.0',
        'description': 'Filtered and quality-enhanced version of nuScenes. High-quality scenes selected using DataFlow-MM pipeline with aesthetic filtering, deduplication, and quality scoring. Ready for training with clean annotations.',
        'datasetType': 'derived',
        'parentDataset': 'autodrive-raw-nuscenes',
        'readonly': True,
        'processingPipeline': 'nuscenes_quality_filter_pipeline',
        'metadata': {
            'timeRange': {'start': '2025-01-01', 'end': '2025-03-15', 'timezone': 'UTC'},
            'spatial': {
                'regions': ['boston', 'singapore'],
                'coverage': 'filtered urban scenes',
                'coordinates': {'lat': [1.2, 42.4], 'lon': [103.8, 71.1]}
            },
            'sensors': ['camera', 'lidar', 'radar'],
            'conditions': ['day', 'night', 'clear', 'light-rain'],
            'annotations': ['3d-bbox', 'tracking-id', 'velocity'],
            'filterCriteria': {
                'minQualityScore': 0.85,
                'deduplication': True,
                'blurRemoval': True
            }
        },
        'semanticIndex': {
            'objects': ['car', 'truck', 'bus', 'pedestrian', 'cyclist', 'motorcycle', 'traffic-cone', 'barrier'],
            'scenes': ['intersection', 'highway-merge', 'parking-lot', 'residential', 'commercial'],
            'actions': ['moving', 'stopped', 'turning', 'parked']
        }
    },
    {
        'id': 'autodrive-derived-nuscenes-labeled',
        'author': 'autodrive-ai',
        'name': 'AutoDrive Derived - nuScenes Labeled',
        'task': 'image-segmentation',
        'domain': 'autonomous-driving',
        'downloads': 760000,
        'likes': 1850,
        'lastModified': '2025-03-16',
        'rows': 620000,
        'size': '340GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-sa-4.0',
        'description': 'VLM-enhanced labeled version of nuScenes with semantic segmentation masks and natural language descriptions. Generated using Qwen2.5-VL for detailed scene understanding and caption generation.',
        'datasetType': 'derived',
        'parentDataset': 'autodrive-raw-nuscenes',
        'readonly': True,
        'processingPipeline': 'nuscenes_vlm_labeling_pipeline',
        'metadata': {
            'timeRange': {'start': '2025-01-01', 'end': '2025-03-15', 'timezone': 'UTC'},
            'spatial': {
                'regions': ['boston', 'singapore'],
                'coverage': 'urban annotated scenes',
                'coordinates': {'lat': [1.2, 42.4], 'lon': [103.8, 71.1]}
            },
            'sensors': ['camera', 'lidar'],
            'conditions': ['day', 'clear', 'overcast'],
            'annotations': ['semantic-seg', 'instance-seg', 'caption', 'qa-pairs'],
            'vlmModel': 'Qwen2.5-VL-3B-Instruct'
        },
        'semanticIndex': {
            'objects': ['vehicle', 'person', 'road', 'sidewalk', 'building', 'vegetation', 'traffic-sign', 'traffic-light'],
            'attributes': ['color', 'size', 'orientation', 'occlusion-level'],
            'relationships': ['in-front-of', 'behind', 'next-to', 'on-road', 'crossing']
        }
    },
    {
        'id': 'autodrive-derived-waymo-motion',
        'author': 'autodrive-ai',
        'name': 'AutoDrive Derived - Waymo Motion',
        'task': 'feature-extraction',
        'domain': 'autonomous-driving',
        'downloads': 1200000,
        'likes': 2850,
        'lastModified': '2025-03-22',
        'rows': 1450000,
        'size': '480GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-4.0',
        'description': 'Motion prediction dataset derived from Waymo Open. 9-second trajectory futures for all agents with map information. Optimized for motion forecasting and behavior prediction models.',
        'datasetType': 'derived',
        'parentDataset': 'autodrive-raw-waymo-open',
        'readonly': True,
        'processingPipeline': 'waymo_motion_forecasting_pipeline',
        'metadata': {
            'timeRange': {'start': '2024-01-01', 'end': '2025-03-20', 'timezone': 'America/Los_Angeles'},
            'spatial': {
                'regions': ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
                'coverage': 'motion-rich scenarios',
                'coordinates': {'lat': [33.4, 37.8], 'lon': [112.0, 122.4]}
            },
            'sensors': ['lidar', 'camera'],
            'conditions': ['all-conditions'],
            'annotations': ['trajectory', 'intent', 'interaction-graph'],
            'predictionHorizon': '9s'
        },
        'semanticIndex': {
            'agentTypes': ['vehicle', 'pedestrian', 'cyclist'],
            'behaviors': ['stationary', 'straight', 'turn-left', 'turn-right', 'u-turn', 'lane-change'],
            'scenarios': ['intersection', 'merging', 'roundabout', 'parking-lot', 'highway'],
            'interactions': ['leader-follower', 'merging', 'crossing', 'yielding']
        }
    },
    {
        'id': 'autodrive-derived-waymo-perception',
        'author': 'autodrive-ai',
        'name': 'AutoDrive Derived - Waymo Perception',
        'task': 'object-detection',
        'domain': 'autonomous-driving',
        'downloads': 980000,
        'likes': 2400,
        'lastModified': '2025-03-21',
        'rows': 1680000,
        'size': '620GB',
        'modality': 'multimodal',
        'language': 'en',
        'license': 'cc-by-nc-4.0',
        'description': 'High-quality perception dataset derived from Waymo Open. Multi-frame temporal consistency and camera-LiDAR fusion annotations. Optimized for 3D detection and tracking tasks.',
        'datasetType': 'derived',
        'parentDataset': 'autodrive-raw-waymo-open',
        'readonly': True,
        'processingPipeline': 'waymo_perception_enhancement_pipeline',
        'metadata': {
            'timeRange': {'start': '2024-01-01', 'end': '2025-03-20', 'timezone': 'America/Los_Angeles'},
            'spatial': {
                'regions': ['phoenix', 'san-francisco', 'mountain-view', 'los-angeles'],
                'coverage': 'diverse perception scenarios',
                'coordinates': {'lat': [33.4, 37.8], 'lon': [112.0, 122.4]}
            },
            'sensors': ['camera', 'lidar'],
            'conditions': ['day', 'night', 'rain', 'clear', 'overcast'],
            'annotations': ['3d-bbox', 'tracking-id', 'velocity', 'acceleration'],
            'temporalWindow': '5-frames'
        },
        'semanticIndex': {
            'objects': ['vehicle', 'pedestrian', 'cyclist', 'sign', 'traffic-light'],
            'difficulty': ['easy', 'medium', 'hard'],
            'occlusion': ['none', 'partial', 'heavy'],
            'distance': ['0-30m', '30-50m', '50m+']
        }
    },
]


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_list_v2(request):
    """List datasets V2 with filtering support"""
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    
    # Get filter parameters
    domain = request.query_params.getlist('domain')
    modality = request.query_params.getlist('modality')
    language = request.query_params.getlist('language')
    dataset_type = request.query_params.getlist('datasetType')
    semantic_query = request.query_params.get('semanticQuery', '').lower()
    spatial_query = request.query_params.get('spatialQuery', '').lower()
    
    # Filter datasets
    filtered_datasets = SAMPLE_DATASETS
    
    if domain:
        filtered_datasets = [d for d in filtered_datasets if d.get('domain') in domain]
    
    if modality:
        filtered_datasets = [d for d in filtered_datasets if d.get('modality') in modality]
    
    if language:
        filtered_datasets = [d for d in filtered_datasets if d.get('language') in language]
    
    if dataset_type:
        filtered_datasets = [d for d in filtered_datasets if d.get('datasetType') in dataset_type]
    
    # Semantic search
    if semantic_query:
        filtered_datasets = [
            d for d in filtered_datasets 
            if (d.get('semanticIndex') and semantic_query in str(d['semanticIndex']).lower()) or
               (d.get('description', '').lower().find(semantic_query) != -1)
        ]
    
    # Spatial search
    if spatial_query:
        filtered_datasets = [
            d for d in filtered_datasets 
            if d.get('metadata', {}).get('spatial') and 
               (spatial_query in str(d['metadata']['spatial'].get('regions', [])).lower() or
                spatial_query in d['metadata']['spatial'].get('coverage', '').lower())
        ]
    
    total = len(filtered_datasets)
    start = (page - 1) * page_size
    end = start + page_size
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': filtered_datasets[start:end],
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
        # Get derived datasets info if this is an original dataset
        response_data = dict(dataset)
        if dataset.get('datasetType') == 'original' and dataset.get('derivedDatasets'):
            derived_info = [
                {'id': d_id, 'name': next((d['name'] for d in SAMPLE_DATASETS if d['id'] == d_id), d_id)}
                for d_id in dataset['derivedDatasets']
            ]
            response_data['derivedDatasetsInfo'] = derived_info
        
        # Get parent dataset info if this is a derived dataset
        if dataset.get('datasetType') == 'derived' and dataset.get('parentDataset'):
            parent = next((d for d in SAMPLE_DATASETS if d['id'] == dataset['parentDataset']), None)
            if parent:
                response_data['parentDatasetInfo'] = {
                    'id': parent['id'],
                    'name': parent['name']
                }
        
        # Get related tasks for this dataset
        related_tasks = [
            {
                'id': t['id'],
                'name': t['name'],
                'type': t['type'],
                'status': t['status'],
                'progress': t['progress'],
                'isInput': t.get('dataset') == dataset_id,
                'isOutput': t.get('outputDataset') == dataset_id,
                'startedAt': t.get('startedAt'),
                'endedAt': t.get('endedAt'),
                'duration': t.get('duration'),
            }
            for t in SAMPLE_TASKS
            if t.get('dataset') == dataset_id or t.get('outputDataset') == dataset_id
        ]
        if related_tasks:
            response_data['relatedTasks'] = related_tasks
        
        return Response({
            'code': 0,
            'msg': 'success',
            'data': response_data
        })
    
    return Response({
        'code': 404,
        'msg': 'dataset not found',
        'data': {}
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def dataset_relationships(request, dataset_id):
    """Get dataset relationships (parent and derived datasets)"""
    dataset = next((d for d in SAMPLE_DATASETS if d['id'] == dataset_id), None)
    
    if not dataset:
        return Response({
            'code': 404,
            'msg': 'dataset not found',
            'data': {}
        })
    
    relationships = {
        'parent': None,
        'derived': []
    }
    
    # Get parent dataset
    if dataset.get('parentDataset'):
        parent = next((d for d in SAMPLE_DATASETS if d['id'] == dataset['parentDataset']), None)
        if parent:
            relationships['parent'] = {
                'id': parent['id'],
                'name': parent['name'],
                'datasetType': parent.get('datasetType', 'original'),
                'readonly': parent.get('readonly', False)
            }
    
    # Get derived datasets
    if dataset.get('derivedDatasets'):
        for derived_id in dataset['derivedDatasets']:
            derived = next((d for d in SAMPLE_DATASETS if d['id'] == derived_id), None)
            if derived:
                relationships['derived'].append({
                    'id': derived['id'],
                    'name': derived['name'],
                    'datasetType': derived.get('datasetType', 'derived'),
                    'readonly': derived.get('readonly', False),
                    'processingPipeline': derived.get('processingPipeline')
                })
    
    return Response({
        'code': 0,
        'msg': 'success',
        'data': relationships
    })


urlpatterns = [
    path('datasets', dataset_list_v2, name='dataset-list-v2'),
    path('datasets/<str:dataset_id>', dataset_detail_v2, name='dataset-detail-v2'),
    path('datasets/<str:dataset_id>/relationships', dataset_relationships, name='dataset-relationships'),
]
