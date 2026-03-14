"""DataFlow URL Configuration."""
from django.urls import path, re_path

from .views import (
    package_detail,
    package_editor_start,
    package_editor_stop,
    package_file_content,
    package_files,
    package_list,
    package_test,
)
from .proxy_views import (
    task_proxy,
    pipeline_proxy,
    operator_subpath_proxy,
    serving_proxy,
    preferences_proxy,
    prompts_proxy,
    text2sql_database_proxy,
    text2sql_database_manager_proxy,
)

urlpatterns = [
    path('packages', package_list, name='package-list'),
    path('packages/<str:package_id>', package_detail, name='package-detail'),
    path('packages/<str:package_id>/files', package_files, name='package-files'),
    path('packages/<str:package_id>/file', package_file_content, name='package-file-content'),
    path('packages/<str:package_id>/editor/start', package_editor_start, name='package-editor-start'),
    path('packages/<str:package_id>/editor/stop', package_editor_stop, name='package-editor-stop'),
    path('packages/<str:package_id>/test', package_test, name='package-test'),

    # Operators: all paths proxied to DataFlow backend (AllowAny, consistent with other proxy views)
    path('operators', operator_subpath_proxy, name='operator-list'),
    path('operators/', operator_subpath_proxy, name='operator-list-slash'),
    path('operators/<path:subpath>', operator_subpath_proxy, name='operator-subpath'),

    # Pipelines: root (with and without trailing slash) + sub-paths all proxied to DataFlow backend
    path('pipelines', pipeline_proxy, name='pipeline-proxy-bare'),
    path('pipelines/', pipeline_proxy, name='pipeline-proxy-root'),
    path('pipelines/<path:subpath>', pipeline_proxy, name='pipeline-proxy'),

    # Tasks: all paths proxied to DataFlow backend
    path('tasks', task_proxy, name='task-list'),
    path('tasks/<path:subpath>', task_proxy, name='task-proxy'),

    # Serving: all paths proxied to DataFlow backend
    re_path(r'^serving(/(?P<subpath>.*))?$', serving_proxy, name='serving-proxy'),

    # Preferences: all paths proxied to DataFlow backend
    re_path(r'^preferences(/(?P<subpath>.*))?$', preferences_proxy, name='preferences-proxy'),

    # Prompts: all paths proxied to DataFlow backend
    re_path(r'^prompts(/(?P<subpath>.*))?$', prompts_proxy, name='prompts-proxy'),

    # Text2SQL Database: all paths proxied to DataFlow backend
    re_path(r'^text2sql_database(/(?P<subpath>.*))?$', text2sql_database_proxy, name='text2sql-database-proxy'),

    # Text2SQL Database Manager: all paths proxied to DataFlow backend
    re_path(r'^text2sql_database_manager(/(?P<subpath>.*))?$', text2sql_database_manager_proxy, name='text2sql-database-manager-proxy'),
]
