# Django 与 FastAPI 通信架构 / Django-FastAPI Communication Architecture

> **文档目的 / Document Purpose**: 说明 dcai-platform (Django) 与 dataflow-webui (FastAPI) 之间的通信机制
>
> **最后更新 / Last Updated**: 2026-03-14

---

## 目录 / Table of Contents

1. [架构概述](#架构概述--architecture-overview)
2. [通信方式 1: ASGI 路由分发](#通信方式-1-asgi-路由分发)
3. [通信方式 2: HTTP 代理](#通信方式-2-http-代理)
4. [路由规则详解](#路由规则详解)
5. [通信流程图](#通信流程图)
6. [性能分析](#性能分析)
7. [潜在问题与改进建议](#潜在问题与改进建议)

---

## 架构概述 / Architecture Overview

dcai-platform 和 dataflow-webui 运行在 **同一个 ASGI 进程** 中，通过 `backend/core/asgi.py` 中的路由分发器统一管理。

dcai-platform and dataflow-webui run in the **same ASGI process**, managed by a unified route dispatcher in `backend/core/asgi.py`.

### 核心架构 / Core Architecture

```
┌─────────────────────────────────────────────────┐
│         ASGI Process (Port 18000)               │
│                                                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │   Django     │         │   FastAPI       │  │
│  │   Backend    │         │   (DataFlow)    │  │
│  └──────┬───────┘         └────────┬────────┘  │
│         │                          │           │
│         │  ① ASGI 路由 (零开销)     │           │
│         │◄────────────────────────►│           │
│         │                          │           │
│         │  ② HTTP Proxy (httpx)    │           │
│         │─────────────────────────►│           │
│         │                          │           │
│         │  ③ 反向调用 (HF API)      │           │
│         │◄─────────────────────────│           │
└─────────┴──────────────────────────┴───────────┘
```

### 两种通信方式 / Two Communication Approaches

| 方式 | 机制 | 延迟 | 使用场景 |
|------|------|------|----------|
| **ASGI 路由** | 同进程 ASGI 调用 | <0.1ms | 前端直接访问 FastAPI |
| **HTTP 代理** | httpx HTTP 请求 | 1-5ms | Django 主动调用 FastAPI |

---

## 通信方式 1: ASGI 路由分发

### 实现位置 / Implementation Location

**文件**: `backend/core/asgi.py`

### 核心代码 / Core Code

```python
async def application(scope, receive, send):
    """ASGI 应用入口 - 根据路径分发到 Django 或 FastAPI"""
    if scope["type"] in ("http", "websocket"):
        rewritten = _rewrite(scope.get("path", ""))
        if rewritten is not None:
            # 路由到 FastAPI (同进程，零网络开销)
            await _dataflow_app(scope, receive, send)
            return
    # 默认路由到 Django
    await django_app(scope, receive, send)
```

### 路径重写逻辑 / Path Rewrite Logic

```python
def _rewrite(path: str):
    """将请求路径重写为 FastAPI 内部路径"""

    # 1. 前端静态资源
    # /embedded/dataflow-webui/foo  →  /foo
    if path.startswith("/embedded/dataflow-webui/"):
        return path[len("/embedded/dataflow-webui/") - 1:]

    # 2. FastAPI API 直通
    # /api/v1/operators/  →  /api/v1/operators/ (不变)
    if path.startswith("/api/v1/"):
        suffix = path[len("/api/v1/"):]
        if suffix.startswith(("operators/", "tasks/", "pipelines/", "datasets/")):
            return path

    # 3. 兼容路径重写
    # /api/v2/dataflow/datasets/foo  →  /api/v1/datasets/foo
    if path.startswith("/api/v2/dataflow/"):
        suffix = path[len("/api/v2/dataflow/"):]
        if suffix.startswith(("datasets/", "serving/", "prompts/")):
            return "/api/v1/" + suffix

    return None  # 交给 Django 处理
```

### 特点 / Characteristics

- ✅ **零网络开销** - 同进程内 ASGI 调用，无序列化成本
- ✅ **透明路由** - 前端无需知道后端是 Django 还是 FastAPI
- ✅ **高性能** - 延迟 <0.1ms
- ✅ **支持 WebSocket** - 可以路由 WebSocket 连接

---

## 通信方式 2: HTTP 代理

### 实现位置 / Implementation Location

**文件**: `backend/df/proxy_views.py`, `backend/df/client.py`

### 场景 1: Django 代理视图 / Django Proxy Views

Django 接收请求后，通过 httpx 转发到 FastAPI。

Django receives requests and forwards them to FastAPI via httpx.

```python
# backend/df/proxy_views.py
DATAFLOW_BACKEND_URL = 'http://localhost:8002'  # 默认配置

def _proxy(request, target_url: str, stream: bool = False):
    """通用代理函数"""
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ['host', 'authorization', 'content-length']
    }
    # 传递用户 ID
    headers['X-DCAI-User-ID'] = str(getattr(request.user, 'id', '') or 'anonymous')

    with httpx.Client(timeout=120) as client:
        resp = client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=request.body,
            params=request.GET.dict(),
        )
    return HttpResponse(resp.content, status=resp.status_code)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def operator_subpath_proxy(request, subpath=''):
    """代理 operator 请求"""
    target = f"{DATAFLOW_BACKEND_URL}/api/v1/operators/{subpath}"
    return _proxy(request, target)
```

### 场景 2: Django 客户端调用 / Django Client Calls

Django 业务逻辑主动调用 FastAPI API。

Django business logic actively calls FastAPI APIs.

```python
# backend/df/client.py
class DataflowClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.DATAFLOW_MOCK_URL
        self.api_url = f"{self.base_url.rstrip('/')}/api/v1"

    def list_operators(self):
        """获取所有可用的 operators"""
        url = f"{self.api_url}/operators"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()

    def create_pipeline(self, pipeline_request: dict):
        """创建 pipeline"""
        url = f"{self.api_url}/pipelines/create"
        with httpx.Client() as client:
            response = client.post(url, json=pipeline_request)
            return response.json()
```

### 场景 3: FastAPI 反向调用 Django / FastAPI Calls Back to Django

FastAPI 调用 Django 的 HF API。

FastAPI calls Django's HF API.

```python
# backend/core/asgi.py (配置)
os.environ.setdefault("EXTERNAL_HF_API_URL", "http://localhost:18000/api/hf")

# dataflow-webui/backend 中使用
# FastAPI 通过 EXTERNAL_HF_API_URL 调用 Django 的 HF datasets 服务
```

### 特点 / Characteristics

- ⚠️ **有网络开销** - HTTP 请求/响应序列化，延迟 1-5ms
- ✅ **灵活** - 可以添加认证、日志、错误处理等中间层逻辑
- ✅ **支持流式响应** - 用于长轮询场景 (如 `/tasks/newly`)
- ✅ **易于拆分** - 未来可以轻松拆分为独立微服务

---

## 路由规则详解

### 完整路由表 / Complete Routing Table

| 请求路径 | 处理方 | 重写后路径 | 说明 |
|---------|--------|-----------|------|
| `/embedded/dataflow-webui/*` | FastAPI | `/*` | 前端静态资源 |
| `/embedded/dataflow-backend/*` | FastAPI | `/*` | 前端 API 调用 |
| `/api/v1/operators/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v1/tasks/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v1/pipelines/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v1/datasets/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v1/serving/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v1/prompts/*` | FastAPI | 不变 | 直通 (passthrough) |
| `/api/v2/dataflow/datasets/*` | FastAPI | `/api/v1/datasets/*` | 兼容路径重写 |
| `/api/v2/dataflow/serving/*` | FastAPI | `/api/v1/serving/*` | 兼容路径重写 |
| `/api/v2/dataflow/prompts/*` | FastAPI | `/api/v1/prompts/*` | 兼容路径重写 |
| `/api/v2/dataflow/operators/*` | Django | - | Django 代理到 FastAPI |
| `/api/v2/dataflow/tasks/*` | Django | - | Django 代理到 FastAPI |
| `/api/v2/dataflow/pipelines/*` | Django | - | Django 代理到 FastAPI |
| `/api/hf/*` | Django | - | HF datasets 服务 |
| 其他所有路径 | Django | - | 默认处理 |


### 循环调用问题 / Circular Call Issue

**问题场景 / Problem Scenario:**

```
前端 → /api/v2/dataflow/operators/xxx 
    → Django proxy_views 
    → httpx → http://localhost:8002/api/v1/operators/xxx
    → ??? (可能再次进入 Django，造成循环)
```

**解决方案 / Solution:**

ASGI 分发器会拦截 `/api/v1/operators/*` 等路径，直接路由到 FastAPI，避免循环。

The ASGI dispatcher intercepts `/api/v1/operators/*` paths and routes directly to FastAPI, preventing loops.

```python
# backend/core/asgi.py (line 91-93)
# operators/, tasks/, pipelines/ MUST stay here so that the 
# self-referential httpx call from Django proxy_views is caught
# by Rule 2 and forwarded to in-process FastAPI
```

---

## 通信流程图

### 流程 1: 前端直接访问 FastAPI (ASGI 路由)

```
┌─────────┐
│  前端    │
└────┬────┘
     │ GET /api/v1/operators/
     ▼
┌─────────────────────────────┐
│  ASGI Dispatcher            │
│  (backend/core/asgi.py)     │
└────┬────────────────────────┘
     │ _rewrite() → /api/v1/operators/
     │ (匹配 FastAPI 路由规则)
     ▼
┌─────────────────────────────┐
│  FastAPI App                │
│  (dataflow-webui/backend)   │
└────┬────────────────────────┘
     │ 返回 JSON 响应
     ▼
┌─────────┐
│  前端    │
└─────────┘

延迟: <0.1ms (零网络开销)
```

### 流程 2: Django 代理到 FastAPI (HTTP)

```
┌─────────┐
│  前端    │
└────┬────┘
     │ GET /api/v2/dataflow/operators/xxx
     ▼
┌─────────────────────────────┐
│  ASGI Dispatcher            │
└────┬────────────────────────┘
     │ _rewrite() → None
     │ (不匹配 FastAPI 规则)
     ▼
┌─────────────────────────────┐
│  Django App                 │
│  (backend/df/proxy_views)   │
└────┬────────────────────────┘
     │ httpx.get(http://localhost:8002/api/v1/operators/xxx)
     ▼
┌─────────────────────────────┐
│  ASGI Dispatcher            │
│  (拦截 /api/v1/operators/)  │
└────┬────────────────────────┘
     │ 路由到 FastAPI (避免循环)
     ▼
┌─────────────────────────────┐
│  FastAPI App                │
└────┬────────────────────────┘
     │ 返回 JSON
     ▼
┌─────────────────────────────┐
│  Django proxy_views         │
└────┬────────────────────────┘
     │ 返回给前端
     ▼
┌─────────┐
│  前端    │
└─────────┘

延迟: 1-5ms (有 HTTP 序列化开销)
```

### 流程 3: FastAPI 反向调用 Django HF API

```
┌─────────────────────────────┐
│  FastAPI App                │
│  (需要 HF datasets 数据)    │
└────┬────────────────────────┘
     │ httpx.get(http://localhost:18000/api/hf/datasets/xxx)
     ▼
┌─────────────────────────────┐
│  ASGI Dispatcher            │
└────┬────────────────────────┘
     │ _rewrite() → None
     │ (不匹配 FastAPI 规则)
     ▼
┌─────────────────────────────┐
│  Django App                 │
│  (backend/hf/)              │
└────┬────────────────────────┘
     │ 返回 HF datasets 数据
     ▼
┌─────────────────────────────┐
│  FastAPI App                │
└─────────────────────────────┘

延迟: 1-5ms
```

---

## 性能分析

### 延迟对比 / Latency Comparison

| 通信方式 | 平均延迟 | 适用场景 | 吞吐量 |
|---------|---------|----------|--------|
| ASGI 路由 | <0.1ms | 前端直接访问 FastAPI | 极高 (>10k req/s) |
| HTTP 代理 (同机) | 1-5ms | Django 调用 FastAPI | 高 (>1k req/s) |
| HTTP 代理 (跨机) | 10-50ms | 未来微服务拆分 | 中 (>100 req/s) |

### 性能瓶颈分析 / Performance Bottleneck Analysis

1. **ASGI 路由** - 几乎无瓶颈，受限于业务逻辑本身
2. **HTTP 代理** - 瓶颈在于：
   - JSON 序列化/反序列化
   - HTTP 连接建立 (可用连接池优化)
   - 请求/响应复制

### 优化建议 / Optimization Recommendations

1. **减少 HTTP 代理使用** - 将 Django 调用 FastAPI 的场景改为直接函数调用
2. **使用连接池** - httpx.Client 复用连接
3. **异步调用** - 使用 httpx.AsyncClient 提升并发性能
4. **缓存热点数据** - 使用 Redis 缓存频繁访问的数据


---

## 潜在问题与改进建议

### 当前架构的问题 / Current Architecture Issues

#### 1. 循环调用风险 / Circular Call Risk

**问题 / Issue:**
- Django 通过 HTTP 调用 FastAPI 时，如果 ASGI 路由配置不当，可能造成无限循环

**解决方案 / Solution:**
- ✅ 已通过 ASGI 分发器拦截 `/api/v1/*` 路径避免循环
- ⚠️ 需要仔细维护路由规则，避免引入新的循环路径

#### 2. HTTP 代理开销 / HTTP Proxy Overhead

**问题 / Issue:**
- Django → FastAPI 的 HTTP 调用有 1-5ms 延迟
- 高频调用场景下会成为性能瓶颈

**改进建议 / Improvement:**
```python
# 当前方式 (HTTP 代理)
def get_operators():
    with httpx.Client() as client:
        resp = client.get(f"{DATAFLOW_BACKEND_URL}/api/v1/operators")
        return resp.json()

# 改进方式 (直接函数调用)
from asgiref.sync import sync_to_async
from dataflow_webui.services import get_operators_list

async def get_operators():
    # 直接调用 FastAPI 的服务层函数
    return await get_operators_list()
```

#### 3. 配置复杂度 / Configuration Complexity

**问题 / Issue:**
- 需要配置 `DATAFLOW_BACKEND_URL`
- 开发环境和生产环境配置不同
- 容易出现配置错误

**改进建议 / Improvement:**
- 统一使用环境变量管理
- 提供默认值和自动检测机制
- 添加配置验证和健康检查

---

## 改进方案建议

### 方案 1: 直接函数调用 (推荐)

**适用场景 / Use Cases:**
- Django 需要频繁调用 FastAPI 的业务逻辑
- 对性能要求高的场景

**实现示例 / Implementation:**

```python
# 创建共享服务层 / Create shared service layer
# backend/shared/dataflow_services.py

from asgiref.sync import sync_to_async

# 导入 FastAPI 的服务函数
from dataflow_webui.app.services.operators import get_all_operators

async def fetch_operators():
    """Django 异步调用 FastAPI 服务"""
    return await get_all_operators()

def fetch_operators_sync():
    """Django 同步调用 FastAPI 服务"""
    import asyncio
    return asyncio.run(fetch_operators())
```

```python
# Django 视图中使用
from backend.shared.dataflow_services import fetch_operators_sync

def operators_view(request):
    operators = fetch_operators_sync()
    return JsonResponse({'operators': operators})
```

**优点 / Advantages:**
- ✅ 零网络开销
- ✅ 类型安全
- ✅ 易于调试

**缺点 / Disadvantages:**
- ⚠️ 需要处理同步/异步转换
- ⚠️ 增加代码耦合度

---

### 方案 2: 共享 Redis 缓存

**适用场景 / Use Cases:**
- 临时状态共享
- 任务状态跟踪
- 会话数据

**实现示例 / Implementation:**

```python
# Django 写入
from django.core.cache import cache

def create_task(task_data):
    task = Task.objects.create(**task_data)
    # 写入 Redis 供 FastAPI 读取
    cache.set(f'task:{task.id}', {
        'id': task.id,
        'status': task.status,
        'config': task.config
    }, timeout=300)
    return task
```

```python
# FastAPI 读取
import redis.asyncio as redis

async def get_task_status(task_id: str):
    r = await redis.from_url("redis://localhost:6379")
    cached = await r.get(f'task:{task_id}')
    if cached:
        return json.loads(cached)
    # 缓存未命中，查询数据库
    return await query_database(task_id)
```

---

### 方案 3: 消息队列 (异步任务)

**适用场景 / Use Cases:**
- Django 触发 FastAPI 异步任务
- 解耦长时间运行的任务

**实现示例 / Implementation:**

```python
# Django 发布任务
import redis

def trigger_pipeline_task(pipeline_id: str):
    r = redis.Redis()
    r.publish('pipeline_tasks', json.dumps({
        'pipeline_id': pipeline_id,
        'timestamp': time.time()
    }))
```

```python
# FastAPI 消费任务
import redis.asyncio as redis

async def task_consumer():
    r = await redis.from_url("redis://localhost:6379")
    pubsub = r.pubsub()
    await pubsub.subscribe('pipeline_tasks')
    
    async for message in pubsub.listen():
        if message['type'] == 'message':
            await process_pipeline(json.loads(message['data']))
```

---

## 总结 / Summary

### 当前架构优点 / Current Architecture Advantages

1. ✅ **单进程部署** - 简化运维，降低资源消耗
2. ✅ **高性能路由** - ASGI 零开销分发
3. ✅ **灵活扩展** - 可以轻松拆分为独立微服务
4. ✅ **透明集成** - 前端无需关心后端架构

### 关键要点 / Key Takeaways

1. **优先使用 ASGI 路由** - 前端访问 FastAPI 时性能最优
2. **谨慎使用 HTTP 代理** - 仅在必要时使用，注意性能开销
3. **避免循环调用** - 仔细维护路由规则
4. **考虑直接函数调用** - Django 调用 FastAPI 时可以直接导入函数
5. **使用 Redis 共享状态** - 临时数据和任务状态

### 未来优化方向 / Future Optimization Directions

1. **减少 HTTP 代理** - 将高频调用改为直接函数调用
2. **引入连接池** - 优化 httpx 客户端性能
3. **添加监控** - 监控各通信路径的延迟和错误率
4. **文档化路由规则** - 避免配置错误导致的循环调用

---

## 相关文件 / Related Files

| 文件 | 说明 |
|------|------|
| `backend/core/asgi.py` | ASGI 路由分发器 |
| `backend/df/proxy_views.py` | Django HTTP 代理视图 |
| `backend/df/client.py` | Django 调用 FastAPI 的客户端 |
| `backend/core/settings.py` | 配置文件 (DATAFLOW_BACKEND_URL) |
| `dataflow-webui/backend/app/main.py` | FastAPI 应用入口 |

---

**文档维护 / Document Maintenance:**
- 当路由规则变化时，及时更新本文档
- 当发现新的性能问题时，添加到"潜在问题"章节
- 当实施优化方案后，更新"改进建议"章节

