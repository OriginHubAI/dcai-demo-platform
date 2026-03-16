# /api/hf/ 接口分析 / API HF Analysis

**生成日期 / Generated:** 2026-03-16
**基础路径 / Base Path:** `/api/hf/`
**路由配置 / Routing:** `backend/core/urls.py` → `backend/dataset/hf_urls.py`
**实现文件 / Implementation:** `backend/dataset/hf_views.py`

---

## 概述 / Overview

`/api/hf/` 提供了与 **Hugging Face Hub** 和 **Hugging Face Datasets Server** 完全兼容的 API 接口。

The `/api/hf/` provides fully compatible APIs with **Hugging Face Hub** and **Hugging Face Datasets Server**.

### 两大类 API / Two API Categories

1. **Hub APIs** - 数据集仓库管理（创建、上传、下载、删除）
   - Dataset repository management (create, upload, download, delete)
2. **Viewer APIs** - 数据集内容浏览（查看、分片、行数据）
   - Dataset content browsing (view, splits, rows)

---

## Hub APIs - 数据集仓库管理

### 1. 列出数据集 / List Datasets

**端点 / Endpoint:** `GET /api/hf/api/datasets`
**视图函数 / View:** `hf_list_datasets`
**认证 / Auth:** AllowAny

**查询参数 / Query Parameters:**
- `search` (string, optional) - 搜索关键词（匹配名称或 pipeline）
- `limit` (int, optional, default: 100) - 最大返回数量

**响应示例 / Response:**
```json
[
  {
    "id": "abc1234567",
    "name": "my-dataset",
    "pipeline": "data-processing",
    "author": "local",
    "tags": ["local"],
    "private": false,
    "downloads": 0,
    "likes": 0,
    "num_samples": 1000,
    "file_size": 2048576
  }
]
```

**实现逻辑 / Implementation:**
- 调用 `hfds.list()` 获取所有数据集
- 按 `search` 参数过滤（不区分大小写）
- 返回前 `limit` 条结果

---

### 2. 获取数据集元数据 / Get Dataset Metadata

**端点 / Endpoint:** `GET /api/hf/api/datasets/{repo_id}`
**视图函数 / View:** `hf_dataset_metadata`
**认证 / Auth:** AllowAny
**支持方法 / Methods:** GET, HEAD, POST, DELETE

**特殊路由 / Special Routes:**
- `/api/hf/api/datasets/{repo_id}/tree/{revision}/{path}` - 列出目录内容
- `/api/hf/api/datasets/{repo_id}/paths-info/{revision}` - 获取多个文件信息
- `/api/hf/api/datasets/{repo_id}/commits/{revision}` - 获取提交历史
- `/api/hf/api/datasets/{repo_id}/revision/{revision}` - 获取特定版本元数据

**响应示例 / Response:**
```json
{
  "id": "my-dataset",
  "sha": "abc1234567",
  "lastModified": "2026-03-14T00:00:00.000Z",
  "siblings": [
    {"rfilename": "data.jsonl"}
  ],
  "private": false,
  "config": "default"
}
```

**实现逻辑 / Implementation:**
- 检测特殊路由（tree, paths-info, commits, revision）
- 调用 `hfds.get_metadata(repo_id)` 获取元数据
- HEAD 请求返回 200 状态码
- DELETE 请求委托给 `hf_delete_repo`

**辅助函数 / Helper Functions:**
- `_hf_paths_info()` - 获取多个文件的路径信息
- `_hf_tree()` - 列出目录树
- `_hf_commits()` - 返回模拟的提交历史

---

### 3. 下载文件 / Resolve/Download File

**端点 / Endpoint:** `GET /api/hf/datasets/{repo_id}/resolve/{revision}/{path}`
**视图函数 / View:** `hf_resolve_file`
**认证 / Auth:** AllowAny
**支持方法 / Methods:** GET, HEAD, DELETE

**路径参数 / Path Parameters:**
- `repo_id` - 数据集仓库 ID
- `revision` - Git 版本（如 "main"）
- `path` - 文件路径

**响应 / Response:** 二进制文件内容，自动检测 MIME 类型

**实现逻辑 / Implementation:**
- 调用 `hfds.resolve_file(repo_id, revision, path)` 解析文件路径
- 使用 `FileResponse` 返回文件内容
- 自动检测 Content-Type

---

### 4. 创建仓库 / Create Repository

**端点 / Endpoint:** `POST /api/hf/api/repos/create`
**视图函数 / View:** `hf_create_repo`
**认证 / Auth:** AllowAny

**请求体 / Request Body:**
```json
{
  "name": "my-new-dataset"
}
```

**响应 / Response:**
```json
{
  "url": "/api/datasets/my-new-dataset"
}
```

**状态码 / Status Codes:**
- 201 - 创建成功
- 400 - 缺少仓库名称

