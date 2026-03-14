# DataFlow-WebUI ASGI Module Integration

## Goal

将 DataFlow-WebUI 从独立服务（HTTP 代理）改为模块级整合：在 dcai-platform 的 ASGI 层直接挂载 DataFlow-WebUI 的 FastAPI 应用，消除两个进程的部署复杂度。

## Background

现有架构（双服务）：
```
Client → Django (/api/v2/dataflow/) → HTTP Proxy → FastAPI (localhost:8002/api/v1/)
```

目标架构（单进程 ASGI）：
```
Client → ASGI Router → Django (其他路由)
                     → FastAPI /api/v1/* (DataFlow-WebUI，路径重写)
```

**关键路径重写规则**：
- 入站：`/api/v2/dataflow/<path>` → FastAPI 内部：`/api/v1/<path>`

## Key Findings

1. **dcai-platform 当前是 WSGI**（wsgi.py），无 asgi.py，但有一个未使用的 `asgi_fastapi.py` 原型
2. **DataFlow-WebUI 无认证**：`X-DCAI-User-ID` 被注入但从未使用
3. **DataFlow-WebUI 在 WSGI 路由外**：只需 ASGI 层挂载，不影响 Django URL conf
4. **`os.chdir()` 风险**：`dataflow_setup.py` 调用 `os.chdir()` 会影响整个进程
5. **缺失依赖**：dcai-platform 需要 `pydantic_settings`, `loguru`（`ray`, `pandas` 检查后确认）

## Requirements

- [ ] 单进程运行：不再启动独立的 DataFlow-WebUI 服务
- [ ] 前端零改动：`/api/v2/dataflow/*` URL 保持不变
- [ ] 路径重写：ASGI 中间件将 `/api/v2/dataflow/<path>` → `/api/v1/<path>`
- [ ] 降级兼容：DataFlow-WebUI 不可用时回退到纯 Django ASGI
- [ ] 修复 `os.chdir()` 问题

## Acceptance Criteria

- [ ] `uvicorn core.asgi:application` 能正常启动
- [ ] `GET /api/v2/dataflow/pipelines/` 返回 200（由 FastAPI 处理）
- [ ] `GET /api/` 等 Django 路由正常（由 Django 处理）
- [ ] DataFlow-WebUI 模块不可 import 时，启动不崩溃

## Technical Notes

- 使用 `DATAFLOW_WEBUI_BACKEND_DIR` 环境变量指定 DataFlow-WebUI backend 目录
- DataFlow-WebUI 配置（`ENABLE_HF_API=false` 等）通过环境变量传入
- Django proxy_views.py 中的代理路由删除；packages 等纯 Django 视图保留
- 不需要修改 Django `urls.py` 中的 `api/v2/dataflow/` include（删除即可）
