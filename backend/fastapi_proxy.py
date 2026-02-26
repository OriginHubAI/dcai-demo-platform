"""
FastAPI Proxy Module for Django
Routes specific API endpoints from Django to FastAPI internal implementation
"""
import httpx
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json


class FastAPIProxyView(View):
    """
    Django View that proxies requests to FastAPI backend.
    
    Usage in urls.py:
        path('api/v2/agents/', FastAPIProxyView.as_view(fastapi_path='agents')),
    """
    
    fastapi_base_url = "http://localhost:8001"  # FastAPI service URL
    fastapi_path = None  # Override in subclass or as_view()
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    async def get(self, request, *args, **kwargs):
        return await self._proxy_request(request, 'GET')
    
    async def post(self, request, *args, **kwargs):
        return await self._proxy_request(request, 'POST')
    
    async def put(self, request, *args, **kwargs):
        return await self._proxy_request(request, 'PUT')
    
    async def patch(self, request, *args, **kwargs):
        return await self._proxy_request(request, 'PATCH')
    
    async def delete(self, request, *args, **kwargs):
        return await self._proxy_request(request, 'DELETE')
    
    async def _proxy_request(self, request, method):
        """Proxy the request to FastAPI backend"""
        path = self.fastapi_path or request.path.lstrip('/')
        url = f"{self.fastapi_base_url}/{path}"
        
        # Prepare headers (filter out Django-specific headers)
        headers = {
            key: value for key, value in request.headers.items()
            if key.lower() not in ['host', 'content-length', 'content-type']
        }
        if 'content-type' in request.headers:
            headers['content-type'] = request.headers['content-type']
        
        # Get query parameters
        params = dict(request.GET)
        
        # Get request body
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body = request.body.decode('utf-8')
            except:
                body = None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    content=body,
                    timeout=30.0
                )
                
                # Return response from FastAPI
                return HttpResponse(
                    content=response.content,
                    status=response.status_code,
                    content_type=response.headers.get('content-type', 'application/json')
                )
        except httpx.ConnectError:
            return JsonResponse(
                {'error': 'FastAPI service unavailable'},
                status=503
            )
        except Exception as e:
            return JsonResponse(
                {'error': f'Proxy error: {str(e)}'},
                status=500
            )


class FastAPIAgentProxyView(FastAPIProxyView):
    """Proxy for Agent endpoints"""
    fastapi_path = 'api/v2/agents'


class FastAPITaskProxyView(FastAPIProxyView):
    """Proxy for Task endpoints"""
    fastapi_path = 'api/v2/tasks'
