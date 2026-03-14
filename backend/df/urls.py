"""DataFlow URL Configuration."""
from django.urls import path

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

    # Django-native DataFlow views (not proxied — handled here regardless of ASGI routing)
    path('operators', OperatorListView.as_view(), name='operator-list'),
    path('pipelines/<uuid:pipeline_id>/status', PipelineStatusView.as_view(), name='pipeline-status'),

    # pipelines/*, operators/*, tasks/*, datasets/*, serving/*, prompts/* are now handled
    # by the DataFlow-WebUI FastAPI app via ASGI routing in core/asgi.py.
]
