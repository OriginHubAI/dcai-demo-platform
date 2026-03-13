from django.urls import path, re_path
from .hf_views import (
    hf_list_datasets, hf_dataset_metadata, hf_resolve_file, hf_parquet_list, hf_dataset_info,
    hf_create_repo, hf_delete_repo, hf_upload_file,
    hf_is_valid, hf_get_splits, hf_get_rows
)

urlpatterns = [
    # Hub APIs
    path('api/datasets', hf_list_datasets, name='hf-list-datasets'),
    path('api/repos/create', hf_create_repo, name='hf-create-repo'),
    
    # Viewer APIs (HF Datasets Server compatible)
    path('is-valid', hf_is_valid, name='hf-is-valid'),
    path('splits', hf_get_splits, name='hf-get-splits'),
    path('rows', hf_get_rows, name='hf-get-rows'),
    path('first-rows', hf_get_rows, name='hf-first-rows'),
    path('info', hf_dataset_info, name='hf-dataset-info'),
    path('parquet', hf_parquet_list, name='hf-parquet-list'),

    # More specific routes MUST come before greedy metadata route
    # Parameterized Hub APIs (Write)
    re_path(r'^api/datasets/(?P<repo_id>[^/]+/[^/]+)/upload/(?P<revision>[^/]+)/(?P<path>.*)$', hf_upload_file, name='hf-upload-file-namespace'),
    re_path(r'^api/datasets/(?P<repo_id>[^/]+)/upload/(?P<revision>[^/]+)/(?P<path>.*)$', hf_upload_file, name='hf-upload-file'),
    
    re_path(r'^api/datasets/(?P<repo_id>[^/]+/[^/]+)$', hf_delete_repo, name='hf-delete-repo-namespace'),
    re_path(r'^api/datasets/(?P<repo_id>[^/]+)$', hf_delete_repo, name='hf-delete-repo'),
    
    # Metadata (greedy to catch /tree/, /paths-info/, /revision/)
    re_path(r'^api/datasets/(?P<repo_id>.*)$', hf_dataset_metadata, name='hf-dataset-metadata'),
    
    # Resolve/Download
    re_path(r'^datasets/(?P<repo_id>.*)/resolve/(?P<revision>[^/]+)/(?P<path>.*)$', hf_resolve_file, name='hf-resolve-file'),
]
