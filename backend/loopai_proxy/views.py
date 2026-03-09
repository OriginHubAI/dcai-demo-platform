"""
Proxy views for Dataflow-LoopAI backend.
Forwards authenticated requests to the LoopAI FastAPI service.
Supports SSE streaming for agent message streams.
"""
import httpx
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

EXCLUDED_HEADERS = frozenset(['host', 'authorization', 'content-length', 'transfer-encoding'])
ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')

LOOPAI_BACKEND_URL = getattr(settings, 'LOOPAI_BACKEND_URL', 'http://localhost:8003')
PROXY_TIMEOUT = getattr(settings, 'PROXY_TIMEOUT', 120)

# Paths that return SSE streams
SSE_PATHS = {'starter/agent/message/stream'}


def _proxy(request, target_url: str, stream: bool = False):
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in EXCLUDED_HEADERS
    }
    headers['X-DCAI-User-ID'] = str(getattr(request.user, 'id', '') or 'anonymous')

    try:
        if stream:
            client = httpx.Client(timeout=None)
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

            response = StreamingHttpResponse(
                streaming_content=_gen(),
                status=resp.status_code,
                content_type=resp.headers.get('content-type', 'text/event-stream'),
            )
            response['Cache-Control'] = resp.headers.get('cache-control', 'no-cache')
            response['X-Accel-Buffering'] = 'no'
            return response
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
            '{"code": 503, "msg": "LoopAI service unavailable", "data": {}}',
            status=503,
            content_type='application/json',
        )
    except httpx.TimeoutException:
        return HttpResponse(
            '{"code": 504, "msg": "LoopAI service timeout", "data": {}}',
            status=504,
            content_type='application/json',
        )


@csrf_exempt
def loopai_proxy(request, path=''):
    if request.method == 'OPTIONS':
        response = HttpResponse(status=204)
        response['Allow'] = ', '.join(ALLOWED_METHODS)
        return response

    if request.method not in ALLOWED_METHODS:
        return HttpResponseNotAllowed(ALLOWED_METHODS)

    is_stream = path in SSE_PATHS or request.GET.get('stream') == 'true'
    target = f"{LOOPAI_BACKEND_URL}/{path}"
    return _proxy(request, target, stream=is_stream)
