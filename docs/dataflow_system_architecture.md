# DataFlow System 架构与模块接口设计文档

本文档详细描述了 DataFlow System（下一代数据流系统）的系统架构、核心工作流程及主要模块接口。本系统基于 FastAPI、Prefect 编排引擎与 Ray 分布式计算框架构建，目的是提供灵活、可扩展且支持 AI 服务集成的数据处理流水线。

---

## 1. 系统架构概览

整个系统分为以下几个主要层级与子系统：

1. **API 层 (FastAPI)**：接收前端/用户的动作请求，如创建工作流（Pipeline）、查询状态、取消工作流、及算子（Operator）列表查询。
2. **编排与管理层 (Prefect)**：负责根据用户请求定义的 DAG（有向无环图），生成并编排运行流程（Flow / Subflow / Task），处理重试和日志记录等调度工作。
3. **计算与执行层 (Ray)**：在工作流中指定的各类具体数据处理任务（Operator），被提交至 Ray 集群中执行，以获得高并发及多节点扩展的能力。
4. **共享运行库与算子生态 (Packages)**：
   - `dataflow-runtime`：为核心服务、Prefect Worker 及 Ray Worker 提供共享的基础运行环境和工具。
   - `dataflow-operators`：提供模块化的核心算子库，内建大模型提取（LLMService）、词嵌入计算（EmbeddingService）与文档解析（MineruParserService），以及通用的存储访问代理。
5. **存储层 (Infrastructure)**：
   - **PostgreSQL**：保存流水线的运行元数据（`PipelineRuntimeCRUD`）、算子注册表（`OperatorsCRUD`）等信息。
   - **外部对象存储 (S3 / MinION 等)**：供各算子读写中间结果和最终数据。

---

## 2. 核心模块与目录结构

代码库主要划分为两个根模块：`app`（API核心服务）和`packages`（算子与运行环境包）。

### 2.1 `app/` 核心服务

- **`app/api/`**：FastAPI的路由模块，暴露出如 `/api/v1/pipelines` (创建/查询管线状态等) 及 `/api/v1/operators` (查询支持的算子)。
- **`app/pipelines/`**：
  - **`dag.py`**：基于 NetworkX 构建 `PipelineDAG` 有向无环图对象，用于解析上下游依赖节点关系、并进行拓扑排序 (`get_execution_order`) 获取算子执行顺序。
  - **`service.py`**：Pipeline的业务层代码。负责将输入的 Pipeline JSON 转换为对应的内部结构，持久化至 PostgreSQL (`PipelineRuntimeCRUD`)，并向 Prefect 发起 `FlowRun` 的注册 (`create_pipeline_flow_run`)。
- **`app/operators/`**：
  - 管理算子列表，它会通过 Ray 集群加载最新可用的算子 (`registry.py`) 并固化到数据库结构中，使得前端可以通过 `service.py` 获取可用算子及算子配置要求。
- **`app/infrastructure/`**：
  - 提供环境基础设施客户端代理：`prefect` (接口包装)，`ray` (集群创建)，`postgresql` (数据库连接与CRUD定义)。

### 2.2 `packages/` 扩展与运行时包

- **`dataflow-operators/`**：
  - 核心算子包，所有的计算任务均需继承 `OperatorABC`，并实现 `run(storage, input_key, output_key, **kwargs)` 接口。
  - `storage_proxy` 支持诸如 S3、Local 等协议的读取和写入(`read`, `write`)。
  - `ai_services.py` 封装了访问外部 AI 大模型API所需的服务层，方便直接在 Operator 内部以 `self.llm_service.generate()` 的形式使用。
- **`dataflow-runtime/`**：
  - 在 API Server、Prefect Workers 还有 Ray Workers 三者间共享。对 `Flow` 和 `Task` 的包装封装在这个包中。

---

## 3. 核心对象与交互流程

### 3.1 创建管线 (Pipeline) 的核心流程

