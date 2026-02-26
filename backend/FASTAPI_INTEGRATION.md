# Django API 路由到 FastAPI 实现方案

## 概述

本项目提供三种方式将 Django API 路由到 FastAPI 内部实现：

1. **代理模式 (Proxy Mode)**: Django 作为反向代理，将请求转发到 FastAPI 服务
2. **混合 ASGI 模式 (Mixed ASGI)**: Django 和 FastAPI 运行在同一端口
3. **独立服务模式 (Standalone Mode)**: FastAPI 独立运行，通过 Nginx 路由

---

## 文件结构

```
backend/
├── fastapi_proxy.py              # Django 代理视图
├── fastapi_app/                  # FastAPI 应用目录
│   ├── __init__.py
│   └── main.py                   # FastAPI 主应用
├── core/
│   ├── asgi_fastapi.py          # 混合 ASGI 配置
│   └── urls_with_fastapi.py     # URL 配置示例
└── FASTAPI_INTEGRATION.md       # 本文档
```

---

## 方案 1: 代理模式 (推荐用于渐进式迁移)

### 原理
Django 视图接收请求，通过 HTTPX 异步转发到 FastAPI 服务，然后将响应返回给客户端。

### 使用步骤

1. **启动 FastAPI 服务**
```bash
cd backend
pip install -r requirements.txt
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload
```

2. **配置 Django URL 路由**
在 `core/urls.py` 中添加代理路由：

```python
from fastapi_proxy import FastAPIProxyView, FastAPIAgentProxyView

urlpatterns = [
    # ... 其他路由
    
    # 代理特定端点到 FastAPI
    path('api/v2/agents/', FastAPIAgentProxyView.as_view()),
    path('api/v2/tasks/', FastAPITaskProxyView.as_view()),
    
    # 或使用通用代理
    path('api/v2/fastapi/<path:path>', FastAPIProxyView.as_view()),
]
```

3. **启动 Django 服务**
```bash
python manage.py runserver 0.0.0.0:8000
```

### 优点
- 渐进式迁移，不影响现有 API
- 保持 Django 认证、中间件等
- 可针对特定端点逐步迁移

---

## 方案 2: 混合 ASGI 模式

### 原理
使用 Starlette 将 FastAPI 挂载到特定路径，Django 处理其他所有请求。

### 使用步骤

1. **修改 ASGI 配置**
使用 `core/asgi_fastapi.py` 替代默认的 `asgi.py`：

```python
# asgi.py
import os
from core.asgi_fastapi import application  # 使用混合 ASGI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
```

2. **启动混合服务**
```bash
uvicorn core.asgi_fastapi:application --host 0.0.0.0 --port 8000 --reload
```

3. **访问端点**
- Django API: `http://localhost:8000/api/v1/...`
- FastAPI: `http://localhost:8000/api/v2/fastapi/...`

### 优点
- 单端口运行
- 无需额外代理配置

### 缺点
- 复杂度较高
- 调试可能更困难

---

## 方案 3: 独立服务 + Nginx 路由

### 原理
Django 和 FastAPI 分别运行在不同端口，Nginx 根据路径路由请求。

### Nginx 配置

```nginx
server {
    listen 80;
    server_name api.example.com;

    # FastAPI 路由
    location /api/v2/agents/ {
        proxy_pass http://localhost:8001/api/v2/agents/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/v2/tasks/ {
        proxy_pass http://localhost:8001/api/v2/tasks/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Django 路由
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 优点
- 完全解耦
- 可独立扩展
- 性能最佳

### 缺点
- 需要 Nginx 配置
- 认证需要额外处理

---

## FastAPI 端点开发

### 复用 Django 模型

```python
# fastapi_app/main.py
import os
import sys
import django

# 初始化 Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# 导入模型
from agent.models import Agent
from task.models import Task

# 创建 FastAPI 端点
@app.get("/api/v2/agents")
async def list_agents():
    agents = Agent.objects.all()
    return [{"id": a.id, "name": a.name} for a in agents]
```

### 使用 Pydantic 进行数据验证

```python
from pydantic import BaseModel
from typing import Optional

class AgentCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

@app.post("/api/v2/agents")
async def create_agent(data: AgentCreateSchema):
    agent = Agent.objects.create(**data.dict())
    return {"id": agent.id, "name": agent.name}
```

---

## 认证集成

### 复用 Django JWT 认证

```python
# fastapi_app/auth.py
from fastapi import Depends, HTTPException, Header
import jwt
from django.conf import settings

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        from user.models import User
        user = User.objects.get(id=payload["user_id"])
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# 在端点中使用
@app.get("/api/v2/my-agents")
async def list_my_agents(user=Depends(get_current_user)):
    return Agent.objects.filter(owner=user)
```

---

## 部署建议

### Docker Compose 配置

```yaml
version: '3.8'

services:
  django:
    build: .
    command: gunicorn core.wsgi:application -b 0.0.0.0:8000
    ports:
      - "8000:8000"
    
  fastapi:
    build: .
    command: uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
    ports:
      - "8001:8001"
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

---

## 迁移策略

1. **第一阶段**: 选择需要高性能的端点（如 Agents、Tasks）迁移到 FastAPI
2. **第二阶段**: 使用代理模式验证 FastAPI 端点
3. **第三阶段**: 逐步将前端调用从 `/api/v1/` 切换到 `/api/v2/`
4. **第四阶段**: 完全迁移后，可考虑停用 Django REST Framework 端点

---

## 性能对比

| 方案 | 延迟 | 吞吐量 | 复杂度 |
|------|------|--------|--------|
| 代理模式 | 中等 | 中等 | 低 |
| 混合 ASGI | 低 | 高 | 中等 |
| Nginx 路由 | 低 | 高 | 高 |

---

## 注意事项

1. **数据库连接**: FastAPI 直接使用 Django ORM，确保在请求后关闭连接
2. **缓存**: 考虑使用 Redis 共享 Django 和 FastAPI 之间的缓存
3. **日志**: 统一日志格式便于排查问题
4. **测试**: 分别为 Django 和 FastAPI 编写单元测试
