# DCAI 平台系统整体架构与模块接口设计文档

## 1. 架构愿景与系统概述

DCAI (Data-Centric AI) 平台是一个兼具模型浏览、数据集托管、智能体应用（Agent）及知识库检索分析的综合性 AI 社区平台。系统旨在解决超大规模多模态数据集的管理、复杂工作流的处理编排以及高并发场景下的 AI 对话与大模型服务能力。

为达到这一目标，平台采用了现代化的微服务与混合架构设计，结合了稳定强大的 Web 框架与云原生大数据与 AI 处理组件，核心底座包括 **Django + FastAPI** 混合后端、用于数据处理与算子分发的 **DataFlow-System（DataFlow + Ray + Prefect）**，以及保障海量多模态数据版本存储与极速检索的 **MyScale + LakeFS** 组合。

---

## 2. 系统整体架构

整个 DCAI 系统自上而下可以划分为以下几个主要层级结构：

```text
┌────────────────────────────────────────────────────────────────────────────┐
│                         User Interface (Frontend)                          │
│     Vue 3 + Vite | Tailwind CSS | Vue Router | Vue I18n                    │
│     [Models]  [Datasets]  [Apps/Agent]  [DataFlow UI]  [Knowledge Base]    │
└──────────────────────────────────────┬─────────────────────────────────────┘
                                       │ HTTP / SSE / WebSocket
                                       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                             Backend API Layer                              │
│                                                                            │
│  ┌──────────────────────────┐                 ┌─────────────────────────┐  │
│  │ Django (v1 APIs)         │                 │ FastAPI (v2 APIs)       │  │
│  │ - Auth / User Mgmt       │◀ ─ ─ ─ ─ ─ ─ ─ ▶│ - High Throughput API   │  │
│  │ - Admin & Business       │   Auth Sync     │ - Agent SSE Chat        │  │
│  │ - Knowledge Base & Doc   │                 │ - Async / DataFlow      │  │
│  └──────────────────────────┘                 └─────────────────────────┘  │
└─────────┬────────────────────────────┬────────────────────────────┬────────┘
          │                            │                            │
          ▼                            ▼                            ▼ 
┌──────────────────┐  ┌────────────────────────────────┐  ┌──────────────────┐
│ Relational & MQ  │  │     Search & Vector Engine     │  │ Data Processing  │
│                  │  │                                │  │                  │
│ - PostgreSQL     │  │ - MyScale (Vector / OLAP)      │  │ - Prefect (DAG)  │
│ - Redis (Cache)  │  │ - SQLite (Local Dev)           │  │ - Ray Cluster    │
│ - Celery         │  │                                │  │ - Operators      │
└─────────┬────────┘  └────────────────┬───────────────┘  └─────────┬────────┘
          │                            │                            │ (ETL)
          ▼                            ▼                            ▼ 
┌────────────────────────────────────────────────────────────────────────────┐
│                         Storage Layer (Data Lake)                          │
│  ┌────────────────────────────────────────────────────────(S3/OSS/MinIO)┐  │
│  │ LakeFS (Data-as-Code): Commits, Branches, Zero-copy snapshots        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 核心子系统与功能模块划分

### 3.1 前端应用模块 (Frontend)
前端基于 `Vue 3 + Vite` 构建，通过 `Vue Router` 划分为多个核心功能视图：`apps/` (智能体应用), `datasets/` (数据集), `dataflow/`, `knowledgeBase/` (知识库), 与 `models/` (模型)。
支持多语言切换 (`Vue I18n`)，并通过环境变量（如 `VITE_DATA_MODE`）动态切换 Mock 数据或请求真实的后端 API。

### 3.2 混合后端架构模块 (Backend)
通过 Nginx 路由代理或 ASGI 混合挂载等模式将 Django 和 FastAPI 紧密结合：
- **user & organization**: 处理基于手机、邮箱、第三方社交账号（WeChat/GitHub）的用户注册、认证及鉴权体系，利用 JWT 并在双框架间共享认证态。
- **dataset**: 数据集及相关的对象存储配置管理，支持数据集的文件托管。
- **agent**: 管理智能体（Agent）配置，包括预设提示词配置、可用调用的第三方 OpenAPI 工具能力。
- **chat / llm_chat**: 核心对话引擎，支持与系统预设智能体或自定义 Agent 的对话交互，并支持通过流式协议（Server-Sent Events）输出。
- **knowledgebase / document**: 支持知识库内文件的解析、片段（Chunks）切分、及全局的相似度文档检索。

### 3.3 数据版本与高性能检索子系统 (MyScale + LakeFS)
为突破原生 Hugging Face 数据集的 Viewer 性能与版本管理瓶颈，平台深度集成了以下数据层：
- **LakeFS Storage Gateway**: 在底层 S3 对象存储之上实现 Git-like 的数据版本控制（分支、Commit、Rollback）。配合 `lakefs-spec` 实现大文件的直接拦截与挂载。
- **MyScale Query Service**: 用作原 HF Viewer 的升级替换，基于 `VersionedS3MergeTree` 引擎。结合 LakeFS 的零拷贝优势，支持百亿级规模的结构化过滤、时空数据分析、关键字检索、高维向量及跨模态特征对象的快速混合查询（Hybrid Search）。

### 3.4 分布式流水线驱动引擎 (DataFlow-System)
替换传统的简单后台 worker 队列，处理底层复杂的数据清洗、图谱化执行逻辑：
- **分布式计算池 (Ray)**: 承接并并发式扩展各类处理算子（`Operators`）。如文档切分映射、向 AI API 服务请求 Embedding 等重负荷工作以及数据向 S3/Parquet 和 MyScale 数据库格式的最后回写与写入。
- **控制与编排平台 (Prefect)**: 负责用户构建的 DAG 网络图执行顺序调度、拓扑排序、运行容错重试和运行回调。

---

## 4. 各个模块的主要接口设计 (Main Module Interfaces)

系统提供了丰富的接口用于服务间路由与前端渲染，以下按域梳理核心接口：

### 4.1 基础业务与平台 API (面向前端/第三方)
*主要部署在 `/api/v1/` 和 `/api/v2/` 路径下：*

- **用户身份与鉴权 API**:
  - `POST /api/v1/login` (邮箱/账户鉴权请求，返回 JWT Token)
  - `GET /api/v1/github/auth/generate` (第三方 OAuth)
- **知识库与内容管理 API**:
  - `GET|POST /api/v1/knowledge-base` (增删改查及知识库维护)
  - `POST /api/v1/knowledge-base/<kb_id>/files` (上传存储文件，放入解析队列)
  - `POST /api/v1/knowledge-base/search` (根据 Prompt 或内容进行知识库内向量检索)
- **智能体管理与对话流 API**:
  - `GET|POST /api/v1/agents` (Agent 基本资源维护)
  - `POST /api/v1/agents/tools` (配置基于 OpenAPI JSON 的大模型工具解析)
  - `POST /api/v1/chat` (向 Agent 发起带有上下文的对话请求，并返回 `text/event-stream` 流响应)
  - `POST /api/v1/chat/share` (生成聊天对外分享链接)

### 4.2 数据集高性能检索接口 (数据查询 API)
*由网关结合 MyScale Query Service 对外暴露的大尺度数据检索请求：*

- **`/search` 及向量检索接口**: 相比原生文本匹配，具备打分检索能力。
  - 请求入口: `GET /search?dataset=my_dataset&query=ML&where=year>=2020`
  - 内部响应: 结合 LLM 计算文本向量后组装 SQL (`... ORDER BY distance(...) LIMIT ...`) 获取数据特征响应给前端。
- **`/filter` 数据过滤**: 结合 SQL `where` 的查询下发。
- **`/rows` & `/size` 资源池读取**: 读取元数据并下发布局分页 (`LIMIT OFFSET`)。

### 4.3 DataFlow 数据流编排系统接口
*操作底座及声明式 DAG 控制接口，多由 FastAPI 暴露：*

- **REST 编排层接口**:
  - `POST /api/v1/pipelines/create`: 接收外部图状 Pipeline UI 产生的图谱 JSON (Nodes 与 Edges) 请求，启动 Prefect 的引擎创建 `FlowRun` 并落地至 PostgreSQL 执行表。
  - `GET /api/v1/pipelines/{pipeline_id}/status`: 返回状态更新同步至客户端。
  - `GET /api/v2/dataflow/packages` / `/api/v1/operators`: 获取注册的可用算子及算子表单规约。
- **核心算子与调度内部接口 (Python)**:
  - `PipelineDAG`: `__init__(nodes, edges)` 解析拓扑；`get_execution_order() -> List[NodeInfo]` 按拓扑排序返回调度策略。
  - `OperatorABC`: 继承制基类引擎。需实现 `run(storage, input_key, output_key, **kwargs) -> List[str]` 方法，实现对存储读写的屏蔽并产出特定特征的字段在 Ray 内执行。

---

## 5. 核心业务交互流转示意 (System Interaction Workflow)

以 **"大规模多模态数据集入库分析与上线检索"** 场景为例，其系统交互跨度如下：

1. **触发与登记**：用户通过 Vue 前端新建一笔 Dataset 并上传了原始文件至对象存储 LakeFS `main` 主干分支上。系统随后将事件组装发给后端。此动作回调 DataFlow-System （`POST /api/v1/pipelines/create`）。
2. **编排与清洗执行**：DataFlow 系统在背后将预设工作流构建 DAG：
   - Prefect Orchestrator 将算子提交给 Ray Cluster 执行。
   - `ParseDatasetOperator` 将文件解析和规范化（基于 Arrow）； `VectorEmbeddingOperator` 对文本和图像进行统一地高纬度 Embedding 编码，并将 Parquet 固定回写到 LakeFS 执行不可变提交；最后通过 `ImportToMyScaleOperator` 将向量写向 MyScale 以生成倒排及 HNSW 索引。
3. **极速检索与响应**：此时，前端页面调用数据集检索。FastAPI 中间件接受查询后代理请求到底层 MyScale，依据其内部构造完成超十亿级别数据的混合查询并立等返回，而无需等待繁重缓慢的本地全量数据同步。