1. **请求到达**：触发 `POST /api/v1/pipelines/create`，参数为包含 Nodes（节点） 和 Edges（边）的 JSON 布局。
2. **构建 DAG**：`pipelines.service.create_pipeline` 通过调用 `PipelineDAG(nodes, edges)` 构建内存 DAG 并检查是否存在环，然后生成基于拓扑顺序的任务列表 (`get_execution_order()`)。
3. **构造任务配置**：生成每个算子的具体上下文 `TaskConfig`（包含上游依赖的输出 `SourcePortInfo`、资源要求 `resource_tags`、运行时配置 `run_config` 等）。
4. **数据库持久化**：使用 PostgreSQL 记录该次执行（即 PipelineRuntime）。
5. **触发执行 (Prefect)**：调用 `infrastructure.prefect.create_pipeline_flow_run` 将配置表发送至 Prefect Server 创建 Flow 执行实例，并把 Prefect 产生的流水 ID 回写数据库。

---

## 4. 关键接口定义文档 (Python)

下面提取了系统中最重要的几个内部类和函数的接口签名，以供接下来的开发或者客户端调用对接参考。

### 4.1 FastAPI 路由接口

**1. 创建流水线**
```python
# HTTP POST /api/v1/pipelines/create
async def create_new_pipeline(request: PipelineRequest) -> DataflowSystemResponse:
    """
    接收用户定义的工作流结构，启动 Prefect 编排环境
    """
```

**2. 获取流水线状态**
```python
# HTTP GET /api/v1/pipelines/{pipeline_id}/status
async def get_pipeline_status(pipeline_id: UUID) -> DataflowSystemResponse:
    """
    返回指定管线对应在 Prefect 的最终状态 (如 Running, Completed, Failed 等)
    """
```

### 4.2 Pipeline 业务组装接口 (`app/pipelines/dag.py`)

**1. PipelineDAG 类**
```python
class PipelineDAG:
    def __init__(self, pipeline_key_in_backend: UUID, nodes: List[Node], edges: List[Edge]):
        # 将前端配置转为内部 NetworkX 的有向多重图存储
        ...

    def get_execution_order(self) -> List[NodeInfo]:
        """
        进行有向无环图验证，返回基于拓扑排序的执行顺序列表
        """
        
    def get_input_keys_source_info(self, node_id: UUID) -> Dict[str, List[SourcePortInfo]]:
        """
        用于寻找给定节点的输入端口映射了哪些上游节点的执行产出物 (task_idx, source_output_key)
        """
```

### 4.3 Runtime 数据流算子接口 (`packages/dataflow-operators`)

所有的定制化算子处理单元都必须继承该接口：

**OperatorABC (基类)*
```python
from dataflow.utils.registry import OPERATOR_REGISTRY

@OPERATOR_REGISTRY.register()
class OperatorABC:
    def __init__(self, **service_deps):
        """
        初始化可能需要的 AI Service 
        (如 required_service: LLMService)
        """
        pass
        
    def run(
        self,
        storage: DataFlowStorage,
        input_key: str = "input",
        output_key: str = "output",
        **kwargs: Any
    ) -> List[str]:
        """
        核心运行逻辑。
        由 Ray Worker 调度至其所在机器中调用。
        
        Args:
            storage:    屏蔽底层的存储操作柄，提供 read(), write() 等操作。
            input_key:  输入数据在 DataFrame 或者字典中的键/列。
            output_key: 输入数据处理后对应的输出在 DataFrame 中的键/列。
            kwargs:     运行时的额外参数配置。
            
        Returns:
            返回处理后产生的相关输出键值列表
        """
        pass
```

---

## 5. REST API 接口文档

DataFlow System 通过 FastAPI 提供 RESTful API 接口，供前端或外部系统调用。所有 API 端点均返回统一的响应格式。

### 5.1 通用响应格式

所有 API 端点返回 `DataflowSystemResponse` 格式：

```python
class DataflowSystemResponse(BaseModel):
    code: int          # 响应码：0=成功, 400=请求错误, 404=未找到, 500=内部错误
    message: str       # 响应消息
    data: Optional[Any] = None  # 响应数据（成功时包含具体数据）
```

**响应码定义：**
- `0` - SUCCESS: 请求成功
- `400` - BAD_REQUEST: 请求参数错误或业务逻辑错误
- `404` - NOT_FOUND: 资源未找到
- `500` - INTERNAL_ERROR: 服务器内部错误

