# DataFlow API 文档 / DataFlow API Documentation

> **版本 / Version**: v2
> **基础路径 / Base Path**: `/api/v2/dataflow/`

本文档描述了 DataFlow 相关的所有 API 接口（不包括 datasets）。

This document describes all DataFlow-related API endpoints (excluding datasets).

---

## 目录 / Table of Contents

1. [Packages API](#packages-api) - 算子包管理
2. [Operators API](#operators-api) - 算子查询
3. [Tasks API](#tasks-api) - 任务执行与管理
4. [Pipelines API](#pipelines-api) - 流水线管理
5. [Serving API](#serving-api) - 模型服务管理
6. [Preferences API](#preferences-api) - 用户偏好设置
7. [Prompts API](#prompts-api) - 提示词管理
8. [Text2SQL Database API](#text2sql-database-api) - 数据库文件管理
9. [Text2SQL Database Manager API](#text2sql-database-manager-api) - 数据库管理器配置

---

## 响应格式 / Response Format

所有 API 响应遵循统一的信封格式：

All API responses follow a unified envelope format:

```json
{
  "code": 0,
  "msg": "success",
  "data": { /* 实际数据 / actual data */ }
}
```

- `code`: 状态码，0 表示成功 / Status code, 0 means success
- `msg`: 消息描述 / Message description
- `data`: 响应数据 / Response data

---

## Packages API

算子包管理接口，用于浏览、查看和测试 DataFlow 算子包。

Operator package management APIs for browsing, viewing, and testing DataFlow operator packages.

### 1. 列出所有包 / List All Packages

**路径 / Path**: `GET /api/v2/dataflow/packages`

**权限 / Permission**: AllowAny

**功能 / Function**: 返回所有可用的算子包列表

**响应 / Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [{"id": "package_id", "name": "Package Name"}],
    "total": 1
  }
}
```

### 2. 获取包详情 / Get Package Detail

**路径 / Path**: `GET /api/v2/dataflow/packages/{package_id}`

**路径参数 / Path Parameters**: `package_id` (string, required)

**错误响应 / Error Response**: `404` - Package not found

### 3. 获取包文件树 / Get Package Files

**路径 / Path**: `GET /api/v2/dataflow/packages/{package_id}/files`

**功能 / Function**: 获取包的文件树结构

### 4. 获取文件内容 / Get File Content

**路径 / Path**: `GET /api/v2/dataflow/packages/{package_id}/file?path={path}`

**查询参数 / Query Parameters**: `path` (string, required) - 文件相对路径

**错误响应 / Error Response**: `403` - Invalid path, `404` - File not found

### 5. 启动包编辑器 / Start Package Editor

**路径 / Path**: `POST /api/v2/dataflow/packages/{package_id}/editor/start`

**功能 / Function**: 启动 Code Server 实例用于编辑包代码

### 6. 停止包编辑器 / Stop Package Editor

**路径 / Path**: `POST /api/v2/dataflow/packages/{package_id}/editor/stop`

### 7. 运行包测试 / Run Package Test

**路径 / Path**: `POST /api/v2/dataflow/packages/{package_id}/test`

**功能 / Function**: 执行包的测试用例

---

## Operators API

算子查询接口，用于获取可用算子列表及详细信息。

Operator query APIs for retrieving available operators and their details.

### 1. 列出算子（简化版）/ List Operators (Simplified)

**路径 / Path**: `GET /api/v1/operators/`

**功能 / Function**: 返回所有注册算子的简化列表

**查询参数 / Query Parameters**: `lang` (string, optional, default: "zh") - 语言代码

**响应 / Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": [
    {"name": "operator_name", "category": "category", "description": "desc"}
  ]
}
```

### 2. 列出算子详情 / List Operators Details

**路径 / Path**: `GET /api/v1/operators/details`

**功能 / Function**: 返回所有算子的详细信息（包含参数定义）

**查询参数 / Query Parameters**: `lang` (string, optional, default: "zh")

**响应 / Response**: 按类别分组的算子详情，包含参数、输入输出定义等

### 3. 获取单个算子详情 / Get Operator Detail by Name

**路径 / Path**: `GET /api/v1/operators/details/{op_name}`

**路径参数 / Path Parameters**: `op_name` (string, required) - 算子名称

**查询参数 / Query Parameters**: `lang` (string, optional, default: "zh")

**错误响应 / Error Response**: `404` - Operator not found

---

## Tasks API

任务执行与管理接口，用于执行 Pipeline 并查询执行状态。

Task execution and management APIs for running pipelines and querying execution status.

### 1. 列出所有执行记录 / List Executions

**路径 / Path**: `GET /api/v1/tasks/executions`

**功能 / Function**: 返回所有 Pipeline 执行记录

### 2. 查询执行状态 / Get Execution Status

**路径 / Path**: `GET /api/v1/tasks/execution/{task_id}/status`

**路径参数 / Path Parameters**: `task_id` (string, required)

**功能 / Function**: 查询任务执行状态（包含算子粒度状态）

**错误响应 / Error Response**: `404` - Task not found

### 3. 查询执行结果 / Get Task Result

**路径 / Path**: `GET /api/v1/tasks/execution/{task_id}/result`

**路径参数 / Path Parameters**: `task_id` (string, required)

**查询参数 / Query Parameters**:
- `step` (int, optional) - 步骤索引，null 表示最后一个步骤
- `limit` (int, optional, default: 5) - 返回数据条数

### 4. 获取执行日志 / Get Execution Log

**路径 / Path**: `GET /api/v1/tasks/execution/{task_id}/log`

**查询参数 / Query Parameters**: `operator_name` (string, optional) - 指定算子名称

### 5. 下载执行结果 / Download Task Result

**路径 / Path**: `GET /api/v1/tasks/execution/{task_id}/download`

**查询参数 / Query Parameters**: `step` (int, optional) - 步骤索引（从 0 开始）

**功能 / Function**: 下载任务执行结果文件（JSONL 格式）

### 6. 执行 Pipeline / Execute Pipeline

**路径 / Path**: `POST /api/v1/tasks/execute?pipeline_id={pipeline_id}`

**功能 / Function**: 同步执行 Pipeline，等待完成后返回结果

**错误响应 / Error Response**: `404` - Pipeline not found, `500` - Execution failed

### 7. 异步执行 Pipeline / Execute Pipeline Async

**路径 / Path**: `POST /api/v1/tasks/execute-async?pipeline_id={pipeline_id}`

**功能 / Function**: 异步执行 Pipeline（使用 Ray），立即返回 task_id

**响应 / Response**:
```json
{
  "code": 0,
  "msg": "success",
  "data": {"task_id": "task_id", "status": "queued"}
}
```

### 8. 终止执行 / Kill Execution

**路径 / Path**: `POST /api/v1/tasks/execution/{task_id}/kill`

**功能 / Function**: 终止正在执行的 Pipeline 任务

---

## Pipelines API

流水线管理接口，用于创建、查询、更新和删除 Pipeline 配置。

Pipeline management APIs for creating, querying, updating, and deleting pipeline configurations.

### 1. 列出所有 Pipeline / List Pipelines

**路径 / Path**: `GET /api/v1/pipelines/`

**功能 / Function**: 返回所有注册的 Pipeline 列表

### 2. 列出模板 Pipeline / List Template Pipelines

**路径 / Path**: `GET /api/v1/pipelines/templates`

**功能 / Function**: 返回所有预置（template）Pipeline 列表

### 3. 创建 Pipeline / Create Pipeline

**路径 / Path**: `POST /api/v1/pipelines/`

**请求体 / Request Body**: PipelineIn schema（包含 name, description, config）

**错误响应 / Error Response**: `400` - Invalid configuration

### 4. 获取 Pipeline 详情 / Get Pipeline

**路径 / Path**: `GET /api/v1/pipelines/{pipeline_id}`

**错误响应 / Error Response**: `404` - Pipeline not found

### 5. 更新 Pipeline / Update Pipeline

**路径 / Path**: `PUT /api/v1/pipelines/{pipeline_id}`

**请求体 / Request Body**: PipelineUpdateIn schema（部分更新）

### 6. 删除 Pipeline / Delete Pipeline

**路径 / Path**: `DELETE /api/v1/pipelines/{pipeline_id}`

**错误响应 / Error Response**: `404` - Pipeline not found

---

## Serving API

模型服务管理接口，用于配置和测试 LLM 服务实例。

Model serving management APIs for configuring and testing LLM service instances.

**路由映射 / Route Mapping**: `/api/v2/dataflow/serving/*` → `/api/v1/serving/*`

### 1. 列出所有 Serving 实例 / List Serving Instances

**路径 / Path**: `GET /api/v2/dataflow/serving/`

**功能 / Function**: 返回所有已配置的 Serving 实例

### 2. 获取可用 Serving 类 / List Serving Classes

**路径 / Path**: `GET /api/v2/dataflow/serving/classes`

**功能 / Function**: 返回所有可用的 Serving 类及其参数定义

### 3. 获取 Serving 实例详情 / Get Serving Detail

**路径 / Path**: `GET /api/v2/dataflow/serving/{id}`

**错误响应 / Error Response**: `404` - Serving instance not found

### 4. 创建 Serving 实例 / Create Serving Instance

**路径 / Path**: `POST /api/v2/dataflow/serving/`

**请求参数 / Request Parameters**:
- `name` (string, required) - 实例名称
- `cls_name` (string, required) - Serving 类名
- `params` (array, required) - 参数列表

### 5. 更新 Serving 实例 / Update Serving Instance

**路径 / Path**: `PUT /api/v2/dataflow/serving/{id}`

### 6. 删除 Serving 实例 / Delete Serving Instance

**路径 / Path**: `DELETE /api/v2/dataflow/serving/{id}`

### 7. 测试 Serving 实例 / Test Serving Instance

**路径 / Path**: `POST /api/v2/dataflow/serving/{id}/test`

**请求体 / Request Body**: `{"prompt": "test prompt"}`

**功能 / Function**: 测试 Serving 实例的响应

---

## Preferences API

用户偏好设置接口，用于保存和读取全局配置。

User preferences APIs for saving and reading global configurations.

**路由映射 / Route Mapping**: `/api/v2/dataflow/preferences/*` → `/api/v1/preferences/*`

### 1. 获取偏好配置 / Get Preferences

**路径 / Path**: `GET /api/v2/dataflow/preferences/`

**功能 / Function**: 返回当前全局用户偏好配置

### 2. 更新偏好配置 / Set Preferences

**路径 / Path**: `POST /api/v2/dataflow/preferences/`

**请求体 / Request Body**: 任意 JSON 对象（直接覆盖原配置）

**功能 / Function**: 写入偏好配置，直接覆盖原文件

---

## Prompts API

提示词管理接口，用于查询算子对应的 Prompt 模板。

Prompt management APIs for querying operator-related prompt templates.

**路由映射 / Route Mapping**: `/api/v2/dataflow/prompts/*` → `/api/v1/prompts/*`

### 1. 获取算子-Prompt 映射 / Get Operator-Prompt Mapping

**路径 / Path**: `GET /api/v2/dataflow/prompts/operator-mapping`

**功能 / Function**: 查看所有算子及其对应的 Prompt 列表

### 2. 获取所有 Prompt 信息 / Get Prompt Info

**路径 / Path**: `GET /api/v2/dataflow/prompts/prompt-info`

**功能 / Function**: 查看所有 Prompt 的信息（operator, class, category）

### 3. 获取单个 Prompt 信息 / Get Single Prompt Info

**路径 / Path**: `GET /api/v2/dataflow/prompts/prompt-info/{prompt_name}`

**错误响应 / Error Response**: `404` - Prompt not found

### 4. 根据算子获取 Prompts / Get Prompts by Operator

**路径 / Path**: `GET /api/v2/dataflow/prompts/{operator_name}`

**错误响应 / Error Response**: `404` - Operator not found

### 5. 获取 Prompt 源码 / Get Prompt Source

**路径 / Path**: `GET /api/v2/dataflow/prompts/source/{prompt_name}`

**功能 / Function**: 返回 Prompt 类的源码

### Prompts 底层实现 / Implementation Details

#### 核心架构 / Core Architecture

**依赖注入容器 / Dependency Injection Container**:
- 文件：`dataflow-webui/backend/app/core/container.py`
- 全局单例：`container.prompt_registry = PromptRegistry()`
- 作用：控制各 Registry 初始化顺序，避免循环依赖

**PromptRegistry 初始化**:
```python
self._prompt_registry = PROMPT_REGISTRY      # DataFlow 核心 Prompt 注册表
self._operator_registry = OPERATOR_REGISTRY  # DataFlow 核心 Operator 注册表
self._operator_registry._get_all()           # 确保所有算子已加载
```

#### API 路由层 / API Router Layer

**文件**: `dataflow-webui/backend/app/api/v1/endpoints/prompts.py`

所有端点通过 `container.prompt_registry` 调用服务层方法：

```python
router = APIRouter(tags=["prompts"])

@router.get("/operator-mapping")
def get_operator_prompt_mapping():
    return ok(container.prompt_registry.list_operator_prompts())

@router.get("/prompt-info")
def get_prompt_info():
    return ok(container.prompt_registry.list_prompt_info())
```

#### 核心方法实现 / Core Method Implementation

**1. list_operator_prompts() - 算子到 Prompts 映射**

工作流程：
1. 获取所有算子：`operator_map = self._operator_registry.get_obj_map()`
2. 遍历算子，读取 `ALLOWED_PROMPTS` 属性
3. 构造 `{operator_name: [prompt_names]}` 映射

**2. list_prompt_info() - Prompt 详细信息**

工作流程：
1. 构建反向映射：Prompt → 关联的 Operators
2. 获取 Prompt 分类：`self._prompt_registry.get_type_of_objects()`
3. 使用 `inspect` 模块提取：
   - 类路径：`f"{cls.__module__}.{cls.__name__}"`
   - 文档字符串：`inspect.getdoc(cls)`
   - 方法参数：`inspect.signature(method)`

**3. get_prompts(operator_name) - 根据算子获取 Prompts**

工作流程：
1. 从 `operator_registry` 获取算子类
2. 读取 `ALLOWED_PROMPTS` 属性
3. 返回 `{prompt_name: full_class_path}` 映射

**4. get_prompt_source(prompt_name) - 获取源码**

工作流程：
1. 从 `PROMPT_REGISTRY` 获取 Prompt 类
2. 使用 `inspect.getsource(cls)` 获取源码
3. 返回源码字符串

#### 关键技术点 / Key Technical Points

**算子-Prompt 关联机制**:
- DataFlow 约定：算子类定义 `ALLOWED_PROMPTS = [PromptClass1, PromptClass2]`
- 通过 `getattr(op_cls, "ALLOWED_PROMPTS", [])` 读取关联

**反射技术应用**:
- `inspect.getsource()`: 获取类源码
- `inspect.signature()`: 获取方法签名
- `inspect.getdoc()`: 获取文档字符串
- `inspect.Parameter`: 解析参数定义

**参数提取健壮性**:
```python
def _safe_json_val(val):
    if val is inspect.Parameter.empty:
        return None
    if isinstance(val, type) or callable(val):
        return str(val)  # 不可序列化的值转为字符串
    return val
```

#### 完整调用链 / Complete Call Chain

```
客户端 GET /api/v2/dataflow/prompts/operator-mapping
    ↓
ASGI dispatcher (backend/core/asgi.py)
    ↓ 路径重写
/api/v1/prompts/operator-mapping
    ↓
DataFlow-WebUI FastAPI app
    ↓
prompts.router.get_operator_prompt_mapping()
    ↓
container.prompt_registry.list_operator_prompts()
    ↓
遍历 OPERATOR_REGISTRY，读取 ALLOWED_PROMPTS
    ↓
返回 {operator: [prompts]} 映射
```

---

## Text2SQL Database API

数据库文件管理接口，用于上传、查询和删除 SQLite 数据库文件。

Database file management APIs for uploading, querying, and deleting SQLite database files.

**路由映射 / Route Mapping**: `/api/v2/dataflow/text2sql_database/*` → `/api/v1/text2sql_database/*`

### 1. 列出所有数据库 / List Databases

**路径 / Path**: `GET /api/v2/dataflow/text2sql_database/`

**功能 / Function**: 列出所有已上传的 SQLite 数据库

### 2. 获取数据库详情 / Get Database Detail

**路径 / Path**: `GET /api/v2/dataflow/text2sql_database/{db_id}`

**错误响应 / Error Response**: `404` - Database not found

### 3. 上传数据库 / Upload Database

**路径 / Path**: `POST /api/v2/dataflow/text2sql_database/upload`

**请求类型 / Content-Type**: `multipart/form-data`

**表单参数 / Form Parameters**:
- `file` (file, required) - SQLite 数据库文件
- `name` (string, optional) - 数据库名称
- `description` (string, optional) - 描述

**错误响应 / Error Response**: `400` - Invalid file

### 4. 删除数据库 / Delete Database

**路径 / Path**: `DELETE /api/v2/dataflow/text2sql_database/{db_id}`

**功能 / Function**: 删除数据库及其文件

---

## Text2SQL Database Manager API

数据库管理器配置接口，用于创建和管理数据库管理器实例。

Database manager configuration APIs for creating and managing database manager instances.

**路由映射 / Route Mapping**: `/api/v2/dataflow/text2sql_database_manager/*` → `/api/v1/text2sql_database_manager/*`

### 1. 列出所有 Database Manager / List Database Managers

**路径 / Path**: `GET /api/v2/dataflow/text2sql_database_manager/`

**功能 / Function**: 列出所有 DatabaseManager 配置

### 2. 获取可用 Manager 类 / List Manager Classes

**路径 / Path**: `GET /api/v2/dataflow/text2sql_database_manager/classes`

**功能 / Function**: 获取所有可用 DatabaseManager 类定义

### 3. 获取 Manager 详情 / Get Manager Detail

**路径 / Path**: `GET /api/v2/dataflow/text2sql_database_manager/{mgr_id}`

**错误响应 / Error Response**: `404` - Manager not found

### 4. 创建 Database Manager / Create Manager

**路径 / Path**: `POST /api/v2/dataflow/text2sql_database_manager/`

**请求体 / Request Body**:
```json
{
  "name": "manager_name",
  "cls_name": "class_name",
  "db_type": "sqlite",
  "selected_db_ids": ["db_id1", "db_id2"],
  "description": "optional description"
}
```

**错误响应 / Error Response**: `400` - Unknown db_id(s)

### 5. 更新 Database Manager / Update Manager

**路径 / Path**: `PUT /api/v2/dataflow/text2sql_database_manager/{mgr_id}`

### 6. 删除 Database Manager / Delete Manager

**路径 / Path**: `DELETE /api/v2/dataflow/text2sql_database_manager/{mgr_id}`

---

## 附录 / Appendix

### 代理路由说明 / Proxy Route Notes

部分 API 路径通过 Django 代理转发到 DataFlow Backend 服务：

Some API paths are proxied through Django to the DataFlow Backend service:

- `/api/v1/operators/*` (除 `/` `/details` `/details/{name}`)
- `/api/v1/tasks/*`
- `/api/v1/pipelines/*`

代理目标由环境变量 `DATAFLOW_BACKEND_URL` 配置（默认: `http://localhost:8002`）

Proxy target is configured by `DATAFLOW_BACKEND_URL` env var (default: `http://localhost:8002`)

### 认证说明 / Authentication Notes

- Packages API: AllowAny
- 其他 API: 根据具体端点配置，部分需要认证


### Operators 底层实现 / Implementation Details

#### 核心架构 / Core Architecture

**依赖注入容器 / Dependency Injection Container**:
- 文件：`dataflow-webui/backend/app/core/container.py`
- 全局单例：`container.operator_registry = OperatorRegistry()`
- 作用：控制各 Registry 初始化顺序，避免循环依赖

**OperatorRegistry 初始化**:
```python
self._op_registry = OPERATOR_REGISTRY  # DataFlow 核心注册表
self._op_registry._init_loaders()      # 触发算子加载
self.op_obj_map = self._op_registry.get_obj_map()  # 缓存映射
```


#### get_op_list() 工作流程 / get_op_list() Workflow

1. **遍历已加载算子**：`for op_name, op_cls in self.op_obj_map.items()`
2. **获取分类信息**：从 `op_to_type` 获取三级分类（level_1, level_2）
3. **获取多语言描述**：调用 `op_cls.get_desc(lang=lang)`
4. **获取 Prompt 模板**：读取 `op_cls.ALLOWED_PROMPTS` 属性
5. **返回简化列表**：包含 name, type, description, allowed_prompts

#### DataFlow 核心注册表 / DataFlow Core Registry

**来源**：`dataflow.utils.registry.OPERATOR_REGISTRY`

**功能**：
- 自动发现：扫描 `dataflow/operators/` 目录
- 装饰器注册：`@OPERATOR_REGISTRY.register()` 注册算子
- 延迟加载：使用 loader 机制按需加载算子类


#### 缓存机制 / Caching Mechanism

**内存缓存**：
- `op_obj_map`: `{op_name: op_class}` 映射
- `op_to_type`: 算子分类信息

**文件缓存**：
- 文件：`ops.zh.json` / `ops.en.json`
- 生成：`dump_ops_to_json()` 方法
- 用途：`GET /operators/details` 读取详细信息

#### 完整调用链 / Complete Call Chain

```
客户端 GET /api/v1/operators/?lang=zh
    ↓
ASGI dispatcher (backend/core/asgi.py)
    ↓
DataFlow-WebUI FastAPI app
    ↓
operators.router.list_operators(lang="zh")
    ↓
container.operator_registry.get_op_list(lang="zh")
    ↓
遍历 op_obj_map，调用 op_cls.get_desc(lang)
    ↓
返回简化算子列表
```