**实现逻辑 / Implementation:**
- 从请求体获取 `name` 参数
- 调用 `hfds.create_repo(repo_id)` 创建目录

---

### 5. 删除仓库 / Delete Repository

**端点 / Endpoint:** `DELETE /api/hf/api/datasets/{repo_id}`
**视图函数 / View:** `hf_delete_repo`
**认证 / Auth:** AllowAny
**支持方法 / Methods:** DELETE, GET, HEAD, POST

**状态码 / Status Codes:**
- 204 - 删除成功
- 404 - 仓库不存在

**实现逻辑 / Implementation:**
- DELETE 方法调用 `hfds.delete_repo(repo_id)`
- 其他方法返回元数据（与 `hf_dataset_metadata` 相同）

---

### 6. 上传文件 / Upload File

**端点 / Endpoint:** `POST /api/hf/api/datasets/{repo_id}/upload/{revision}/{path}`
**视图函数 / View:** `hf_upload_file`
**认证 / Auth:** AllowAny

**路径参数 / Path Parameters:**
- `repo_id` - 数据集仓库 ID（支持 namespace/name 格式）
- `revision` - 目标版本（如 "main"）
- `path` - 目标文件路径

**请求 / Request:** Multipart form data，包含 `file` 字段

**响应 / Response:**
```json
{
  "commit": {"oid": "new-hash"},
  "url": "/datasets/{repo_id}/resolve/{revision}/{path}"
}
```

**状态码 / Status Codes:**
- 200 - 上传成功
- 400 - 未上传文件
- 404 - 仓库不存在

**实现逻辑 / Implementation:**
- 检查仓库是否存在
- 从 `request.FILES` 获取上传的文件
- 调用 `hfds.upload_file()` 保存文件
- 如果是数据文件，自动重新索引

---

## Viewer APIs - 数据集内容浏览

### 1. 检查数据集有效性 / Check Dataset Validity

**端点 / Endpoint:** `GET /api/hf/viewer/is-valid`
**视图函数 / View:** `hf_is_valid`
**认证 / Auth:** AllowAny

**查询参数 / Query Parameters:**
- `dataset` (string, required) - 数据集 ID

**响应 / Response:**
```json
{
  "preview": true,
  "viewer": true,
  "search": false,
  "filter": false,
  "statistics": false
}
```

**状态码 / Status Codes:**
- 200 - 数据集有效
- 404 - 数据集不存在

**实现逻辑 / Implementation:**
- 调用 `hfds.get_metadata(dataset)` 检查数据集是否存在
- 返回能力标志（仅支持 preview 和 viewer）

---

### 2. 获取数据集分片 / Get Dataset Splits

**端点 / Endpoint:** `GET /api/hf/viewer/splits`
**视图函数 / View:** `hf_get_splits`
**认证 / Auth:** AllowAny

**查询参数 / Query Parameters:**
- `dataset` (string, required) - 数据集 ID

**响应 / Response:**
```json
{
  "splits": [
    {
      "dataset": "my-dataset",
      "config": "default",
      "split": "default"
    }
  ],
  "pending": [],
  "failed": []
}
```

**状态码 / Status Codes:**
- 200 - 成功
- 400 - 缺少 dataset 参数
- 404 - 数据集不存在

**实现逻辑 / Implementation:**
- 调用 `hfds.get_splits(dataset)` 获取分片信息
- 所有数据集默认只有一个 "default" 分片

---

### 3. 获取数据集信息 / Get Dataset Info

**端点 / Endpoint:** `GET /api/hf/viewer/info`
**视图函数 / View:** `hf_dataset_info`
**认证 / Auth:** AllowAny

**查询参数 / Query Parameters:**
- `dataset` (string, required) - 数据集 ID

**响应 / Response:**
```json
{
  "dataset_info": {
    "description": "Local dataset my-dataset",
    "features": {
      "id": {"dtype": "int64", "_type": "Value"},
      "text": {"dtype": "string", "_type": "Value"}
    },
    "builder_name": "generator",
    "config_name": "default",
    "version": {"version_str": "0.0.0"},
    "splits": {
      "default": {"num_examples": 0}
    }
  }
}
```

**实现逻辑 / Implementation:**
- 调用 `hfds.get_metadata(dataset)` 检查数据集存在
- 调用 `hfds.infer_features(dataset)` 推断数据特征
- 从前 5 行数据自动推断列类型（bool, int64, float64, string）

---

### 4. 获取数据行 / Get Dataset Rows

**端点 / Endpoint:**
- `GET /api/hf/viewer/rows`
- `GET /api/hf/viewer/first-rows`

**视图函数 / View:** `hf_get_rows`
**认证 / Auth:** AllowAny