### 5.2 算子管理 API (Operators)

#### 5.2.1 列出所有可用算子

**端点：** `GET /operators`

**描述：** 查询系统中所有已注册的算子及其配置信息。算子在系统启动时从 Ray 集群加载并保存到数据库。

**请求参数：** 无

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "id": "operator_id_1",
      "name": "LLMExtractor",
      "type": "AI_SERVICE",
      "type1": "EXTRACTION",
      "type2": "LLM",
      "description": "使用大语言模型提取结构化信息",
      "parameters": {
        "model": {"type": "string", "required": true},
        "prompt_template": {"type": "string", "required": true},
        "temperature": {"type": "float", "default": 0.7}
      }
    }
  ]
}
```

**错误响应：**
- `500` - 查询算子列表失败

---

### 5.3 流水线管理 API (Pipelines)

#### 5.3.1 创建流水线定义

**端点：** `POST /pipelines/create`

**描述：** 创建一个新的流水线定义，包含节点（算子）和边（数据流连接）的 DAG 结构。流水线定义保存到数据库，但不立即执行。

**请求体：**
```json
{
  "pipeline_key": "uuid",
  "pipeline_config": {
    "name": "数据处理流水线",
    "task_type": "data_processing",
    "nodes": [
      {
        "id": "node_uuid_1",
        "task_idx": 0,
        "operator_name": "DataLoader",
        "operator_type": "INPUT",
        "config": {
          "init": {},
          "run": {
            "input_key": "input",
            "output_key": "loaded_data"
          }
        }
      }
    ],
    "edges": [
      {
        "source": "node_uuid_1",
        "target": "node_uuid_2",
        "source_port": "loaded_data",
        "target_port": "input"
      }
    ]
  }
}
```

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pipeline_key": "uuid"
  }
}
```

**错误响应：**
- `400` - 流水线配置错误（如存在环、节点配置无效等）

#### 5.3.2 创建流水线并运行工作流

**端点：** `POST /pipelines/run`

**描述：** 一次性完成流水线定义创建和工作流执行。这是创建流水线定义和创建工作流的组合操作。

**请求体：**
```json
{
  "pipeline_key": "uuid",
  "pipeline_config": { /* 同 5.3.1 */ },
  "priority": 50,
  "datasets_config": [
    {
      "dataset_id": "dataset_uuid",
      "bucket_name": "my-bucket",
      "storage_options": {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {
          "endpoint_url": "https://s3.example.com",
          "region_name": "us-east-1"
        }
      },
      "s3_files": ["s3://bucket/file1.jsonl"],
      "s3_directory": null
    }
  ],
  "output_storage_config": {
    "bucket_name": "output-bucket",
    "storage_options": { /* 同上 */ },
    "s3_result_directory": "results/2024-01-01"
  }
}
```

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pipeline_key": "uuid",
    "workflow_id": "flow_run_uuid"
  }
}
```

**错误响应：**
- `400` - 流水线配置错误或工作流创建失败

#### 5.3.3 列出流水线的所有工作流

**端点：** `GET /pipelines/{pipeline_key}/workflows`

**描述：** 查询指定流水线的所有工作流执行记录。

**路径参数：**
- `pipeline_key` (UUID) - 流水线唯一标识

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pipeline_key": "uuid",
    "workflow_ids": ["workflow_uuid_1", "workflow_uuid_2"]
  }
}
```

**错误响应：**
- `500` - 查询失败

---

### 5.4 工作流管理 API (Workflows)

#### 5.4.1 创建工作流

**端点：** `POST /workflows/create`

**描述：** 基于已存在的流水线定义创建一个新的工作流执行实例。工作流会提交到 Prefect 集群进行调度执行。

**请求体：**
```json
{
  "pipeline_key": "uuid",
  "priority": 50,
  "datasets_config": [
    {
      "dataset_id": "dataset_uuid",
      "bucket_name": "my-bucket",
      "storage_options": {
        "key": "access_key",
        "secret": "secret_key",
        "client_kwargs": {
          "endpoint_url": "https://s3.example.com",
          "region_name": "us-east-1"
        }
      },
      "s3_files": ["s3://bucket/file1.jsonl", "s3://bucket/file2.jsonl"],
      "s3_directory": ["s3://bucket/data/"]
    }
  ],
  "output_storage_config": {
    "bucket_name": "output-bucket",
    "storage_options": { /* 同上 */ },
    "s3_result_directory": "results/2024-01-01"
  }
}
```

