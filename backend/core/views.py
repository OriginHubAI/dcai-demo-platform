import asyncio

import httpx
from django.conf import settings
from django.http import JsonResponse


async def services_health(request):
    services = {
        'dataflow': getattr(settings, 'DATAFLOW_BACKEND_URL', 'http://localhost:8002'),
        'loopai': getattr(settings, 'LOOPAI_BACKEND_URL', 'http://localhost:8003'),
        'dfagent': getattr(settings, 'DFAGENT_BACKEND_URL', 'http://localhost:7860'),
    }

    async def probe(name: str, base_url: str) -> tuple[str, dict]:
        last_error = ''
        last_response: dict | None = None
        for suffix in ('/health', '/'):
            try:
                url = f'{base_url.rstrip("/")}{suffix}'
                async with httpx.AsyncClient(timeout=5) as client:
                    response = await client.get(url)
                if response.status_code < 400:
                    return name, {
                        'ok': True,
                        'status_code': response.status_code,
                        'url': url,
                    }
                last_response = {
                    'ok': False,
                    'status_code': response.status_code,
                    'url': url,
                }
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
        if last_response is not None:
            return name, last_response
        return name, {
            'ok': False,
            'status_code': None,
            'url': base_url,
            'error': last_error,
        }

    results = dict(await asyncio.gather(*(probe(name, url) for name, url in services.items())))
    overall = all(item['ok'] for item in results.values())
    return JsonResponse({
        'code': 0,
        'msg': 'success',
        'data': {
            'ok': overall,
            'services': results,
        },
    }, status=200 if overall else 503)
