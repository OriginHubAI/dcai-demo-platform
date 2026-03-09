# FastAPI Integration & Microservices

> Guidelines for developing FastAPI services and integrating them with the main Django application for high-performance, asynchronous endpoints.

---

## Architecture & Integration Modes

FastAPI is used for high-performance, asynchronous workloads (e.g., Agents, Tasks, Data Processing). It integrates with Django using one of the following modes:

### 1. Proxy Mode (Recommended for Migration)
Django acts as a reverse proxy, forwarding requests to a separate FastAPI service. This allows gradual migration while maintaining Django's session, auth, and middleware.

- **Implementation**: Use `FastAPIProxyView` in `backend/fastapi_proxy.py`.
- **Routing**: Define paths in Django's `urls.py`.

```python
# core/urls.py
from fastapi_proxy import FastAPIAgentProxyView

urlpatterns = [
    path('api/v2/agents/', FastAPIAgentProxyView.as_view()),
    path('api/v2/fastapi/<path:path>', FastAPIProxyView.as_view()),
]
```

### 2. Mixed ASGI Mode
Django and FastAPI run in the same process on the same port using a combined ASGI application.

- **Implementation**: See `backend/core/asgi_fastapi.py`.
- **Usage**: Use `uvicorn core.asgi_fastapi:application`.

### 3. Standalone Mode
FastAPI runs as an independent microservice, typically routed via Nginx at the infrastructure level.

---

## Project Structure

FastAPI-related code is organized as follows:

```text
backend/
├── fastapi_app/          # FastAPI application directory
│   ├── main.py           # Application entry point
│   ├── api/              # Route handlers (APIRouters)
│   ├── schemas/          # Pydantic validation models
│   └── services/         # Business logic
├── fastapi_proxy.py      # Django proxy views
└── core/
    └── asgi_fastapi.py   # Mixed ASGI configuration
```

---

## Reusing Django Models

FastAPI can directly use Django ORM models by initializing Django within the FastAPI process.

```python
# fastapi_app/main.py
import os
import django

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now models can be imported and used
from agent.models import Agent

@app.get("/api/v2/agents")
async def list_agents():
    # Note: Use sync_to_async if performing complex ORM operations in async routes
    agents = Agent.objects.all()
    return [{"id": a.id, "name": a.name} for a in agents]
```

---

## Authentication Integration

To maintain consistency, FastAPI should reuse Django's JWT authentication mechanism.

```python
# fastapi_app/auth.py
from fastapi import Depends, HTTPException, Header
import jwt
from django.conf import settings
from user.models import User

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## Pydantic Models & Validation

Always use Pydantic models for request validation and response serialization, even when working with Django models.

```python
from pydantic import BaseModel, Field
from typing import Optional

class AgentSchema(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None

@app.post("/api/v2/agents")
async def create_agent(data: AgentSchema, user=Depends(get_current_user)):
    from agent.models import Agent
    agent = Agent.objects.create(owner=user, **data.dict())
    return {"id": agent.id, "name": agent.name}
```

---

## Best Practices

1.  **Async/Sync Boundary**: When using Django ORM (synchronous) inside FastAPI's `async def` routes, wrap blocking calls in `database_sync_to_async` (from `channels.db`) or run the endpoint as a standard `def`.
2.  **Connection Management**: Ensure database connections are properly handled, especially when sharing the same database between Django and FastAPI.
3.  **Schema Consistency**: Keep Pydantic schemas in sync with Django model definitions or use tools like `djantic` (if available) for automated schema generation.
4.  **Error Handling**: Use FastAPI's exception handlers to return standard JSON error responses that match the platform's API specification.