**字段说明：**
- `priority`: 工作流优先级 (0-100)，数值越大优先级越高
- `datasets_config`: 输入数据集配置列表
  - `s3_files`: S3 文件路径列表（优先使用）
  - `s3_directory`: S3 目录路径列表
- `output_storage_config`: 输出存储配置
  - `s3_result_directory`: 结果存储目录前缀

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "pipeline_key": "uuid",
    "workflow_id": "flow_run_uuid"
  }
}
```

**错误响应：**
- `400` - 流水线定义不存在或参数错误

#### 5.4.2 查询工作流状态

**端点：** `GET /workflows/{workflow_id}/status`

**描述：** 查询指定工作流的执行状态。

**路径参数：**
- `workflow_id` (UUID) - 工作流唯一标识（即 Prefect Flow Run ID）

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "workflow_id": "uuid",
    "status": "RUNNING"
  }
}
```

**状态值：**
- `PENDING` - 等待执行
- `RUNNING` - 执行中
- `COMPLETED` - 执行成功
- `FAILED` - 执行失败
- `CANCELLED` - 已取消
- `CRASHED` - 崩溃

**错误响应：**
- `500` - 查询状态失败

#### 5.4.3 列出子工作流

**端点：** `GET /workflows/{workflow_id}/sub-workflows`

**描述：** 列出指定工作流的所有子工作流（Sub-flow）ID。每个算子节点对应一个子工作流。

**路径参数：**
- `workflow_id` (UUID) - 工作流唯一标识

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "workflow_id": "uuid",
    "sub_workflow_id_list": ["sub_flow_uuid_1", "sub_flow_uuid_2"]
  }
}
```

**错误响应：**
- `500` - 查询失败

#### 5.4.4 查询子工作流状态

**端点：** `GET /workflows/{workflow_id}/{sub_workflow_id}/status`

**描述：** 查询指定子工作流的执行状态。

**路径参数：**
- `workflow_id` (UUID) - 工作流唯一标识
- `sub_workflow_id` (UUID) - 子工作流唯一标识

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "workflow_id": "uuid",
    "sub_workflow_id": "sub_uuid",
    "status": "COMPLETED"
  }
}
```

**错误响应：**
- `500` - 查询状态失败

#### 5.4.5 取消工作流

**端点：** `POST /workflows/{workflow_id}/cancel`

**描述：** 取消正在执行或等待执行的工作流。

