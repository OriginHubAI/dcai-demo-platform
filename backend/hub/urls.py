from django.urls import path

from . import views


urlpatterns = [
    path('datasets', views.dataset_list_v2, name='hub-dataset-list-v2'),
    path('datasets/<path:repo_id>/tree', views.dataset_tree_v2, name='hub-dataset-tree-v2'),
    path('datasets/<path:repo_id>/splits', views.dataset_splits_v2, name='hub-dataset-splits-v2'),
    path('datasets/<path:repo_id>/rows', views.dataset_rows_v2, name='hub-dataset-rows-v2'),
    path('datasets/<path:repo_id>/preview', views.dataset_preview_v2, name='hub-dataset-preview-v2'),
    path('datasets/<path:repo_id>', views.dataset_detail_v2, name='hub-dataset-detail-v2'),
    path('models', views.model_list_v2, name='hub-model-list-v2'),
    path('models/<path:repo_id>', views.model_detail_v2, name='hub-model-detail-v2'),
    path('hf/api/datasets', views.hf_list_datasets, name='hf-list-datasets'),
    path('hf/api/datasets/<path:repo_id>/tree/<str:revision>', views.hf_dataset_tree, name='hf-dataset-tree'),
    path('hf/api/datasets/<path:repo_id>/paths-info/<str:revision>', views.hf_dataset_paths_info, name='hf-dataset-paths-info'),
    path('hf/api/datasets/<path:repo_id>/commits/<str:revision>', views.hf_dataset_commits, name='hf-dataset-commits'),
    path('hf/api/datasets/<path:repo_id>', views.hf_dataset_metadata, name='hf-dataset-metadata'),
    path('hf/is-valid', views.hf_is_valid, name='hf-is-valid'),
    path('hf/viewer/is-valid', views.hf_is_valid, name='hf-viewer-is-valid'),
    path('hf/splits', views.hf_get_splits, name='hf-get-splits'),
    path('hf/viewer/splits', views.hf_get_splits, name='hf-viewer-get-splits'),
    path('hf/rows', views.hf_get_rows, name='hf-get-rows'),
    path('hf/viewer/rows', views.hf_get_rows, name='hf-viewer-get-rows'),
    path('hf/first-rows', views.hf_get_rows, name='hf-first-rows'),
    path('hf/viewer/first-rows', views.hf_get_rows, name='hf-viewer-first-rows'),
    path('hf/info', views.hf_dataset_info, name='hf-dataset-info'),
    path('hf/viewer/info', views.hf_dataset_info, name='hf-viewer-dataset-info'),
    path('hf/parquet', views.hf_parquet_list, name='hf-parquet-list'),
    path('hf/viewer/parquet', views.hf_parquet_list, name='hf-viewer-parquet-list'),
    path('hf/datasets/<path:repo_id>/resolve/<str:revision>/<path:file_path>', views.hf_resolve_file, name='hf-resolve-file'),
]