**查询参数 / Query Parameters:**
- `dataset` (string, required) - 数据集 ID
- `offset` (int, optional, default: 0) - 起始行索引
- `length` (int, optional, default: 100) - 返回行数

**响应 / Response:**
```json
{
  "features": [
    {
      "feature_idx": 0,
      "name": "id",
      "type": {"dtype": "int64", "_type": "Value"}
    },
    {
      "feature_idx": 1,
      "name": "text",
      "type": {"dtype": "string", "_type": "Value"}
    }
  ],
  "rows": [
    {
      "row_idx": 0,
      "row": {"id": 1, "text": "example"},
      "truncated_cells": []
    }
  ],
  "num_rows_total": 1000,
  "num_rows_per_page": 100,
  "partial": false
}
```

**实现逻辑 / Implementation:**
- 调用 `hfds.get_rows(dataset, offset, length)` 读取数据
- 调用 `hfds.infer_features(dataset)` 获取特征定义
- 支持 JSONL、JSON、CSV、Parquet 格式
- 返回分页结果和特征模式

---

### 5. Parquet 导出 / Parquet Export

**端点 / Endpoint:** `GET /api/hf/viewer/parquet`
**视图函数 / View:** `hf_parquet_list`
**认证 / Auth:** AllowAny

**响应 / Response:**
```json
{
  "error": "Parquet export not supported"
}
```

**状态码 / Status Code:** 404

**说明 / Note:** Parquet 导出功能未实现

---

## 完整路由映射 / Complete URL Mapping

### Hub APIs

| 端点 / Endpoint | 方法 / Method | 视图函数 / View | 功能 / Purpose |
|----------------|--------------|----------------|---------------|
| `/api/hf/api/datasets` | GET | `hf_list_datasets` | 列出所有数据集 |
| `/api/hf/api/repos/create` | POST | `hf_create_repo` | 创建新仓库 |
| `/api/hf/api/datasets/{repo_id}` | GET, HEAD, DELETE | `hf_dataset_metadata` / `hf_delete_repo` | 获取元数据/删除仓库 |
| `/api/hf/api/datasets/{repo_id}/tree/{revision}/{path}` | GET | `hf_dataset_metadata` → `_hf_tree` | 列出目录树 |
| `/api/hf/api/datasets/{repo_id}/paths-info/{revision}` | POST | `hf_dataset_metadata` → `_hf_paths_info` | 获取文件信息 |
| `/api/hf/api/datasets/{repo_id}/commits/{revision}` | GET | `hf_dataset_metadata` → `_hf_commits` | 获取提交历史 |
| `/api/hf/api/datasets/{repo_id}/upload/{revision}/{path}` | POST | `hf_upload_file` | 上传文件 |
| `/api/hf/datasets/{repo_id}/resolve/{revision}/{path}` | GET, HEAD | `hf_resolve_file` | 下载文件 |

### Viewer APIs

| 端点 / Endpoint | 方法 / Method | 视图函数 / View | 功能 / Purpose |
|----------------|--------------|----------------|---------------|
| `/api/hf/viewer/is-valid` | GET | `hf_is_valid` | 检查数据集有效性 |
| `/api/hf/viewer/splits` | GET | `hf_get_splits` | 获取数据集分片 |
| `/api/hf/viewer/rows` | GET | `hf_get_rows` | 获取数据行 |
| `/api/hf/viewer/first-rows` | GET | `hf_get_rows` | 获取首批数据行 |
| `/api/hf/viewer/info` | GET | `hf_dataset_info` | 获取数据集信息 |
| `/api/hf/viewer/parquet` | GET | `hf_parquet_list` | Parquet 导出（未实现） |

---

## 实现特点 / Implementation Features

### 1. 完全兼容 HF Hub

- ✅ 支持标准的 HF Hub API 调用
- ✅ 支持 namespace/name 格式的仓库 ID
- ✅ 支持 revision（版本）参数
- ✅ 返回 HF 兼容的 JSON 响应格式

### 2. 完全兼容 HF Datasets Server

- ✅ 支持 Datasets Server Viewer API
- ✅ 自动推断数据特征（dtype）
- ✅ 分页读取数据行
- ✅ 返回 HF 兼容的特征模式

### 3. 多格式支持

支持的数据格式：
- **JSONL** - 逐行 JSON 解析
- **JSON** - 标准 JSON 数组或对象
- **CSV** - 使用 Pandas 读取
- **Parquet** - 使用 PyArrow/Pandas 读取

### 4. 智能文件解析

- **自动检测 MIME 类型** - 下载文件时自动设置 Content-Type
- **自动推断数据类型** - 从样本数据推断列类型
- **自动重新索引** - 上传数据文件后自动更新注册表

### 5. 灵活的路由匹配