**路径参数：**
- `workflow_id` (UUID) - 工作流唯一标识

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": null
}
```

**错误响应：**
- `500` - 取消失败

#### 5.4.6 暂停工作流 (未实现)

**端点：** `POST /workflows/{workflow_id}/pause`

**状态：** `NotImplementedError`

**描述：** 暂停正在执行的工作流（功能待实现）。

#### 5.4.7 恢复工作流 (未实现)

**端点：** `POST /workflows/{workflow_id}/resume`

**状态：** `NotImplementedError`

**描述：** 恢复已暂停的工作流（功能待实现）。

#### 5.4.8 更新工作流优先级 (未实现)

**端点：** `PATCH /workflows/{workflow_id}/priority`

**状态：** `NotImplementedError`

**描述：** 动态调整工作流的执行优先级（功能待实现）。

**预期请求体：**
```json
{
  "priority": 80
}
```

#### 5.4.9 获取工作流结果 (未实现)

**端点：** `GET /workflows/{workflow_id}/results`

**状态：** `NotImplementedError`

**描述：** 获取工作流执行完成后的结果文件路径（功能待实现）。

**预期响应格式：**
```json
{
  "s3_files": ["s3://bucket/results/file1.jsonl"],
  "storage_options": {
    "key": "access_key",
    "secret": "secret_key",
    "client_kwargs": {
      "endpoint_url": "https://s3.example.com",
      "region_name": "us-east-1"
    }
  }
}
```

---

### 5.5 Prefect 回调 API (Prefect Callbacks)

#### 5.5.1 接收 Prefect Webhook 通知

**端点：** `POST /prefect/callback`

**描述：** 接收来自 Prefect CustomWebhookNotificationBlock 的 Webhook 通知。Prefect 在工作流、子工作流或算子任务状态变化时会调用此端点。

**请求体：**
```json
{
  "subject": "Workflow State Changed",
  "body": {
    "state": "COMPLETED",
    "flow_run_id": "uuid"
  }
}
```

**支持的回调类型：**

1. **工作流回调 (WorkflowCallbackPayload)**
```json
{
  "subject": "Workflow Callback",
  "body": {
    "state": "RUNNING",
    "flow_run_id": "workflow_uuid"
  }
}
```

2. **子工作流回调 (SubFlowCallbackPayload)**
```json
{
  "subject": "Sub-flow Callback",
  "body": {
    "state": "COMPLETED",
    "sub_flow_run_id": "sub_workflow_uuid"
  }
}
```

3. **算子任务回调 (OperatorTaskCallbackPayload)**
```json
{
  "subject": "Operator Task Callback",
  "body": {
    "state": "FAILED",
    "sub_flow_run_id": "sub_workflow_uuid",
    "operator_task_run_id": "task_uuid",
    "operator_task_name": "LLMExtractor"
  }
}
```

**响应示例：**
```json
{
  "ok": true
}
```

**错误响应：**
- `400` - 无效的 payload 类型

---

### 5.6 核心数据模型

#### 5.6.1 Node (节点)

```python
class Node(BaseModel):
    id: UUID                    # 节点唯一标识
    task_idx: int              # 任务索引（执行顺序）
    operator_name: str         # 算子名称
    operator_type: str         # 算子类型
    config: NodeConfig         # 节点配置
        - init: Dict[str, Any]   # 初始化参数
        - run: Dict[str, Any]    # 运行时参数
```

#### 5.6.2 Edge (边)

```python
class Edge(BaseModel):
    source: UUID               # 源节点 ID
    target: UUID               # 目标节点 ID
    source_port: str          # 源节点输出端口
    target_port: str          # 目标节点输入端口
```

#### 5.6.3 DatasetConfig (数据集配置)

```python
class DatasetConfig(BaseModel):
    dataset_id: UUID                      # 数据集 ID
    bucket_name: str                      # S3 桶名称
    storage_options: S3StorageOptions     # S3 访问配置
    s3_files: Optional[List[str]]         # S3 文件列表（优先）
    s3_directory: Optional[List[str]]     # S3 目录列表
```

#### 5.6.4 OutputStorageConfig (输出存储配置)

```python
class OutputStorageConfig(BaseModel):
    bucket_name: str                      # 输出桶名称
    storage_options: S3StorageOptions     # S3 访问配置
    s3_result_directory: str              # 结果目录前缀
```

**结果路径格式：**
```
s3://{bucket_name}/{s3_result_directory}/{flow_run_id}/{sub_flow_run_id}/{task_idx}/output.jsonl
```

---

### 5.7 API 使用示例

#### 5.7.1 完整工作流示例

**步骤 1: 查询可用算子**
```bash
curl -X GET http://localhost:8000/operators
```

**步骤 2: 创建流水线并运行**
```bash
curl -X POST http://localhost:8000/pipelines/run \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_key": "550e8400-e29b-41d4-a716-446655440000",
    "pipeline_config": {
      "name": "文本处理流水线",
      "task_type": "text_processing",
      "nodes": [
        {
          "id": "node-1",
          "task_idx": 0,
          "operator_name": "TextLoader",
          "operator_type": "INPUT",
          "config": {
            "init": {},
            "run": {"input_key": "text", "output_key": "loaded_text"}
          }
        },
        {
          "id": "node-2",
          "task_idx": 1,
          "operator_name": "LLMExtractor",
          "operator_type": "PROCESSOR",
          "config": {
            "init": {"model": "gpt-4"},
            "run": {"input_key": "loaded_text", "output_key": "extracted_data"}
          }
        }
      ],
      "edges": [
        {
          "source": "node-1",
          "target": "node-2",
          "source_port": "loaded_text",
          "target_port": "loaded_text"
        }
      ]
    },
    "priority": 50,
    "datasets_config": [
      {
        "dataset_id": "dataset-uuid",
        "bucket_name": "input-bucket",
        "storage_options": {
          "key": "your-access-key",
          "secret": "your-secret-key",
          "client_kwargs": {
            "endpoint_url": "https://s3.amazonaws.com",
            "region_name": "us-east-1"
          }
        },
        "s3_files": ["s3://input-bucket/data.jsonl"]
      }
    ],
    "output_storage_config": {
      "bucket_name": "output-bucket",
      "storage_options": {
        "key": "your-access-key",
        "secret": "your-secret-key",
        "client_kwargs": {
          "endpoint_url": "https://s3.amazonaws.com",
          "region_name": "us-east-1"
        }
      },
      "s3_result_directory": "results/2024-03-14"
    }
  }'
