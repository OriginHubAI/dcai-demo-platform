# Dataset API 分析文档 / Dataset API Analysis - backend/dataset

**生成日期 / Generated:** 2026-03-16
**模块 / Module:** `backend/dataset`

---

## 目录 / Table of Contents

1. [概述 / Overview](#overview)
2. [架构 / Architecture](#architecture)
3. [API 分类 / API Categories](#api-categories)
4. [Hub APIs (HF兼容) / Hub APIs (HF-Compatible)](#hub-apis-hf-compatible)
5. [Viewer APIs (HF数据集服务器兼容) / Viewer APIs (HF Datasets Server Compatible)](#viewer-apis-hf-datasets-server-compatible)
6. [V2 APIs (模拟数据) / V2 APIs (Mock Data)](#v2-apis-mock-data)
7. [标准数据集 APIs / Standard Dataset APIs](#standard-dataset-apis)
8. [服务层 / Service Layer](#service-layer)
9. [数据模型 / Data Models](#data-models)
10. [URL 路由汇总 / URL Routing Summary](#url-routing-summary)

---

## 概述 / Overview

`backend/dataset` 模块提供了一个全面的数据集管理系统，具有 **Hugging Face Hub 兼容性**。支持：

The `backend/dataset` module provides a comprehensive dataset management system with **Hugging Face Hub compatibility**. It supports:

- **本地数据集注册表** - 扫描和索引平面数据文件（JSONL、JSON、CSV、Parquet）
  - **Local dataset registry** - Scans and indexes flat data files (JSONL, JSON, CSV, Parquet)
- **Hub 兼容 APIs** - 创建、列出、上传、下载数据集
  - **Hub-compatible APIs** - Create, list, upload, download datasets
- **Viewer APIs** - 浏览数据集内容、分片和元数据
  - **Viewer APIs** - Browse dataset contents, splits, and metadata
- **V2 APIs** - 增强的数据集列表，支持过滤和关系查询
  - **V2 APIs** - Enhanced dataset listing with filtering and relationships
- **模拟数据** - 用于开发的自动驾驶数据集样本
  - **Mock data** - Sample autonomous driving datasets for development

### 核心特性 / Key Features

- ✅ HF Hub API 兼容性（列表、元数据、文件解析）
  - HF Hub API compatibility (list, metadata, resolve files)
- ✅ HF Datasets Server Viewer API 兼容性（is-valid、splits、rows、info）
  - HF Datasets Server Viewer API compatibility (is-valid, splits, rows, info)
- ✅ 基于文件的数据集注册表，YAML 持久化
  - File-based dataset registry with YAML persistence
- ✅ 支持 JSONL、JSON、CSV、Parquet 格式
  - Support for JSONL, JSON, CSV, Parquet formats
- ✅ 数据集关系（原始 → 派生数据集）
  - Dataset relationships (original → derived datasets)
- ✅ 语义和空间搜索能力
  - Semantic and spatial search capabilities
- ✅ 只读派生数据集
  - Read-only derived datasets

---

## 架构 / Architecture

**系统架构图 / System Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                     Django REST Framework                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  hf_views.py │    │ urls_v2.py   │    │   urls.py    │
│ (HF Hub/     │    │ (V2 Mock     │    │ (Standard    │
│  Viewer)     │    │  APIs)       │    │  Stubs)      │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   services.py    │
                    │ HFDatasetFile    │
                    │    Registry      │
                    └──────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ YAML Registry│    │  Scan Dir    │    │  Hub Root    │
│ (Index)      │    │ (Auto-scan)  │    │ (Uploads)    │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 组件说明 / Components

| 组件 / Component | 用途 / Purpose | 位置 / Location |
|-----------|---------|----------|
| **hf_views.py** | HF Hub & Viewer API 实现 / HF Hub & Viewer API implementations | 视图层 / View layer |
| **urls_v2.py** | V2 API，包含模拟数据和过滤 / V2 API with mock data & filtering | 视图层 / View layer |
| **urls.py** | 标准数据集 CRUD（存根）/ Standard dataset CRUD (stubs) | 视图层 / View layer |
| **services.py** | 核心数据集注册表服务 / Core dataset registry service | 服务层 / Service layer |
| **hf_urls.py** | HF 兼容 URL 路由 / HF-compatible URL routing | URL 配置 / URL config |

---

## API 分类 / API Categories

数据集模块提供 **4 种不同的 API 类别**：

The dataset module provides **4 distinct API categories**:

| 类别 / Category | 基础路径 / Base Path | 用途 / Purpose | 认证 / Auth |
|----------|-----------|---------|------|
| **Hub APIs** | `/api/datasets` | HF Hub 兼容的数据集管理 / HF Hub-compatible dataset management | AllowAny |
| **Viewer APIs** | `/is-valid`, `/splits`, `/rows`, `/info` | HF 数据集服务器查看器兼容 / HF Datasets Server viewer compatibility | AllowAny |
| **V2 APIs** | `/v2/datasets` | 增强列表，支持过滤和关系 / Enhanced listing with filtering & relationships | AllowAny |
| **Standard APIs** | `/dataset` | 基础 CRUD 操作（存根）/ Basic CRUD operations (stubs) | IsAuthenticated |

---

## Hub APIs (HF兼容) / Hub APIs (HF-Compatible)

**基础路径 / Base Path:** `/api/datasets`
**源文件 / Source:** `hf_views.py`, `hf_urls.py`
**用途 / Purpose:** Hugging Face Hub 兼容的数据集仓库管理 / Hugging Face Hub-compatible dataset repository management

### 1. List Datasets

**Endpoint:** `GET /api/datasets`
**View:** `hf_list_datasets`
**Auth:** AllowAny

**Query Parameters:**
- `search` (string, optional) - Search query for dataset name or pipeline
- `limit` (int, optional, default: 100) - Maximum results to return

**Response:**
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

**Implementation:**
- Scans local dataset registry via `hfds.list()`
- Filters by search term (case-insensitive, matches name or pipeline)
- Returns flat-file datasets indexed by `HFDatasetFileRegistry`

---

### 2. Get Dataset Metadata

**Endpoint:** `GET /api/datasets/{repo_id}`
**View:** `hf_dataset_metadata`
**Auth:** AllowAny

**Path Parameters:**
- `repo_id` (string) - Dataset repository ID (supports namespace/name format)

**Special Routes:**
- `/api/datasets/{repo_id}/tree/{revision}/{path}` - List directory contents
- `/api/datasets/{repo_id}/paths-info/{revision}` - Get file info for multiple paths
- `/api/datasets/{repo_id}/commits/{revision}` - Get commit history
- `/api/datasets/{repo_id}/revision/{revision}` - Get specific revision metadata

**Response:**
```json
{
  "id": "my-dataset",
  "sha": "abc1234567",
  "lastModified": "2026-03-14T00:00:00.000Z",
  "siblings": [{"rfilename": "data.jsonl"}],
  "private": false,
  "config": "default"
}
```

---

### 3. Resolve/Download File

**Endpoint:** `GET /datasets/{repo_id}/resolve/{revision}/{path}`
**View:** `hf_resolve_file`
**Auth:** AllowAny

**Response:** Binary file content with appropriate MIME type

**Implementation:**
- Strips redundant `resolve/{revision}/` prefix if present
- Checks flat-file dataset first, then hub repo directories
- Returns FileResponse with auto-detected content type

---

### 4. Create Repository

**Endpoint:** `POST /api/repos/create`
**View:** `hf_create_repo`
**Auth:** AllowAny

**Request:** `{"name": "my-new-dataset"}`
**Response:** `{"url": "/api/datasets/my-new-dataset"}`
**Status:** 201 Created, 400 Bad Request

---

### 5. Delete Repository

**Endpoint:** `DELETE /api/datasets/{repo_id}`
**View:** `hf_delete_repo`
**Auth:** AllowAny

**Status:** 204 No Content, 404 Not Found

---

### 6. Upload File

**Endpoint:** `POST /api/datasets/{repo_id}/upload/{revision}/{path}`
**View:** `hf_upload_file`
**Auth:** AllowAny

**Request:** Multipart form data with `file` field
**Response:** `{"commit": {"oid": "new-hash"}, "url": "..."}`

**Implementation:**
- Saves to `hub_root/{repo_id}/resolve/{revision}/{path}`
- Re-indexes if file is a data file (.jsonl, .json, .csv, .parquet)

---

## Viewer APIs (HF数据集服务器兼容) / Viewer APIs (HF Datasets Server Compatible)

**Base Paths:** `/is-valid`, `/splits`, `/rows`, `/info`, `/parquet`, `/viewer/*`
**Source:** `hf_views.py`, `hf_urls.py`
**Purpose:** Hugging Face Datasets Server viewer compatibility for browsing dataset contents

**Note:** All viewer endpoints are duplicated under `/viewer/` prefix for embedded DataFlow-WebUI compatibility.

### 1. Check Dataset Validity

**Endpoint:** `GET /is-valid` or `GET /viewer/is-valid`
**View:** `hf_is_valid`
**Auth:** AllowAny

**Query Parameters:**
- `dataset` (string, required) - Dataset ID to check

**Response:**
```json
{
  "preview": true,
  "viewer": true,
  "search": false,
  "filter": false,
  "statistics": false
}
```

**Status:** 200 OK, 404 Not Found

**Implementation:**
- Checks if dataset exists in registry via `hfds.get_metadata(dataset)`
- Returns capability flags (only preview and viewer are supported)

---

### 2. Get Dataset Splits

**Endpoint:** `GET /splits` or `GET /viewer/splits`
**View:** `hf_get_splits`
**Auth:** AllowAny

**Query Parameters:**
- `dataset` (string, required) - Dataset ID

**Response:**
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

**Status:** 200 OK, 400 Bad Request, 404 Not Found

**Implementation:**
- Returns default split configuration
- All datasets have a single "default" split

---

### 3. Get Dataset Info

**Endpoint:** `GET /info` or `GET /viewer/info`
**View:** `hf_dataset_info`
**Auth:** AllowAny

**Query Parameters:**
- `dataset` (string, required) - Dataset ID

**Response:**
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

**Implementation:**
- Infers features from first 5 rows via `hfds.infer_features()`
- Auto-detects data types: bool, int64, float64, string

---

### 4. Get Dataset Rows

**Endpoint:** `GET /rows` or `GET /viewer/rows` or `GET /first-rows` or `GET /viewer/first-rows`
**View:** `hf_get_rows`
**Auth:** AllowAny

**Query Parameters:**
- `dataset` (string, required) - Dataset ID
- `offset` (int, optional, default: 0) - Starting row index
- `length` (int, optional, default: 100) - Number of rows to return

**Response:**
```json
{
  "features": [
    {"feature_idx": 0, "name": "id", "type": {"dtype": "int64", "_type": "Value"}},
    {"feature_idx": 1, "name": "text", "type": {"dtype": "string", "_type": "Value"}}
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

**Implementation:**
- Reads data from file via `hfds.get_rows()`
- Supports JSONL, JSON, CSV, Parquet formats
- Returns paginated results with feature schema

---

### 5. Get Parquet Files

**Endpoint:** `GET /parquet` or `GET /viewer/parquet`
**View:** `hf_parquet_list`
**Auth:** AllowAny

**Response:** `{"error": "Parquet export not supported"}` (404)

**Note:** Parquet export is not currently implemented.

---

## V2 APIs (模拟数据) / V2 APIs (Mock Data)

**Base Path:** `/v2/datasets`
**Source:** `urls_v2.py`
**Purpose:** Enhanced dataset listing with filtering, relationships, and mock autonomous driving datasets

**Note:** These APIs use in-memory mock data (SAMPLE_DATASETS, SAMPLE_TASKS) for development/demo purposes.

### 1. List Datasets V2

**Endpoint:** `GET /v2/datasets`
**View:** `dataset_list_v2`
**Auth:** AllowAny

**Query Parameters:**
- `page` (int, optional, default: 1) - Page number
- `page_size` (int, optional, default: 20) - Items per page
- `domain` (array, optional) - Filter by domain (e.g., "autonomous-driving", "biology")
- `modality` (array, optional) - Filter by modality (e.g., "multimodal", "text")
- `language` (array, optional) - Filter by language (e.g., "en")
- `datasetType` (array, optional) - Filter by type ("original", "derived")
- `semanticQuery` (string, optional) - Semantic search in description and semanticIndex
- `spatialQuery` (string, optional) - Spatial search in metadata.spatial regions/coverage

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": "autodrive-raw-nuscenes",
        "author": "motional-labs",
        "name": "AutoDrive Raw - nuScenes",
        "task": "object-detection",
        "domain": "autonomous-driving",
        "downloads": 2100000,
        "likes": 4200,
        "lastModified": "2025-03-15",
        "rows": 1400000,
        "size": "680GB",
        "modality": "multimodal",
        "language": "en",
        "license": "cc-by-nc-sa-4.0",
        "description": "Original raw autonomous driving dataset...",
        "datasetType": "original",
        "derivedDatasets": ["autodrive-derived-nuscenes-filtered"],
        "metadata": {
          "timeRange": {"start": "2025-01-01", "end": "2025-03-15"},
          "spatial": {"regions": ["boston", "singapore"]},
          "sensors": ["camera", "lidar", "radar"],
          "conditions": ["day", "night", "rain"]
        }
      }
    ],
    "total": 15,
    "page": 1,
    "page_size": 20
  }
}
```

**Implementation:**
- Filters SAMPLE_DATASETS by multiple criteria
- Supports semantic search (matches description and semanticIndex)
- Supports spatial search (matches regions and coverage)
- Returns paginated results

---

### 2. Get Dataset Detail V2

**Endpoint:** `GET /v2/datasets/{dataset_id}`
**View:** `dataset_detail_v2`
**Auth:** AllowAny

**Path Parameters:**
- `dataset_id` (string) - Dataset ID

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "autodrive-raw-nuscenes",
    "name": "AutoDrive Raw - nuScenes",
    "datasetType": "original",
    "derivedDatasetsInfo": [
      {"id": "autodrive-derived-nuscenes-filtered", "name": "AutoDrive Derived - nuScenes Filtered"}
    ],
    "relatedTasks": [
      {
        "id": "task-nuscenes-filter",
        "name": "nuScenes Quality Filtering Pipeline",
        "type": "Data Processing",
        "status": "completed",
        "progress": 100,
        "isInput": true,
        "isOutput": false,
        "startedAt": "2025-03-15T08:00:00Z",
        "endedAt": "2025-03-15T14:30:00Z",
        "duration": "6h 30m"
      }
    ]
  }
}
```

**Implementation:**
- Returns full dataset details
- Enriches with `derivedDatasetsInfo` for original datasets
- Enriches with `parentDatasetInfo` for derived datasets
- Includes `relatedTasks` that use this dataset as input or output

---

### 3. Get Dataset Relationships

**Endpoint:** `GET /v2/datasets/{dataset_id}/relationships`
**View:** `dataset_relationships`
**Auth:** AllowAny

**Path Parameters:**
- `dataset_id` (string) - Dataset ID

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "parent": {
      "id": "autodrive-raw-nuscenes",
      "name": "AutoDrive Raw - nuScenes",
      "datasetType": "original",
      "readonly": false
    },
    "derived": [
      {
        "id": "autodrive-derived-nuscenes-filtered",
        "name": "AutoDrive Derived - nuScenes Filtered",
        "datasetType": "derived",
        "readonly": true,
        "processingPipeline": "nuscenes_quality_filter_pipeline"
      }
    ]
  }
}
```

**Implementation:**
- Returns parent dataset (if this is a derived dataset)
- Returns derived datasets (if this is an original dataset)
- Includes processing pipeline information for derived datasets

---

### Mock Data Overview

**SAMPLE_DATASETS** includes:
- **Science domains:** Math Olympiad, Iron & Steel Papers, Protein Structures, RNA Sequences, Astrophysics Spectra, Materials Genome, Ocean Climate Sensors, Drug Molecules
- **Autonomous Driving (Original):** nuScenes, KITTI-360, Waymo Open
- **Autonomous Driving (Derived):** nuScenes Filtered, nuScenes Labeled, Waymo Motion, Waymo Perception

**SAMPLE_TASKS** includes:
- nuScenes Quality Filtering Pipeline
- nuScenes VLM Labeling Pipeline
- Waymo Motion Forecasting Pipeline
- Waymo Perception Enhancement Pipeline
- KITTI-360 Enhancement Pipeline
- KITTI-360 Semantic Segmentation Pipeline

---

## 标准数据集 APIs / Standard Dataset APIs

**Base Path:** `/dataset`
**Source:** `urls.py`
**Purpose:** Basic CRUD operations for dataset management
**Auth:** IsAuthenticated (requires authentication)

**Note:** These are stub implementations that return empty responses.

### 1. List/Create Datasets

**Endpoint:** `GET /dataset` or `POST /dataset`
**View:** `dataset_list`
**Auth:** IsAuthenticated

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [],
    "total": 0
  }
}
```

**Status:** Stub implementation, returns empty list

---

### 2. Dataset CRUD Operations

**Endpoint:** `GET /dataset/{dataset_id}` or `PUT /dataset/{dataset_id}` or `DELETE /dataset/{dataset_id}`
**View:** `dataset_detail`
**Auth:** IsAuthenticated

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

**Status:** Stub implementation, returns empty object

---

### 3. Third Party Dataset List

**Endpoint:** `GET /third-party/list`
**View:** `third_party_list`
**Auth:** AllowAny

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": []
  }
}
```

**Status:** Stub implementation

---

### 4. Third Party Dataset Detail

**Endpoint:** `GET /third-party/detail/{dataset_name}`
**View:** `third_party_detail`
**Auth:** AllowAny

**Response:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

**Status:** Stub implementation

---

## 服务层 / Service Layer

**Source:** `services.py`
**Class:** `HFDatasetFileRegistry`

### Overview

The `HFDatasetFileRegistry` is the core service that manages dataset indexing, storage, and retrieval. It provides a unified interface for both flat-file datasets and hub repositories.

### Initialization

```python
hfds = HFDatasetFileRegistry(
    registry_path=settings.DATASET_REGISTRY_PATH,
    scan_dir=settings.DATASET_SCAN_DIR,
    hub_root=os.path.join(settings.BASE_DIR, '..', 'data', 'hub_datasets')
)
```

### Key Responsibilities

1. **Flat-file scanning** - Auto-indexes data files from `scan_dir`
2. **YAML registry** - Persists dataset metadata to YAML file
3. **Hub operations** - Manages uploaded repositories in `hub_root`
4. **Data reading** - Reads rows from JSONL, JSON, CSV, Parquet files
5. **Feature inference** - Auto-detects column types from sample data

---

### Core Methods

#### Scanning & Indexing

**`_rescan()`**
- Walks `scan_dir` recursively
- Finds files with extensions: `.jsonl`, `.json`, `.csv`, `.parquet`
- Builds dataset entries with metadata
- Writes to YAML registry

**`_build_entry(file_path: str) -> dict`**
- Creates dataset entry from file path
- Generates stable ID via SHA1 hash (first 10 chars)
- Extracts pipeline name from parent directory
- Counts rows based on file type

**`_count_rows(file_path: str) -> int`**
- Parquet: Uses `pyarrow.parquet.read_metadata()`
- JSONL: Counts non-empty lines
- JSON: Returns array length or 1 for objects
- CSV: Counts lines minus header

#### Dataset Lookup

**`list() -> List[dict]`**
- Returns all datasets from registry

**`get(key: str) -> Optional[dict]`**
- Looks up by: dataset ID, pipeline name, or file stem
- Case-insensitive matching

#### Data Reading

**`get_rows(key: str, offset: int = 0, length: int = 100) -> Dict[str, Any]`**
- Reads paginated rows from dataset
- Supports JSONL, JSON, CSV, Parquet
- Falls back to hub repo if not in flat-file registry

**`infer_features(key: str) -> Dict[str, Any]`**
- Reads first 5 rows
- Infers data types: bool, int64, float64, string
- Returns HF-compatible feature schema

**`get_splits(key: str) -> Optional[Dict[str, Any]]`**
- Returns default split configuration

#### Hub Repository Operations

**`get_metadata(repo_id: str) -> Optional[Dict[str, Any]]`**
- Checks flat-file registry first
- Falls back to hub repo directory
- Returns HF-compatible metadata with siblings list

**`resolve_file(repo_id: str, revision: str, path: str) -> Optional[str]`**
- Strips redundant `resolve/{revision}/` prefix
- Searches multiple candidate paths

**`create_repo(repo_id: str) -> bool`**
- Creates directory under `hub_root/{repo_id}`

**`delete_repo(repo_id: str) -> bool`**
- Removes entire repository directory

**`upload_file(repo_id: str, revision: str, path: str, content: bytes)`**
- Saves file to `hub_root/{repo_id}/resolve/{revision}/{path}`
- Re-indexes if file is a data file

---

### Supported File Formats

| Format | Extension | Read Method | Row Counting |
|--------|-----------|-------------|--------------|
| **JSONL** | `.jsonl` | Line-by-line JSON parsing | Count non-empty lines |
| **JSON** | `.json` | `json.load()` | Array length or 1 |
| **CSV** | `.csv` | `pandas.read_csv()` | DataFrame length |
| **Parquet** | `.parquet` | `pandas.read_parquet()` | PyArrow metadata |

---

## 数据模型 / Data Models

### Dataset Entry (Flat-file Registry)

```python
{
  "id": "abc1234567",           # SHA1 hash of file path (first 10 chars)
  "name": "my-dataset",         # File stem (filename without extension)
  "pipeline": "data-processing", # Parent directory name
  "root": "/path/to/file.jsonl", # Absolute file path
  "type": "jsonl",              # File extension (jsonl, json, csv, parquet)
  "num_samples": 1000,          # Row count
  "file_size": 2048576          # File size in bytes
}
```

### Hub Metadata Response

```python
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

### Viewer Row Response

```python
{
  "row_idx": 0,                 # Row index (offset + i)
  "row": {                      # Actual data
    "id": 1,
    "text": "example"
  },
  "truncated_cells": []         # Empty array (no truncation)
}
```

### V2 Dataset Model (Mock Data)

```python
{
  "id": "autodrive-raw-nuscenes",
  "author": "motional-labs",
  "name": "AutoDrive Raw - nuScenes",
  "task": "object-detection",
  "domain": "autonomous-driving",
  "downloads": 2100000,
  "likes": 4200,
  "lastModified": "2025-03-15",
  "rows": 1400000,
  "size": "680GB",
  "modality": "multimodal",
  "language": "en",
  "license": "cc-by-nc-sa-4.0",
  "description": "...",
  "datasetType": "original",    # or "derived"
  "derivedDatasets": [...],     # For original datasets
  "parentDataset": "...",       # For derived datasets
  "readonly": true,             # For derived datasets
  "processingPipeline": "...",  # For derived datasets
  "metadata": {
    "timeRange": {...},
    "spatial": {...},
    "sensors": [...],
    "conditions": [...],
    "annotations": [...]
  },
  "semanticIndex": {            # For semantic search
    "objects": [...],
    "scenes": [...],
    "actions": [...]
  }
}
```

---

## URL 路由汇总 / URL Routing Summary

### Complete URL Mapping

| Endpoint Pattern | View Function | Source File | Purpose |
|-----------------|---------------|-------------|---------|
| **Hub APIs (hf_urls.py)** |
| `GET /api/datasets` | `hf_list_datasets` | hf_views.py | List all datasets |
| `POST /api/repos/create` | `hf_create_repo` | hf_views.py | Create repository |
| `GET /api/datasets/{repo_id}` | `hf_dataset_metadata` | hf_views.py | Get metadata |
| `DELETE /api/datasets/{repo_id}` | `hf_delete_repo` | hf_views.py | Delete repository |
| `POST /api/datasets/{repo_id}/upload/{revision}/{path}` | `hf_upload_file` | hf_views.py | Upload file |
| `GET /datasets/{repo_id}/resolve/{revision}/{path}` | `hf_resolve_file` | hf_views.py | Download file |
| **Viewer APIs (hf_urls.py)** |
| `GET /is-valid` | `hf_is_valid` | hf_views.py | Check validity |
| `GET /splits` | `hf_get_splits` | hf_views.py | Get splits |
| `GET /rows` | `hf_get_rows` | hf_views.py | Get rows |
| `GET /first-rows` | `hf_get_rows` | hf_views.py | Get first rows |
| `GET /info` | `hf_dataset_info` | hf_views.py | Get dataset info |
| `GET /parquet` | `hf_parquet_list` | hf_views.py | List parquet files |
| `GET /viewer/*` | (same as above) | hf_views.py | Viewer prefix variants |
| **V2 APIs (urls_v2.py)** |
| `GET /v2/datasets` | `dataset_list_v2` | urls_v2.py | List with filtering |
| `GET /v2/datasets/{dataset_id}` | `dataset_detail_v2` | urls_v2.py | Get detail |
| `GET /v2/datasets/{dataset_id}/relationships` | `dataset_relationships` | urls_v2.py | Get relationships |
| **Standard APIs (urls.py)** |
| `GET /dataset` | `dataset_list` | urls.py | List datasets (stub) |
| `POST /dataset` | `dataset_list` | urls.py | Create dataset (stub) |
| `GET /dataset/{dataset_id}` | `dataset_detail` | urls.py | Get detail (stub) |
| `PUT /dataset/{dataset_id}` | `dataset_detail` | urls.py | Update dataset (stub) |
| `DELETE /dataset/{dataset_id}` | `dataset_detail` | urls.py | Delete dataset (stub) |
| `GET /third-party/list` | `third_party_list` | urls.py | List third-party (stub) |
| `GET /third-party/detail/{dataset_name}` | `third_party_detail` | urls.py | Get third-party detail (stub) |

---

## 配置要求 / Configuration Requirements

### Django Settings

```python
# settings.py
DATASET_REGISTRY_PATH = os.path.join(BASE_DIR, '..', 'data', 'dataset_registry.yaml')
DATASET_SCAN_DIR = os.path.join(BASE_DIR, '..', 'data', 'datasets')
```

### Directory Structure

```
project_root/
├── backend/
│   └── dataset/
│       ├── hf_views.py
│       ├── hf_urls.py
│       ├── urls_v2.py
│       ├── urls.py
│       └── services.py
└── data/
    ├── dataset_registry.yaml    # Auto-generated YAML index
    ├── datasets/                # Auto-scanned flat files
    │   └── pipeline-name/
    │       └── data.jsonl
    └── hub_datasets/            # Uploaded repositories
        └── repo-id/
            └── resolve/
                └── main/
                    └── data.jsonl
```

---

## 核心特性总结 / Key Features Summary

### ✅ Implemented

- HF Hub API compatibility (list, metadata, create, delete, upload, resolve)
- HF Datasets Server Viewer API (is-valid, splits, rows, info)
- Flat-file dataset auto-scanning and indexing
- YAML-based registry persistence
- Multi-format support (JSONL, JSON, CSV, Parquet)
- V2 APIs with filtering (domain, modality, semantic, spatial)
- Dataset relationships (original → derived)
- Mock autonomous driving datasets

### ⚠️ Limitations

- Parquet export not implemented
- Standard CRUD APIs are stubs only
- No authentication/authorization enforcement on Hub APIs
- No git integration (mock commit hashes)
- Single "default" split for all datasets
- No search/filter/statistics in viewer APIs

### 🔄 Data Flow

```
Upload → hub_root/{repo_id}/resolve/{revision}/{path}
       → Re-index if data file
       → Update YAML registry

Scan → Walk scan_dir
     → Find data files
     → Build entries
     → Write YAML registry

Query → Check YAML registry
      → Resolve file path
      → Read and parse
      → Return paginated results
```

---

## 使用示例 / Usage Examples

### List Datasets

```bash
curl http://localhost:8000/api/datasets?search=nuscenes&limit=10
```

### Get Dataset Metadata

```bash
curl http://localhost:8000/api/datasets/my-dataset
```

### Download File

```bash
curl http://localhost:8000/datasets/my-dataset/resolve/main/data.jsonl
```

### Create Repository

```bash
curl -X POST http://localhost:8000/api/repos/create \
  -H "Content-Type: application/json" \
  -d '{"name": "my-new-dataset"}'
```

### Upload File

```bash
curl -X POST http://localhost:8000/api/datasets/my-dataset/upload/main/data.jsonl \
  -F "file=@data.jsonl"
```

### Get Dataset Rows (Viewer API)

```bash
curl "http://localhost:8000/rows?dataset=my-dataset&offset=0&length=10"
```

### List V2 with Filtering

```bash
curl "http://localhost:8000/v2/datasets?domain=autonomous-driving&datasetType=derived&semanticQuery=vehicle"
```

---

**End of Analysis**


---

## 中文总结 / Chinese Summary

### 模块概述

`backend/dataset` 模块是一个功能完整的数据集管理系统，提供了与 Hugging Face Hub 和 Datasets Server 的完整兼容性。

### 四大 API 类别

1. **Hub APIs** (`/api/datasets`) - 数据集仓库管理
   - 列出、创建、删除数据集仓库
   - 上传和下载文件
   - 获取数据集元数据

2. **Viewer APIs** (`/is-valid`, `/splits`, `/rows`, `/info`) - 数据集内容浏览
   - 检查数据集有效性
   - 获取数据集分片信息
   - 分页读取数据行
   - 自动推断数据特征

3. **V2 APIs** (`/v2/datasets`) - 增强功能
   - 多维度过滤（领域、模态、语言、类型）
   - 语义搜索和空间搜索
   - 数据集关系查询（原始 → 派生）
   - 包含自动驾驶领域的模拟数据

4. **Standard APIs** (`/dataset`) - 基础 CRUD（存根实现）

### 核心服务：HFDatasetFileRegistry

- **自动扫描**：递归扫描指定目录，索引所有数据文件
- **YAML 注册表**：持久化数据集元数据
- **多格式支持**：JSONL、JSON、CSV、Parquet
- **Hub 仓库管理**：独立的上传文件存储区域
- **智能查找**：支持按 ID、pipeline 名称、文件名查找

### 数据流程

```
上传流程：
文件上传 → 保存到 hub_root → 检测数据文件 → 重新索引 → 更新 YAML

扫描流程：
启动时扫描 → 遍历目录 → 识别数据文件 → 统计行数 → 写入 YAML

查询流程：
API 请求 → 查询 YAML → 解析文件路径 → 读取并解析 → 返回分页结果
```

### 特色功能

- ✅ **完整的 HF 兼容性**：可直接替代 Hugging Face Hub 和 Datasets Server
- ✅ **自动驾驶数据集**：内置 nuScenes、KITTI-360、Waymo Open 等模拟数据
- ✅ **数据集血缘**：追踪原始数据集和派生数据集的关系
- ✅ **语义搜索**：支持在数据集描述和语义索引中搜索
- ✅ **空间搜索**：支持按地理区域过滤数据集

### 使用场景

1. **本地数据集管理**：扫描和索引本地数据文件
2. **HF Hub 替代**：作为私有的 Hugging Face Hub 服务
3. **数据集浏览**：通过 Viewer API 浏览数据集内容
4. **自动驾驶研究**：使用内置的自动驾驶数据集模拟数据
5. **数据血缘追踪**：管理数据处理流水线的输入输出关系

### 技术栈

- **后端框架**：Django + Django REST Framework
- **数据存储**：YAML 文件（元数据）+ 文件系统（数据文件）
- **数据格式**：JSONL、JSON、CSV、Parquet
- **数据处理**：Pandas、PyArrow

---

**文档结束 / End of Document**

