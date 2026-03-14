"""
DataFlow /api/v1/ passthrough URL Configuration.

Routes /api/v1/tasks/*, /api/v1/pipelines/*, /api/v1/operators/* through
Django proxy views to DATAFLOW_BACKEND_URL, so all DataFlow traffic passes
through a single Django-controlled layer regardless of whether it originates
from the in-iframe frontend (/api/v1/) or the compat layer (/api/v2/dataflow/).

re_path is used so that both bare paths (operators) and trailing-slash paths
(operators/) are handled correctly — <path:subpath> requires ≥1 character and
would 404 on a trailing-slash-only suffix.
"""
from django.urls import re_path

from .proxy_views import task_proxy, pipeline_proxy, operator_subpath_proxy

urlpatterns = [
    # Tasks: matches /tasks, /tasks/, /tasks/foo, /tasks/foo/bar, …
    re_path(r'^tasks(/(?P<subpath>.*))?$', task_proxy, name='v1-task-proxy'),

    # Pipelines: matches /pipelines, /pipelines/, /pipelines/foo, …
    re_path(r'^pipelines(/(?P<subpath>.*))?$', pipeline_proxy, name='v1-pipeline-proxy'),

    # Operators: matches /operators, /operators/, /operators/foo, …
    re_path(r'^operators(/(?P<subpath>.*))?$', operator_subpath_proxy, name='v1-operator-proxy'),
]
