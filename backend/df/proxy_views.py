"""
Proxy views for DataFlow-WebUI backend.
Forwards authenticated requests to the DataFlow-WebUI FastAPI service.
"""
import httpx
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

EXCLUDED_HEADERS = frozenset(['host', 'authorization', 'content-length', 'transfer-encoding'])

DATAFLOW_BACKEND_URL = getattr(settings, 'DATAFLOW_BACKEND_URL', 'http://localhost:8002')
PROXY_TIMEOUT = getattr(settings, 'PROXY_TIMEOUT', 120)


def _proxy(request, target_url: str, stream: bool = False):
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_HEADERS
    }
    headers['X-DCAI-User-ID'] = str(getattr(request.user, 'id', '') or 'anonymous')

    try:
        if stream:
            client = httpx.Client(timeout=PROXY_TIMEOUT)
            req = client.build_request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=request.body,
                params=request.GET.dict(),
            )
            resp = client.send(req, stream=True)

            def _gen():
                try:
                    for chunk in resp.iter_bytes():
                        yield chunk
                finally:
                    resp.close()
                    client.close()

            return StreamingHttpResponse(
                streaming_content=_gen(),
                status=resp.status_code,
                content_type=resp.headers.get('content-type', 'text/event-stream'),
            )
        else:
            with httpx.Client(timeout=PROXY_TIMEOUT) as client:
                resp = client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=request.body,
                    params=request.GET.dict(),
                )
            return HttpResponse(
                content=resp.content,
                status=resp.status_code,
                content_type=resp.headers.get('content-type', 'application/json'),
            )
    except httpx.ConnectError:
        return HttpResponse(
            '{"code": 503, "msg": "DataFlow service unavailable", "data": {}}',
            status=503,
            content_type='application/json',
        )
    except httpx.TimeoutException:
        return HttpResponse(
            '{"code": 504, "msg": "DataFlow service timeout", "data": {}}',
            status=504,
            content_type='application/json',
        )


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def dataflow_proxy(request, path=''):
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def task_proxy(request, subpath=''):
    """Proxy task lifecycle requests to DataFlow-WebUI backend."""
    path = f"tasks/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    # /newly endpoint uses long-polling — enable streaming
    stream = subpath.rstrip('/').endswith('/newly')
    return _proxy(request, target, stream=stream)


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def pipeline_proxy(request, subpath=''):
    """Proxy pipeline requests to DataFlow-WebUI backend."""
    path = f"pipelines/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def operator_subpath_proxy(request, subpath=''):
    """Proxy operator sub-path requests to DataFlow-WebUI backend."""
    path = f"operators/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
def serving_proxy(request, subpath=''):
    """Proxy serving requests to DataFlow-WebUI backend."""
    path = f"serving/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def preferences_proxy(request, subpath=''):
    """Proxy preferences requests to DataFlow-WebUI backend."""
    path = f"preferences/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET'])
@permission_classes([AllowAny])
def prompts_proxy(request, subpath=''):
    """Proxy prompts requests to DataFlow-WebUI backend."""
    path = f"prompts/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def text2sql_database_proxy(request, subpath=''):
    """Proxy text2sql_database requests to DataFlow-WebUI backend."""
    path = f"text2sql_database/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def text2sql_database_manager_proxy(request, subpath=''):
    """Proxy text2sql_database_manager requests to DataFlow-WebUI backend."""
    path = f"text2sql_database_manager/{subpath}"
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/{path}"
    return _proxy(request, target)
