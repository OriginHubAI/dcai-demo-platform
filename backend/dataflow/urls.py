"""DataFlow URL Configuration."""
from django.urls import path, re_path

from .proxy_views import dataflow_proxy
from .views import (
    package_detail,
    package_editor_start,
    package_editor_stop,
    package_file_content,
    package_files,
    package_list,
    package_test,
    OperatorListView,
    PipelineStatusView,
)

urlpatterns = [
    path('packages', package_list, name='package-list'),
    path('packages/<str:package_id>', package_detail, name='package-detail'),
    path('packages/<str:package_id>/files', package_files, name='package-files'),
    path('packages/<str:package_id>/file', package_file_content, name='package-file-content'),
    path('packages/<str:package_id>/editor/start', package_editor_start, name='package-editor-start'),
    path('packages/<str:package_id>/editor/stop', package_editor_stop, name='package-editor-stop'),
    path('packages/<str:package_id>/test', package_test, name='package-test'),
    
    # Dataflow System Integration (Mock specific routes)
    path('operators', OperatorListView.as_view(), name='operator-list'),
    path('pipelines/<uuid:pipeline_id>/status', PipelineStatusView.as_view(), name='pipeline-status'),

    # DataFlow-WebUI proxy routes
    re_path(r'^pipelines/(?P<path>.*)$', dataflow_proxy),
    re_path(r'^operators/(?P<path>.*)$', dataflow_proxy),
    re_path(r'^tasks/(?P<path>.*)$', dataflow_proxy),
    re_path(r'^datasets/(?P<path>.*)$', dataflow_proxy),
    re_path(r'^serving/(?P<path>.*)$', dataflow_proxy),
    re_path(r'^prompts/(?P<path>.*)$', dataflow_proxy),
]