```

**步骤 3: 查询工作流状态**
```bash
curl -X GET http://localhost:8000/workflows/{workflow_id}/status
```

**步骤 4: 查询子工作流列表**
```bash
curl -X GET http://localhost:8000/workflows/{workflow_id}/sub-workflows
```

**步骤 5: 取消工作流（如需要）**
```bash
curl -X POST http://localhost:8000/workflows/{workflow_id}/cancel
```

#### 5.7.2 分步创建示例

**先创建流水线定义：**
```bash
curl -X POST http://localhost:8000/pipelines/create \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_key": "pipeline-uuid",
    "pipeline_config": { /* 流水线配置 */ }
  }'
```

**再创建工作流执行：**
```bash
curl -X POST http://localhost:8000/workflows/create \
  -H "Content-Type: application/json" \
  -d '{
    "pipeline_key": "pipeline-uuid",
    "priority": 50,
    "datasets_config": [ /* 数据集配置 */ ],
    "output_storage_config": { /* 输出配置 */ }
  }'
```

---

### 5.8 API 设计要点总结

#### 5.8.1 关键概念

1. **Pipeline (流水线)**: 定义时配置，包含节点和边的 DAG 结构，可复用
2. **Workflow (工作流)**: 运行时实例，基于 Pipeline 定义创建，包含具体的数据集和输出配置
3. **Sub-workflow (子工作流)**: 每个算子节点对应一个子工作流，由 Prefect 调度
4. **Operator (算子)**: 具体的数据处理单元，在 Ray 集群中执行

#### 5.8.2 API 调用流程

```
1. GET /operators
   ↓ (查询可用算子)
2. POST /pipelines/create
   ↓ (创建流水线定义)
3. POST /workflows/create
   ↓ (创建工作流实例)
4. GET /workflows/{id}/status
   ↓ (轮询状态)
5. GET /workflows/{id}/results
   (获取结果)
```

**或使用快捷方式：**
```
1. GET /operators
   ↓
2. POST /pipelines/run
   ↓ (一步完成创建和运行)
3. GET /workflows/{id}/status
```

#### 5.8.3 状态管理

- 工作流状态由 Prefect 管理，通过 API 查询
- 支持通过 Webhook 接收状态变化通知
- 可取消正在执行的工作流
- 暂停/恢复功能待实现

#### 5.8.4 错误处理

- 所有 API 返回统一的 `DataflowSystemResponse` 格式
- `code=0` 表示成功，其他值表示错误
- 错误信息包含在 `message` 字段中
- 建议客户端根据 `code` 进行错误处理

---

## 6. 待完善接口清单

根据 DataFlow-WebUI 的 API 设计（`docs/api-v2-dataflow.md`），DataFlow System 后端需要补充以下接口以支持完整的前端功能。

### 6.1 Operators API 增强

**当前状态：** 已实现基础算子列表查询

**需要补充：**

#### 6.1.1 获取算子详细信息（带参数定义）

**端点：** `GET /api/v1/operators/details`

**功能：** 返回所有算子的详细配置信息，包括参数定义、输入输出端口、类别分组等

**响应格式：**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "category_1": {
      "category_2": [
        {
          "name": "operator_name",
          "description": "算子描述",
          "parameters": {
            "param1": {
              "type": "string",
              "required": true,
              "default": null,
              "description": "参数说明"
            }
          },
          "input_ports": ["input"],
          "output_ports": ["output"]
        }
      ]
    }
  }
}
```

