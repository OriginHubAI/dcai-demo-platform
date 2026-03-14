# Python 高性能服务实现模式 / Python High-Performance Service Patterns

> **文档目的**: 介绍 Python 最新的并发机制和高性能服务实现模式
>
> **最后更新**: 2026-03-14

---

## 目录 / Table of Contents

1. [Python 并发模型概述](#python-并发模型概述)
2. [方案 1: asyncio + uvloop (Web 服务推荐)](#方案-1-asyncio--uvloop)
3. [方案 2: Python 3.13 Free-Threading (实验性)](#方案-2-python-313-free-threading)
4. [方案 3: 多进程 + 共享内存](#方案-3-多进程--共享内存)
5. [方案 4: 线程池 + 异步混合](#方案-4-线程池--异步混合)
6. [Django/FastAPI 性能优化](#djangofastapi-性能优化)
7. [性能对比](#性能对比)

---

## Python 并发模型概述

### GIL 的影响 / GIL Impact

```python
# GIL 限制示例
import threading
import time

def cpu_bound_task():
    """CPU 密集型任务 - 受 GIL 限制"""
    total = 0
    for i in range(10_000_000):
        total += i
    return total

# 多线程执行 CPU 密集型任务
start = time.time()
threads = [threading.Thread(target=cpu_bound_task) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"多线程: {time.time() - start:.2f}s")  # ~4s (无加速)

# 单线程执行
start = time.time()
for _ in range(4):
    cpu_bound_task()
print(f"单线程: {time.time() - start:.2f}s")  # ~4s (相同)
```

**结论**: 多线程对 CPU 密集型任务无效，因为 GIL 导致同一时刻只有一个线程执行 Python 字节码。

**Conclusion**: Multi-threading is ineffective for CPU-bound tasks due to GIL allowing only one thread to execute Python bytecode at a time.

---

## 方案 1: asyncio + uvloop

### 适用场景 / Use Cases

- ✅ Web API 服务 (Django, FastAPI)
- ✅ 数据库密集型应用
- ✅ 微服务间通信
- ✅ WebSocket 服务
- ❌ CPU 密集型计算

### 基础实现 / Basic Implementation

```python
import asyncio
import uvloop

# 使用 uvloop 替换默认事件循环 (性能提升 2-4x)
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def fetch_data(url: str):
    """异步 HTTP 请求"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def process_multiple_requests():
    """并发处理多个请求"""
    urls = [f"https://api.example.com/data/{i}" for i in range(100)]

    # 并发执行 100 个请求
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return results

# 运行
asyncio.run(process_multiple_requests())
```

### FastAPI 集成 / FastAPI Integration

```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/api/data/{item_id}")
async def get_data(item_id: int):
    """异步端点 - 自动使用 asyncio"""
    # 并发查询数据库和缓存
    db_task = fetch_from_db(item_id)
    cache_task = fetch_from_cache(item_id)

    db_result, cache_result = await asyncio.gather(db_task, cache_task)

    return {"db": db_result, "cache": cache_result}

if __name__ == "__main__":
    # 使用 uvloop 启动
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        loop="uvloop",  # 关键配置
        workers=4       # 多进程 worker
    )
```

### Django 异步视图 / Django Async Views

```python
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import asyncio

async def async_view(request):
    """Django 异步视图"""
    # 并发执行多个数据库查询
    users_task = sync_to_async(User.objects.all)()
    posts_task = sync_to_async(Post.objects.filter)(status='published')

    users, posts = await asyncio.gather(users_task, posts_task)

    return JsonResponse({
        'users': list(users.values()),
        'posts': list(posts.values())
    })
```

### 性能优化技巧 / Performance Tips

```python
# 1. 使用连接池
import httpx

# 全局客户端 (复用连接)
http_client = httpx.AsyncClient(
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    timeout=30.0
)

async def fetch_with_pool(url: str):
    response = await http_client.get(url)
    return response.json()

# 2. 限制并发数 (避免资源耗尽)
async def fetch_with_semaphore(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(url):
        async with semaphore:
            return await http_client.get(url)

    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)

# 3. 超时控制
async def fetch_with_timeout(url: str, timeout: float = 5.0):
    try:
        return await asyncio.wait_for(
            http_client.get(url),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return None
```

---

## 方案 2: Python 3.13 Free-Threading (实验性)

### 什么是 Free-Threading？

Python 3.13 引入了**实验性的无 GIL 模式** (PEP 703)，允许真正的多线程并行执行。

Python 3.13 introduces **experimental GIL-free mode** (PEP 703), enabling true multi-threaded parallel execution.

### 启用方式 / How to Enable

```bash
# 编译时启用 free-threading
./configure --disable-gil
make
make install

# 或使用预编译版本
python3.13t  # 't' 表示 free-threading 版本
```

### 使用示例 / Usage Example

```python
import threading
import time

def cpu_bound_task(n: int):
    """CPU 密集型任务"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# Python 3.13t (无 GIL)
start = time.time()
threads = [
    threading.Thread(target=cpu_bound_task, args=(10_000_000,))
    for _ in range(4)
]
for t in threads: t.start()
for t in threads: t.join()
print(f"Free-threading: {time.time() - start:.2f}s")  # ~1s (4x 加速)
```

### 注意事项 / Caveats

- ⚠️ **实验性功能** - 不建议生产环境使用
- ⚠️ **兼容性问题** - 部分 C 扩展可能不兼容
- ⚠️ **性能不稳定** - 某些场景可能比有 GIL 版本慢
- ✅ **未来趋势** - Python 3.14+ 可能成为默认选项

### 适用场景 / Use Cases

- CPU 密集型计算 (图像处理、数据分析)
- 科学计算
- 机器学习推理

---

## 方案 3: 多进程 + 共享内存

### 适用场景 / Use Cases

- ✅ CPU 密集型任务 (数据处理、计算)
- ✅ 需要绕过 GIL
- ❌ 进程间通信频繁的场景 (开销大)

### 基础实现 / Basic Implementation

```python
from multiprocessing import Pool, cpu_count
import numpy as np

def process_chunk(data_chunk):
    """处理数据块 - 在独立进程中运行"""
    return np.sum(data_chunk ** 2)

def parallel_processing(data: np.ndarray):
    """多进程并行处理"""
    # 分割数据
    chunk_size = len(data) // cpu_count()
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # 多进程处理
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_chunk, chunks)

    return sum(results)

# 使用
data = np.random.rand(10_000_000)
result = parallel_processing(data)
```

### 共享内存优化 / Shared Memory Optimization

```python
from multiprocessing import Pool, shared_memory
import numpy as np

def process_shared_chunk(shm_name: str, shape: tuple, start: int, end: int):
    """处理共享内存中的数据块"""
    # 连接到共享内存
    shm = shared_memory.SharedMemory(name=shm_name)
    data = np.ndarray(shape, dtype=np.float64, buffer=shm.buf)

    # 处理数据块
    result = np.sum(data[start:end] ** 2)

    shm.close()
    return result

def parallel_with_shared_memory(data: np.ndarray):
    """使用共享内存避免数据复制"""
    # 创建共享内存
    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    shared_data = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    shared_data[:] = data[:]

    # 分配任务
    chunk_size = len(data) // cpu_count()
    tasks = [
        (shm.name, data.shape, i, min(i + chunk_size, len(data)))
        for i in range(0, len(data), chunk_size)
    ]

    # 多进程处理
    with Pool(processes=cpu_count()) as pool:
        results = pool.starmap(process_shared_chunk, tasks)

    # 清理
    shm.close()
    shm.unlink()

    return sum(results)
```

---

## 方案 4: 线程池 + 异步混合

### 适用场景 / Use Cases

- 混合 I/O 和 CPU 任务
- 需要调用阻塞的同步库
- Django/FastAPI 中调用同步代码

### 实现模式 / Implementation Pattern

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# 全局线程池
executor = ThreadPoolExecutor(max_workers=10)

def blocking_io_task(n: int):
    """阻塞的 I/O 任务 (如调用同步库)"""
    time.sleep(1)  # 模拟阻塞操作
    return n * 2

async def async_with_thread_pool():
    """在异步代码中运行阻塞任务"""
    loop = asyncio.get_event_loop()

    # 在线程池中运行阻塞任务
    tasks = [
        loop.run_in_executor(executor, blocking_io_task, i)
        for i in range(10)
    ]

    results = await asyncio.gather(*tasks)
    return results

# 运行
asyncio.run(async_with_thread_pool())
```

### Django 集成 / Django Integration

```python
from asgiref.sync import sync_to_async
from concurrent.futures import ThreadPoolExecutor
import asyncio

# 自定义线程池
custom_executor = ThreadPoolExecutor(max_workers=20)

async def django_async_view(request):
    """Django 异步视图 - 使用自定义线程池"""

    # 方式 1: 使用 sync_to_async
    @sync_to_async
    def get_users():
        return list(User.objects.all())

    # 方式 2: 使用自定义线程池
    loop = asyncio.get_event_loop()
    users = await loop.run_in_executor(
        custom_executor,
        lambda: list(User.objects.all())
    )

    return JsonResponse({'users': users})
```

### FastAPI 集成 / FastAPI Integration

```python
from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=20)

def cpu_intensive_task(data: dict):
    """CPU 密集型任务"""
    # 复杂计算...
    return processed_data

@app.post("/api/process")
async def process_data(data: dict):
    """在线程池中运行 CPU 密集型任务"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        cpu_intensive_task,
        data
    )
    return {"result": result}
```


---

## Django/FastAPI 性能优化

### 针对当前项目的优化建议 / Optimization for Current Project

基于 `dcai-platform` 的架构（Django + FastAPI 同进程），以下是具体优化方案：

Based on `dcai-platform` architecture (Django + FastAPI in same process), here are specific optimizations:

#### 1. 使用 uvloop 启动 ASGI 服务

```bash
# 当前启动方式
conda run -n dataflow uvicorn core.asgi:application --host 0.0.0.0 --port 18000

# 优化后启动方式 (使用 uvloop)
conda run -n dataflow uvicorn core.asgi:application \
    --host 0.0.0.0 \
    --port 18000 \
    --loop uvloop \
    --workers 4
```

**性能提升**: 2-4x 吞吐量提升

#### 2. Django 数据库连接池优化

```python
# backend/core/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'CONN_MAX_AGE': 600,  # 连接复用 10 分钟
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000'  # 30s 查询超时
        }
    }
}
```

#### 3. FastAPI 异步数据库查询

```python
# dataflow-webui/backend/app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 异步引擎 + 连接池
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # 连接池大小
    max_overflow=10,       # 最大溢出连接
    pool_pre_ping=True,    # 连接健康检查
    pool_recycle=3600      # 1 小时回收连接
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 使用示例
async def get_datasets():
    async with async_session() as session:
        result = await session.execute(select(Dataset))
        return result.scalars().all()
```

#### 4. Redis 连接池优化

```python
# backend/core/cache.py
import redis.asyncio as redis

# 全局连接池
redis_pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379",
    max_connections=50,
    decode_responses=True
)

async def get_redis_client():
    """获取 Redis 客户端"""
    return redis.Redis(connection_pool=redis_pool)

# 使用示例
async def cache_get(key: str):
    client = await get_redis_client()
    return await client.get(key)
```

#### 5. httpx 客户端复用

```python
# backend/df/client.py (优化前)
def list_operators(self):
    with httpx.Client() as client:  # 每次创建新连接
        response = client.get(url)
        return response.json()

# backend/df/client.py (优化后)
class DataflowClient:
    def __init__(self):
        self._client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=100),
            timeout=30.0
        )

    async def list_operators(self):
        response = await self._client.get(url)
        return response.json()

    async def close(self):
        await self._client.aclose()

# 全局单例
dataflow_client = DataflowClient()
```

---

## 性能对比

### 并发模型性能对比 / Concurrency Model Performance Comparison

| 模型 | I/O 密集型 (req/s) | CPU 密集型 (tasks/s) | 内存占用 | 复杂度 |
|------|-------------------|---------------------|---------|--------|
| 单线程同步 | 100 | 10 | 低 | 低 |
| 多线程 (threading) | 500 | 10 | 中 | 中 |
| asyncio | 5,000 | 10 | 低 | 中 |
| asyncio + uvloop | 10,000 | 10 | 低 | 中 |
| 多进程 | 200 | 40 | 高 | 高 |
| Python 3.13t (free-threading) | 500 | 40 | 中 | 中 |

### 实际场景性能测试 / Real-World Performance Test

```python
import asyncio
import time
import httpx

# 测试场景: 100 个并发 HTTP 请求
async def benchmark_async():
    """异步方式"""
    async with httpx.AsyncClient() as client:
        tasks = [client.get("http://localhost:8000/api/test") for _ in range(100)]
        start = time.time()
        await asyncio.gather(*tasks)
        return time.time() - start

def benchmark_sync():
    """同步方式"""
    with httpx.Client() as client:
        start = time.time()
        for _ in range(100):
            client.get("http://localhost:8000/api/test")
        return time.time() - start

# 结果对比
# 同步: ~10s (串行执行)
# 异步: ~0.5s (并发执行, 20x 提升)
```

---

## 最佳实践总结 / Best Practices Summary

### 选择合适的并发模型 / Choose the Right Concurrency Model

```
任务类型判断流程:

Web API 服务?
├─ Yes → asyncio + uvloop ✅
└─ No → 继续判断

CPU 密集型?
├─ Yes → 多进程 (multiprocessing) ✅
└─ No → 继续判断

需要调用阻塞库?
├─ Yes → 线程池 + asyncio 混合 ✅
└─ No → asyncio ✅
```

### 关键优化点 / Key Optimization Points

1. **使用 uvloop** - FastAPI/Django ASGI 服务必备
2. **连接池复用** - 数据库、Redis、HTTP 客户端
3. **限制并发数** - 使用 Semaphore 避免资源耗尽
4. **超时控制** - 所有 I/O 操作设置超时
5. **避免阻塞** - 在异步代码中使用 `run_in_executor` 运行阻塞操作

### 常见陷阱 / Common Pitfalls

```python
# ❌ 错误: 在异步函数中使用同步 I/O
async def bad_example():
    time.sleep(1)  # 阻塞整个事件循环!
    return "done"

# ✅ 正确: 使用异步 I/O
async def good_example():
    await asyncio.sleep(1)  # 不阻塞事件循环
    return "done"

# ❌ 错误: 在循环中创建连接
async def bad_http():
    for url in urls:
        async with httpx.AsyncClient() as client:  # 每次创建新连接
            await client.get(url)

# ✅ 正确: 复用连接
async def good_http():
    async with httpx.AsyncClient() as client:  # 复用连接
        tasks = [client.get(url) for url in urls]
        await asyncio.gather(*tasks)
```

---

## 针对 dcai-platform 的具体建议

### 立即可实施的优化 / Immediate Optimizations

1. **启用 uvloop**
   ```bash
   # 修改启动脚本
   uvicorn core.asgi:application --loop uvloop --workers 4
   ```

2. **优化 Django 数据库连接**
   ```python
   # settings.py
   DATABASES['default']['CONN_MAX_AGE'] = 600
   ```

3. **FastAPI 使用异步数据库查询**
   ```python
   # 将同步查询改为异步
   from sqlalchemy.ext.asyncio import AsyncSession
   ```

### 中期优化 / Medium-Term Optimizations

1. **将 Django → FastAPI 的 HTTP 调用改为直接函数调用**
   - 参考 `docs/django_fastapi_communication.md` 中的方案 1

2. **引入 Redis 连接池**
   - 避免每次请求创建新连接

3. **优化 httpx 客户端**
   - 使用全局单例 + 连接池

### 长期优化 / Long-Term Optimizations

1. **评估 Python 3.13 free-threading**
   - 适用于 CPU 密集型任务（如数据处理）

2. **考虑微服务拆分**
   - 将 CPU 密集型任务拆分为独立服务

3. **引入消息队列**
   - 使用 Redis Pub/Sub 或 RabbitMQ 处理异步任务

---

## 参考资源 / References

- [PEP 703: Making the Global Interpreter Lock Optional](https://peps.python.org/pep-0703/)
- [uvloop Documentation](https://uvloop.readthedocs.io/)
- [FastAPI Performance Tips](https://fastapi.tiangolo.com/deployment/concepts/)
- [Django Async Views](https://docs.djangoproject.com/en/stable/topics/async/)

---

**文档维护**: 当发现新的性能优化模式时，请更新本文档。

