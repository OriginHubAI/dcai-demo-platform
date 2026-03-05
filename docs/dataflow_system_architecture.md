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