- **支持嵌套路径** - 如 `/tree/`, `/paths-info/`, `/commits/`
- **支持 namespace** - 如 `org/dataset-name`
- **支持通配符** - 使用正则表达式匹配复杂路径

### 6. 无认证限制

- 所有接口使用 `AllowAny` 权限
- 适合内部网络或开发环境
- 生产环境建议添加认证

---

## 依赖服务 / Dependencies

所有接口都依赖 `HFDatasetFileRegistry` 服务（`hfds`）：

```python
from .services import hfds
```

### 核心方法调用 / Core Method Calls

| 视图函数 | 调用的服务方法 |
|---------|--------------|
| `hf_list_datasets` | `hfds.list()` |
| `hf_dataset_metadata` | `hfds.get_metadata()`, `hfds.get_dataset_dir()` |
| `hf_resolve_file` | `hfds.resolve_file()` |
| `hf_create_repo` | `hfds.create_repo()` |
| `hf_delete_repo` | `hfds.delete_repo()` |
| `hf_upload_file` | `hfds.upload_file()`, `hfds.get_dataset_dir()` |
| `hf_is_valid` | `hfds.get_metadata()` |
| `hf_get_splits` | `hfds.get_splits()` |
| `hf_dataset_info` | `hfds.get_metadata()`, `hfds.infer_features()`, `hfds.get_splits()` |
| `hf_get_rows` | `hfds.get_rows()`, `hfds.infer_features()` |

---

## 使用示例 / Usage Examples

### Hub APIs 示例

```bash
# 列出数据集
curl http://localhost:8000/api/hf/api/datasets?search=test&limit=10

# 创建仓库
curl -X POST http://localhost:8000/api/hf/api/repos/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my-dataset"}'

# 获取元数据
curl http://localhost:8000/api/hf/api/datasets/my-dataset

# 上传文件
curl -X POST http://localhost:8000/api/hf/api/datasets/my-dataset/upload/main/data.jsonl \
  -F "file=@data.jsonl"

# 下载文件
curl http://localhost:8000/api/hf/datasets/my-dataset/resolve/main/data.jsonl

# 删除仓库
curl -X DELETE http://localhost:8000/api/hf/api/datasets/my-dataset
```

### Viewer APIs 示例

```bash
# 检查有效性
curl "http://localhost:8000/api/hf/viewer/is-valid?dataset=my-dataset"

# 获取分片
curl "http://localhost:8000/api/hf/viewer/splits?dataset=my-dataset"

# 获取数据集信息
curl "http://localhost:8000/api/hf/viewer/info?dataset=my-dataset"

# 获取数据行
curl "http://localhost:8000/api/hf/viewer/rows?dataset=my-dataset&offset=0&length=10"
```

---

## 中文总结 / Chinese Summary

### 接口概览

`/api/hf/` 提供了 **11 个核心接口**，分为两大类：

1. **Hub APIs (6个)** - 数据集仓库管理
   - 列出数据集
   - 创建/删除仓库
   - 上传/下载文件
   - 获取元数据（支持 tree、paths-info、commits 等子路径）

2. **Viewer APIs (5个)** - 数据集内容浏览
   - 检查有效性
   - 获取分片信息
   - 获取数据集信息
   - 分页读取数据行
   - Parquet 导出（未实现）

### 核心特性

✅ **完全兼容 Hugging Face**
- 可作为私有 HF Hub 服务器使用
- 支持 HF Datasets Server Viewer API
- 返回标准的 HF 格式响应

✅ **多格式支持**
- JSONL、JSON、CSV、Parquet
- 自动推断数据类型
- 智能 MIME 类型检测

✅ **灵活的路由**
- 支持 namespace/name 格式
- 支持嵌套路径（tree、paths-info、commits）
- 正则表达式匹配复杂路径

✅ **自动化处理**
- 上传数据文件后自动重新索引
- 从样本数据自动推断特征
- 自动检测和设置 Content-Type

### 实现架构

```
请求 → Django URL 路由 → 视图函数 → HFDatasetFileRegistry 服务 → 文件系统/YAML
```

所有接口都通过 `hfds` 服务实例访问底层的数据集注册表和文件系统。

### 使用场景

1. **本地 HF Hub** - 作为私有的 Hugging Face Hub 服务器
2. **数据集浏览** - 通过 Viewer API 浏览本地数据集
3. **数据集管理** - 上传、下载、删除数据集文件
4. **HF 客户端兼容** - 可直接使用 HF 官方客户端库访问

### 注意事项

⚠️ **无认证限制** - 所有接口使用 `AllowAny` 权限，生产环境需添加认证
⚠️ **模拟提交历史** - Git 提交历史为模拟数据
⚠️ **单一分片** - 所有数据集默认只有一个 "default" 分片
⚠️ **Parquet 导出未实现** - `/parquet` 端点返回 404

---

**文档结束 / End of Document**

