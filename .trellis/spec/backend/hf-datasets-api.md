# Hugging Face Datasets 核心接口与使用文档

本指南详细介绍了 Hugging Face Datasets (`hf-datasets`) 的核心 API、数据流及内部实现原理。主要为 Backend 开发提供对 Hugging Face Hub 数据集进行下载、处理、上传和 Server 端交互的规范指导。

## 1. 核心加载接口

### 1.1 `load_dataset()`
主入口函数，用于从本地或远程 (Hub) 加载数据集。

```python
from datasets import load_dataset

# 从 Hugging Face Hub 加载
dataset = load_dataset("username/dataset_name", split="train")

# 加载本地文件
dataset = load_dataset("csv", data_files="my_file.csv")
dataset = load_dataset("json", data_files=["file1.json", "file2.json"])
```

- **支持的数据源**：包含 Packaged (csv/json/parquet等)、Local Directory、Hugging Face Hub、Dataset Viewer API。

### 1.2 `load_from_disk()` & `save_to_disk()`
高效的本地磁盘序列化与反序列化（基于 Apache Arrow 格式）。

```python
# 序列化到磁盘
dataset.save_to_disk("path/to/dataset/directory")

# 从磁盘加载
from datasets import load_from_disk
dataset = load_from_disk("path/to/dataset/directory")
```

## 2. 核心数据结构

### 2.1 `Dataset`
核心类，基于 Apache Arrow 后端构建。

- **数据转换操作**：
  - `map(function, batched=False, num_proc=1)`: 对数据集进行元素级或批处理变换。
  - `filter(function, num_proc=1)`: 过滤数据样本。
  - `select(indices)`: 选取特定索引的子集。
  - `sort(column)`: 按照某一列排序。
  - `shuffle(seed=None)`: 随机打乱数据集。
- **格式控制**：
  - `set_format(type="pandas"|"torch"|"pt"|"numpy"等)`: 修改数据集的输出格式而不改变底层 Arrow 存储。
- **导出操作**：
  - `to_csv()`, `to_json()`, `to_parquet()`, `to_pandas()`

### 2.2 `IterableDataset`
支持流式加载，无需将完整数据载入内存或写入磁盘，适用于超大规模数据集。

```python
iterable_dataset = load_dataset("username/large_dataset", streaming=True)
for example in iterable_dataset:
    print(example)
```

### 2.3 `DatasetDict`
一种字典类型的容器，常用于管理多个 Split (例如 `train`, `validation`, `test`)。

## 3. Server 端与 Hub 交互接口

### 3.1 推送数据集到 Hub (`push_to_hub`)
将本地数据集上传至 Hugging Face Hub。底层会自动将数据集拆分为 Parquet Shards (默认 500MB/Shard) 并并行上传，最后调用 `HfApi.create_commit()` 完成提交。

```python
dataset.push_to_hub("username/dataset_name", token="<hf_token>")
```

### 3.2 Hugging Face Hub REST API
Hugging Face datasets 底层通过 `HfApi` 进行网络请求：
- **获取数据集元数据**: `GET /api/datasets/{repo_id}`
- **下载文件**: `GET /datasets/{repo_id}/resolve/{revision}/{path}`
- **提交更改**: `POST /api/datasets/{repo_id}/commit/{revision}`
- **预上传大文件 (LFS)**: `POST /api/datasets/{repo_id}/lfs`

### 3.3 Dataset Viewer API
用于直接查询 Parquet 导出和特征信息（常用于预览和轻量级获取）：
- **获取 Parquet 文件列表**: `GET https://datasets-server.huggingface.co/parquet?dataset={repo_id}`
- **获取特征信息**: `GET https://datasets-server.huggingface.co/info?dataset={repo_id}`

## 4. 扩展与高级特性

### 4.1 数据集构建器 (DatasetBuilder)
自定义数据集的处理逻辑。

```python
class MyDatasetBuilder(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(features=...)

    def _split_generators(self, dl_manager):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={...})]

    def _generate_examples(self, ...):
        yield id, example
```

### 4.2 特征定义 (Features)
支持丰富的数据类型，包括基本类型 `Value`、枚举 `ClassLabel`、序列 `Sequence` 和多媒体 `Image`, `Audio`, `Video` 等。

## 5. 配置与性能优化机制
- **环境变量控制**:
  - `HF_ENDPOINT`: 指定请求域名，默认为 `https://huggingface.co`。
  - `HF_DATASETS_CACHE`: 自定义下载/处理缓存路径。
- **并行与缓存**:
  - 使用 `num_proc` 参数利用多进程加速 `map`/`filter`。
  - 强大的指纹 (Fingerprint) 缓存机制避免重复处理数据。

## 6. Mock Datasets Server 接口规范

为了在内部系统（如 DataFlow）中 Mock Hugging Face 数据集交互，必须实现以下核心 API，以便欺骗 `datasets` 库或类似组件的请求。

### 6.1 Hub 基础信息查询

`datasets` 加载数据时通常会首先向 Hub 确认数据集的 commit revision 和基本配置信息。
需要 Mock 以下基于 `huggingface_hub` 的核心端点：

- **获取数据集元数据** (`GET /api/datasets/{repo_id}`)
  - **响应要求**: 返回一个 JSON 包含 `id`, `sha` (commit hash) 等。

- **下载文件解析** (`GET /datasets/{repo_id}/resolve/{revision}/{path}`)
  - **功能**: 根据实际文件返回 302 重定向到真实的 S3 / LakeFS 地址或直接返回文件流。

### 6.2 Dataset Viewer APIs (Parquet & Info)

对于使用 Parquet 或者查询预处理 Dataset Viewer 结构的情况（在 `_dataset_viewer.py` 中被调用），`datasets` 期望查询 `datasets-server` 子域名对应的接口。
**注意：** 如果配置了自定义的 `HF_ENDPOINT`（例如 `http://localhost:8000`），`datasets` 会将其替换为 `http://datasets-server.localhost:8000`。Mock 时需支持这种域名解析或保证请求被正确路由。

#### a. 获取 Parquet 导出列表 (`GET /parquet?dataset={dataset_name}`)

- **Headers**:
  - **期望返回**: `X-Revision: <commit_hash>` （`datasets` 会以此校验数据版本）
- **Response JSON**:
  ```json
  {
    "partial": false,
    "pending": false,
    "failed": false,
    "parquet_files": [
      {
        "dataset": "dataset_name",
        "config": "default",
        "split": "train",
        "url": "http://your-storage-url.com/path/to.parquet",
        "filename": "train-0000.parquet",
        "size": 123456
      }
    ]
  }
  ```

#### b. 获取数据集 Info 信息 (`GET /info?dataset={dataset_name}`)

- **Headers**:
  - **期望返回**: `X-Revision: <commit_hash>`
- **Response JSON**:
  ```json
  {
    "partial": false,
    "pending": false,
    "failed": false,
    "dataset_info": {
      "default": {
        "description": "Dataset description",
        "features": {
          "text": {"dtype": "string", "_type": "Value"},
          "label": {"names": ["neg", "pos"], "_type": "ClassLabel"}
        }
      }
    }
  }
  ```
