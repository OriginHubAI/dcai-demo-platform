# FastAPI Microservice Guidelines

> Guidelines for developing internal microservices (e.g., DataFlow-Sys, LoopAI) and data plane components using FastAPI.

---

## Architecture & Role

FastAPI serves as the backbone for high-performance, asynchronous microservices within the DCAI Platform. While Django acts as the primary Gateway/IdP, FastAPI is used for:

1. **Data Plane Operations**: High-throughput data ingestion, processing, and streaming (Datasets API).
2. **AI/ML Workloads**: Managing long-running DataFlow operators, LLM inference, and Agent tracking.
3. **Compute-Heavy/Async Tasks**: Logic that benefits from non-blocking I/O.

---

## 1. Project Structure (Microservices)

Keep FastAPI apps modular, using `APIRouter` to organize endpoints by domain.

```text
src/
├── main.py               # FastAPI application instance & middlewares
├── api/
│   ├── dependencies.py   # Auth, DB sessions (Depends)
│   └── routes/           # APIRouters (e.g., datasets.py, operators.py)
├── core/
│   ├── config.py         # Pydantic BaseSettings
│   └── security.py       # JWT validation (shared secret with Django)
├── models/               # SQLAlchemy/Tortoise ORM models (if applicable)
├── schemas/              # Pydantic models (Input/Output validation)
└── services/             # Core business logic (separated from HTTP)
```

## 2. Pydantic Models (Schemas)

Always use Pydantic models for request validation and response serialization. Ensure standard response shapes.

```python
# schemas/operator.py
from pydantic import BaseModel, ConfigDict, Field

class OperatorCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    config: dict

class OperatorResponse(OperatorCreate):
    id: str
    status: str

    model_config = ConfigDict(from_attributes=True)
```

## 3. Dependency Injection

Use `Depends` to manage shared logic like Database Sessions and Authentication context injected by Django.

```python
# api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user_from_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT signed by the Django Gateway."""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            "SHARED_SECRET", 
            algorithms=["HS256"]
        )
        return {"user_id": payload.get("user_id")}
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
```

## 4. Async Performance & Blocking I/O

FastAPI relies on ASGI. Avoid synchronous blocking operations inside `async def` routes.

- **BAD**:
  ```python
  import time
  @app.get("/heavy")
  async def heavy_computation():
      time.sleep(5)  # Blocks the entire event loop!
      return {"status": "done"}
  ```

- **GOOD**: Run blocking code in a thread pool (e.g., `run_in_threadpool` or declaring endpoint as `def` instead of `async def`), or use asyncio counterparts.
  ```python
  import asyncio
  
  @app.get("/light_async")
  async def async_wait():
      await asyncio.sleep(5) # Event loop remains free
      return {"status": "done"}

  # FastAPI runs normal `def` in a separate threadpool automatically
  @app.get("/heavy_sync")
  def heavy_computation():
      time.sleep(5) 
      return {"status": "done"}
  ```

## 5. Streaming & Data Plane (Large Files)

When handling large datasets (upload or download), stream the data to avoid memory bloat.

```python
# api/routes/datasets.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()

async def generate_large_csv():
    # Yield chunks of data rather than building a huge string
    for i in range(1000000):
        yield f"{i},value_{i}\n".encode('utf-8')

@router.get("/download")
async def download_dataset():
    """Stream response directly to client without buffering in memory."""
    return StreamingResponse(
        generate_large_csv(), 
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=large.csv"}
    )
```

## 6. Error Handling

Define custom Exception Handlers globally to maintain a consistent error response format matching the Django Gateway.

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class ServiceException(Exception):
    def __init__(self, name: str, code: int):
        self.name = name
        self.code = code

@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        status_code=exc.code,
        content={"detail": exc.name},
    )
```

---

## Summary

| Policy                 | Implementation                          |
| ---------------------- | --------------------------------------- |
| **Data Validation**    | Pydantic schemas (`BaseModel`)          |
| **Authentication**     | Validate Django JWT using `Depends()`   |
| **Logic Separation**   | Use `APIRouter` and `services/` layer   |
| **Blocking Core**      | Use `async/await` safely, no `time.sleep` in `async` |
| **Data Plane**         | Use `StreamingResponse` for chunks      |
| **Error Format**       | Global Exception Handlers returning JSON|
