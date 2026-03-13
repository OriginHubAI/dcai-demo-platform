from django.urls import path, re_path
from .hf_views import hf_list_datasets, hf_dataset_metadata, hf_resolve_file, hf_parquet_list, hf_dataset_info

urlpatterns = [
    path('api/datasets', hf_list_datasets, name='hf-list-datasets'),
    path('parquet', hf_parquet_list, name='hf-parquet-list'),
    path('info', hf_dataset_info, name='hf-dataset-info'),
    re_path(r'^api/datasets/(?P<repo_id>.*)$', hf_dataset_metadata, name='hf-dataset-metadata'),
    re_path(r'^datasets/(?P<repo_id>.*)/resolve/(?P<revision>[^/]+)/(?P<path>.*)$', hf_resolve_file, name='hf-resolve-file'),
]