#### 6.1.2 获取单个算子详情

**端点：** `GET /api/v1/operators/details/{op_name}`

**功能：** 返回指定算子的详细配置信息

**路径参数：**
- `op_name` (string) - 算子名称


---

### 6.2 Tasks API（执行管理）

**当前状态：** 使用 Workflows API，但接口设计与前端需求不匹配

**需要重构为 Tasks API：**

#### 6.2.1 列出所有执行记录

**端点：** `GET /api/v1/tasks/executions`

**功能：** 返回所有 Pipeline 执行记录列表

**查询参数：**
- `pipeline_id` (optional) - 过滤特定 Pipeline 的执行记录
- `status` (optional) - 过滤特定状态的执行记录
- `limit` (optional, default: 50) - 返回记录数
- `offset` (optional, default: 0) - 分页偏移

#### 6.2.2 查询执行状态（算子粒度）

**端点：** `GET /api/v1/tasks/execution/{task_id}/status`

**功能：** 返回任务执行状态，包含每个算子的执行状态

**映射关系：**
- `task_id` → Prefect `flow_run_id`
- `operators[].status` → Prefect `sub_flow_run` 状态

#### 6.2.3 查询执行结果

**端点：** `GET /api/v1/tasks/execution/{task_id}/result`

**功能：** 返回任务执行结果的预览数据

**查询参数：**
- `step` (int, optional) - 步骤索引，null 表示最后一个步骤
- `limit` (int, optional, default: 5) - 返回数据条数

**实现要点：**
- 从 S3 读取结果文件（JSONL 格式）
- 返回前 N 条记录作为预览
- 提供完整的 S3 路径供下载


#### 6.2.4 获取执行日志

**端点：** `GET /api/v1/tasks/execution/{task_id}/log`

**功能：** 返回任务执行日志

**查询参数：**
- `operator_name` (string, optional) - 指定算子名称，不指定则返回所有日志

**实现要点：**
- 从 Prefect 获取 Flow Run 和 Sub-flow Run 的日志
- 支持按算子名称过滤
- 按时间顺序排序

#### 6.2.5 下载执行结果

**端点：** `GET /api/v1/tasks/execution/{task_id}/download`

**功能：** 下载任务执行结果文件（JSONL 格式）

**查询参数：**
- `step` (int, optional) - 步骤索引（从 0 开始），不指定则下载最后一步的结果

**响应：**
- Content-Type: `application/x-ndjson`
- Content-Disposition: `attachment; filename="result_{task_id}_{step}.jsonl"`

**实现要点：**
- 从 S3 读取完整结果文件
- 流式传输，避免内存溢出
- 支持大文件下载


#### 6.2.6 执行 Pipeline（同步）

**端点：** `POST /api/v1/tasks/execute?pipeline_id={pipeline_id}`

**功能：** 同步执行 Pipeline，等待完成后返回结果

**实现要点：**
- 创建 Workflow 并等待执行完成
- 超时时间建议 30 分钟
- 适用于小规模、快速执行的 Pipeline

#### 6.2.7 异步执行 Pipeline

**端点：** `POST /api/v1/tasks/execute-async?pipeline_id={pipeline_id}`

**功能：** 异步执行 Pipeline，立即返回 task_id

**实现要点：**
- 创建 Workflow 后立即返回
- 客户端通过 `GET /tasks/execution/{task_id}/status` 轮询状态

#### 6.2.8 终止执行

**端点：** `POST /api/v1/tasks/execution/{task_id}/kill`

**功能：** 终止正在执行的 Pipeline 任务

**实现要点：**
- 调用 Prefect API 取消 Flow Run
- 清理 Ray 集群中的运行任务
- 更新数据库中的任务状态


---

### 6.3 Pipelines API 增强

**当前状态：** 已实现基础的创建和查询

**需要补充：**

#### 6.3.1 列出模板 Pipeline

