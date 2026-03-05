# Backend Architecture and API Documentation

## 1. 系统架构概述 (System Architecture Overview)

DCAI (Data-Centric AI) 平台的后端采用了 **Django + FastAPI** 的混合架构模式，结合了两者的优势：Django 强大的生态和 ORM 功能，以及 FastAPI 在异步处理和高性能 API 方面的卓越表现。

### 1.1 核心技术栈
- **Django**: 作为主框架，处理用户认证、管理后台、复杂的业务逻辑以及作为主要的入口。
- **FastAPI**: 用于处理需要高吞吐量和低延迟的 API 端点（例如 Agent 交互、Task 异步处理）。
- **Django REST Framework (DRF)**: 用于快速构建标准的 RESTful API。
- **SQLite / PostgreSQL**: 数据库存储（开发环境使用 SQLite，生产环境推荐 PostgreSQL）。
- **Redis & Celery**: 用于缓存、异步任务队列处理。

### 1.2 架构集成模式
根据 `FASTAPI_INTEGRATION.md`，系统支持三种接入模式以融合 Django 与 FastAPI：
1. **代理模式 (Proxy Mode)** (推荐用于渐进式迁移)：Django 视图作为反向代理，利用异步 HTTPX 将请求透明地转发给后端的 FastAPI 服务。
2. **混合 ASGI 模式**: 使用 Starlette 将 FastAPI 挂载到 Django 的特定路线上，实现单端口同进程运行。
3. **独立服务 + Nginx 路由**: Django 与 FastAPI 分别在不同的端口运行，由 Nginx 根据路径（如 `/api/v2/agents/` 转发给 FastAPI，`/` 转发给 Django）进行分发，实现完全解耦和最佳性能。

---

## 2. 核心功能模块划分 (Core Modules & Functionalities)

项目的 `backend/` 目录下按照业务逻辑划分了多个核心模块（Apps），主要包括：

- **user (用户管理)**: 处理用户注册、登录（邮箱、手机号、微信、GitHub OAuth）、密码找回、Token 刷新及包含验证码和邀请码机制。
- **agent (智能体管理)**: 核心业务之一，管理智能体的创建、更新、分享、订阅及运行所需调用的第三方 API 工具集的配置。
- **chat / llm_chat (聊天会话)**: 管理端到端的聊天流程。支持与系统预设或自定义 Agent 的会话交互，提供流式 (SSE) 答复。并允许进行会话分享。
- **knowledgebase / document (知识库与文档)**: 管理企业或个人的知识库（支持按分组管理），支持在知识库中上传文件、文档解析片段 (Chunks) 的检索和搜索历史记录。
- **dataset (数据集)**: 分为 V1 和 V2 版本（V2 基于 ViewSet）。提供数据集的元数据管理、数据集文件管理以及对象存储 (Object Storage) 的配置整合。
- **collection (收藏夹)**: 用户个人的收藏管理功能，可以收藏智能体、知识库和相应的文档。
- **dataflow (数据流/流水线)**: 提供可视化的数据处理 Pipeline 任务管理（包含 Package 管理、流水线构建和执行结果查询）。
- **task (任务系统)**: 专门管理的后台长期运行任务状态或异步 Pipeline 执行状态。

---

## 3. 核心 API 概览 (Core API Overview)

平台的 API 路径主要分为 `/api/v1/`（基于 Django 构建） 和 `/api/v2/`（正在逐步向 FastAPI 迁移）。以下为核心 API 清单及说明：

### 3.1 用户认证 (User & Auth) - `/api/v1/`
- **登录鉴权**: `POST /api/v1/login` (邮箱), `POST /api/v1/login/phone` (手机)
- **第三方登录**: `GET /api/v1/wechat/qr/generate`, `GET /api/v1/github/auth/generate`
- **验证码机制**: `POST /api/v1/email/code`, `POST /api/v1/sms/code`
- **用户信息**: `GET /api/v1/users/info` (获取当前用户), `PUT /api/v1/users/sync`

### 3.2 智能体与工具 (Agent & Tools) - `/api/v1/` 和 `/api/v2/`
- **Agent CRUD**: `GET|POST /api/v1/agents`, `PUT|DELETE /api/v1/agents/<id>`
- **Agent 工具配置**: `POST /api/v1/agents/tools` (配置基于 OpenAPI JSON 的工具解析)
- **行为订阅/分享**: `POST /api/v1/agents/<id>/subscribe/<action>`

### 3.3 对话会话 (Chat) - `/api/v1/`
- **发起流式聊天**: `POST /api/v1/chat` (返回 `text/event-stream`)
- **会话管理**: `GET|POST /api/v1/chat/conversations` (历史记录获取和创建)
- **会话分享**: `POST /api/v1/chat/share` 

### 3.4 知识库与文档管理 - `/api/v1/`
- **知识库 CRUD**: `GET|POST /api/v1/knowledge-base`, `PUT|DELETE /api/v1/knowledge-base/<id>`
- **文档文件处理**: `GET|POST /api/v1/knowledge-base/<kb_id>/files`
- **全局文档检索**: `POST /api/v1/knowledge-base/search`, `POST /api/v1/documents/search`
- **文本片段 (Chunks) 管理**: `GET /api/v1/chunks`, `POST /api/v1/chunks/search` 

### 3.5 数据集与数据流 (Dataset & DataFlow) - `/api/v2/`
- **数据集管理**: `GET|POST|PUT|DELETE /api/v2/dataset/` 
- **文件与对象存储**: `/api/v2/files/`, `/api/v2/object_storage/`
- **DataFlow Packages**: `GET /api/v2/dataflow/packages`

---

## 4. 前端对接指南 (Frontend Integration Guide)

为了让前端（Vue 3 + Vite）能顺利集成和请求这些接口，前端实现了一套自动切换数据源的架构：

### 4.1 数据模式 (Data Mode)
前端可以通过 `.env` 环境变量 `VITE_DATA_MODE` 进行控制：
- `mock`：前端使用本地 JS `data/` 目录下的 mock 模拟数据（开发初期使用）。
- `api`：真实发起 HTTP 请求到后端 API 服务。

需要配置 API 基础地址：
`VITE_API_BASE_URL=http://localhost:8000`

### 4.2 认证机制
目前的 API 在生产环境中应受到严格的 JWT 保护（基于 `Authorization: Bearer <token>` Header）。
FastAPI 部分可以完美复用 Django 生成的 JWT：在 FastAPI 中同样解析同样的 `SECRET_KEY` 并从 Django ORM 中提取 User 对象实例，以实现认证信息的完全互通。

### 4.3 跨域配置 (CORS)
为保证前端（通常运行在 `http://localhost:5173`）可以顺利请求后端。后端的 `core/settings.py` 必须正确设定 CORS 规则：
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
```

---

## 5. OpenAPI 文档自动生成

如果后端正常运行，可以访问以下地址获取全量基于 Swagger/ReDoc 的自动生成接口调试文档：
- **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **ReDoc**: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- **Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
