# Authentication Guidelines

> Strategies for handling authentication and authorization across the Django gateway and proxied FastAPI services.

---

## The Hybrid Authentication Architecture

The DCAI Platform leverages Django as the primary Identity Provider (IdP) and API Gateway. Downstream services (Type B apps like DataFlow-WebUI, LoopAI) rely on Django to supply validated identity context via JWT headers.

### 1. User Login & Token Generation (Django)

Users authenticate via:
- Email / Password
- Phone / SMS Code
- OAuth (WeChat, GitHub)

Django handles these flows and issues **JSON Web Tokens (JWT)**—specifically, Access Tokens (short-lived) and Refresh Tokens (long-lived).

```python
# The client receives a pair:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiO..."
}
```

### 2. Django API Endpoint Protection

Use standard DRF classes to protect native Django endpoints.

```python
# backend/dataset/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Dataset

class DatasetViewSet(ModelViewSet):
    queryset = Dataset.objects.all()
    # Enforce JWT validity
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The user is securely injected into request.user by DRF's JWTAuthentication
        serializer.save(owner=self.request.user)
```

---

## 3. Proxying Identity to Internal Type-B Apps (FastAPI)

When Django proxies a request to an internal FastAPI service via `httpx`, it passes the JWT context forward.

```python
# backend/core/proxy.py (Snippet)
async def forward_to_fastapi(request, endpoint: str):
    target_url = f"{settings.FASTAPI_BASE_URL}/{endpoint}"
    
    # Forward the Bearer token transparently
    headers = {
        'Authorization': request.headers.get('Authorization', ''),
        'X-Forwarded-User-Id': str(request.user.id) if request.user.is_authenticated else '',
    }

    async with httpx.AsyncClient() as client:
        return await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            # ...
        )
```

### 4. Decoding JWT in FastAPI

The remote FastAPI service receives the standard `Authorization: Bearer <token>` header. It validates the signature locally (since both services share the JWT Secret Key) to trust the identity.

```python
# DataFlow-System / FastAPI
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()
JWT_SECRET = "your-shared-django-secret-key"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # FastAPI decodes the token that Django generated
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token scope")
        return {"user_id": user_id}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Using it in a FastAPI route
@app.post("/operators")
async def create_operator(operator_data: dict, user: dict = Depends(get_current_user)):
    # Safely associate the operator with the user
    save_operator(creator_id=user["user_id"], data=operator_data)
```

---

## Agent Routing Permissions (@SubAgent Dispatch)

When users invoke an agent via the DataMaster unified chat (`POST /api/v1/chat`), the Django router verifies:
1. Is the user authenticated?
2. Does the user have access to the referenced `knowledge_base` or `dataset`?
3. Is `AgentRegistry` allowed to proxy this specific user to the downstream model?

If all clear, it dispatches the `stream_agent` SSE connection with the appended context headers.

---

## Role-Based Access Control (RBAC)

Use simple Python decorators or permission classes for complex rules.

```python
# Custom Permissions Example
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user

class DocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
```

---

## Handling High-Volume Data APIs (Datasets API)

While the JWT + Django Gateway approach is excellent for the **Control Plane** (e.g., creating datasets, editing metadata, managing permissions), it can become a bottleneck for the **Data Plane** (e.g., uploading/downloading large files or high-throughput data streams). For high-performance APIs like the Datasets API, follow these guidelines to separate control flow from data flow:

1. **Bypass Django for Large Data Transfer**:
   Do not proxy large binary streams or gigabytes of data through Django using `httpx`. This will tie up Django workers and cause excessive memory/CPU overhead.
   - **Solution**: Use **Presigned URLs**. Django validates permissions and generates a temporary, secure URL (e.g., AWS S3, MinIO, LakeFS). The client then interacts directly with the object storage, bypassing the Python backend completely.

2. **Push Authorization Down to the Database Level**:
   Avoid using standard DRF object-level permissions (`has_object_permission`) for list endpoints returning thousands of records, as this can lead to severe `N+1` query issues and high Python CPU usage.
   - **Solution**: Filter datasets by the authenticated user directly in the database query (e.g., `Dataset.objects.filter(owner=request.user)` inside the view's `get_queryset` method).

3. **Avoid SSE for Binary Data**:
   Server-Sent Events (SSE) used for Agent Routing are tailored for text generation (like LLM tokens), not for streaming binary or structured table data.
   - **Solution**: Use standard chunked transfers (`Transfer-Encoding: chunked`), dedicated binary protocols, or direct file downloads.

---

## Summary

| Core Component       | Auth Responsibility                     |
| -------------------- | --------------------------------------- |
| **Django Auth APIs** | Issues JWTs (`/api/v1/login`, OAuth)    |
| **Django ViewSets**  | Validates token via `IsAuthenticated`   |
| **Proxy Layer**      | Passes `Authorization` header downstream|
| **FastAPI Services** | Decodes JWT manually using shared secret|
| **Agent Router**     | Evaluates workspace permissions before proxying |
| **Data Plane**       | Issues Presigned URLs to bypass proxy overhead  |