**端点：** `GET /api/v1/pipelines/templates`

**功能：** 返回所有预置（template）Pipeline 列表

**实现要点：**
- 在数据库中标记模板 Pipeline（`is_template` 字段）
- 用户可以基于模板创建新的 Pipeline

#### 6.3.2 更新 Pipeline

**端点：** `PUT /api/v1/pipelines/{pipeline_id}`

**功能：** 更新已存在的 Pipeline 定义

**实现要点：**
- 验证更新后的 DAG 是否有效
- 不影响已创建的 Workflow 执行

#### 6.3.3 删除 Pipeline

**端点：** `DELETE /api/v1/pipelines/{pipeline_id}`

**功能：** 删除 Pipeline 定义

**实现要点：**
- 检查是否有正在执行的 Workflow
- 可选：软删除（标记为已删除）或硬删除


---

### 6.4 实现优先级建议

根据前端功能需求，建议按以下优先级实现：

**P0（核心功能，必须实现）：**
1. `GET /api/v1/operators/details` - 前端需要算子参数定义来构建配置表单
2. `POST /api/v1/tasks/execute-async` - 异步执行是主要使用场景
3. `GET /api/v1/tasks/execution/{task_id}/status` - 前端需要轮询任务状态
4. `GET /api/v1/tasks/executions` - 前端需要展示执行历史列表

**P1（重要功能，尽快实现）：**

5. `GET /api/v1/tasks/execution/{task_id}/result` - 前端需要预览执行结果
6. `POST /api/v1/tasks/execution/{task_id}/kill` - 用户需要能够取消任务
7. `GET /api/v1/pipelines/templates` - 提供模板可以降低使用门槛
8. `PUT /api/v1/pipelines/{pipeline_id}` - 用户需要能够修改 Pipeline

**P2（增强功能，后续实现）：**

9. `GET /api/v1/tasks/execution/{task_id}/log` - 调试和监控需要
10. `GET /api/v1/tasks/execution/{task_id}/download` - 大规模数据下载
11. `POST /api/v1/tasks/execute` - 同步执行（小规模场景）
12. `DELETE /api/v1/pipelines/{pipeline_id}` - Pipeline 管理


---

### 6.5 接口对齐注意事项

#### 6.5.1 命名约定

- DataFlow-WebUI 使用 `tasks` 表示执行实例
- DataFlow System 使用 `workflows` 表示执行实例
- **建议：** 在 API 层统一使用 `tasks`，内部实现仍使用 Prefect 的 `workflows` 概念

#### 6.5.2 响应格式

- 所有接口返回统一的信封格式：`{code, msg, data}`
- `code=0` 表示成功，其他值表示错误
- 错误信息包含在 `msg` 字段中

#### 6.5.3 状态映射

Prefect 状态 → API 状态：
- `PENDING` → `queued`
- `RUNNING` → `RUNNING`
- `COMPLETED` → `COMPLETED`
- `FAILED` → `FAILED`
- `CANCELLED` → `CANCELLED`
- `CRASHED` → `FAILED`

#### 6.5.4 ID 映射

- `task_id` (API) ↔ `flow_run_id` (Prefect)
- `pipeline_id` (API) ↔ `pipeline_key` (Database)
- `operator_name` (API) ↔ `operator_name` (Registry)


---

### 6.6 技术实现建议

#### 6.6.1 日志聚合

- 使用 Prefect API 获取 Flow Run 日志
- 考虑使用 ELK/Loki 等日志系统进行集中管理
- 支持实时日志流（WebSocket 或 SSE）

#### 6.6.2 结果存储

- 统一使用 S3 存储中间结果和最终结果
- 结果路径格式：`s3://{bucket}/{prefix}/{flow_run_id}/{sub_flow_run_id}/{task_idx}/output.jsonl`
- 支持结果过期自动清理

#### 6.6.3 性能优化

- 执行列表接口支持分页和过滤
- 结果预览接口限制返回数据量
- 下载接口使用流式传输
- 状态查询接口考虑缓存（Redis）

#### 6.6.4 错误处理

- 统一的异常处理和错误码定义
- 详细的错误信息帮助调试
- 区分用户错误（400）和系统错误（500）

---
