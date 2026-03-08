import httpx
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


EXCLUDED_HEADERS = frozenset(['host', 'authorization', 'content-length', 'transfer-encoding'])
DFAGENT_BACKEND_URL = getattr(settings, 'DFAGENT_BACKEND_URL', 'http://localhost:7860')
PROXY_TIMEOUT = getattr(settings, 'PROXY_TIMEOUT', 120)


def _proxy(request, target_url: str, stream: bool = False):
    headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in EXCLUDED_HEADERS
    }
    headers['X-DCAI-User-ID'] = str(getattr(request.user, 'id', '') or 'anonymous')

    try:
        if stream:
            client = httpx.Client(timeout=None)
            proxy_request = client.build_request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=request.body,
                params=request.GET.dict(),
            )
            response = client.send(proxy_request, stream=True)

            def iterator():
                try:
                    for chunk in response.iter_bytes():
                        yield chunk
                finally:
                    response.close()
                    client.close()

            return StreamingHttpResponse(
                streaming_content=iterator(),
                status=response.status_code,
                content_type=response.headers.get('content-type', 'text/plain'),
            )

        with httpx.Client(timeout=PROXY_TIMEOUT) as client:
            response = client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=request.body,
                params=request.GET.dict(),
            )
        proxied = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'text/html'),
        )
        for header_name in ('cache-control', 'etag'):
            if header_name in response.headers:
                proxied[header_name] = response.headers[header_name]
        return proxied
    except httpx.ConnectError:
        return HttpResponse(
            '{"code": 503, "msg": "DFAgent service unavailable", "data": {}}',
            status=503,
            content_type='application/json',
        )
    except httpx.TimeoutException:
        return HttpResponse(
            '{"code": 504, "msg": "DFAgent service timeout", "data": {}}',
            status=504,
            content_type='application/json',
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def dfagent_proxy(request, path=''):
    target = DFAGENT_BACKEND_URL.rstrip('/')
    target_url = f'{target}/{path}' if path else f'{target}/'
    return _proxy(request, target_url, stream=path.endswith('/stream'))
