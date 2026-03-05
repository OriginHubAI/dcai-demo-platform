# 基于 MyScale, LakeFS 与 DataFlow-System 支持 HuggingFace Datasets 接口的架构设计

## 1. 架构愿景与概述

Hugging Face (HF) Datasets 及其自带的 Viewer 为 AI 社区提供了强大的数据集托管、版本控制和快照浏览功能。但在面对超大规模数据处理、复杂的 SQL 过滤、特别是基于多模态的向量检索（Vector Search）时存在诸多痛点（例如，默认仅支持基于 DuckDB 在运行时构造全文检索，不支持高维向量与多模态结构的本地查询，Git 管理数十亿行数据的能力受限）。

为解决这些瓶颈，本架构融合了强大的 **版本存储组件 (LakeFS)**、**AI 原生分析和向量数据库 (MyScale)**，以及 **流控与计算引擎 (DataFlow-System)**。其整体设计原则如下：
1. **数据湖版本控制与零拷贝 (LakeFS)**：负责数据集文件的物理存储、类似 Git 的分支 (Branch) 与提交 (Commit) 版本控制，完美兼容 Hugging Face 接口中的 Revision/Branch 概念。
2. **高性能结构化查询与检索 (MyScale)**：替代 HF Viewer 中的搜索和 SQL 过滤能力，为数据集的每一行建立结构化与向量索引，支持类似 `/rows`, `/search`, `/filter` 等接口的毫秒级高并发访问。
3. **分布式任务编排与处理引擎 (DataFlow-System)**：替代 HF 的后台 Worker Service，通过 Prefect 与 Ray 提供的数据流系统，将用户的上传数据转为 Parquet、分析出元数据、执行向量提取 (Embedding) 并最终持久化到 MyScale 和 LakeFS。

---

## 2. 整体系统架构图

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           User Interface & API Layer                        │
│                                                                             │
│  ┌─────────────────────────┐          ┌──────────────────────────────────┐  │
│  │ HF Datasets Client      │          │ Data Viewer API (API Service)    │  │
│  │ load_dataset(...)       │          │ /splits, /first-rows, /info      │  │
│  │ (基于 lakefs-spec 挂载) │          │ /rows, /search, /filter          │  │
│  └───────────┬─────────────┘          └────────────────┬─────────────────┘  │
└──────────────┼─────────────────────────────────────────┼────────────────────┘
               │                                         │
               ▼                                         ▼
┌───────────────────────────────┐       ┌─────────────────────────────────────┐
│    LakeFS Storage Gateway     │       │       MyScale Query Service         │
│  - S3/OSS Proxy 接口支持       │       │  - SQL 过滤 (WHERE age > 30)         │
│  - Git-like Branching/Commits │       │  - 向量/关键字/时空/时序等混合检索    │
│  - API: /datasets/{id}/resolve│       │  - 分页与 Rows (LIMIT .. OFFSET)      │
└──────────────┬────────────────┘       └────────────────┬────────────────────┘
               │                                         ▲
               │                                         │
┌──────────────┴─────────────────────────────────────────┴────────────────────┐
│                       Webhook & Event Router Service                        │
│  (当新建数据集/更新分支时触发 DataFlow-System 执行预热与ETL任务)                 │
└────────────────────────────────────┬────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Data Processing (DataFlow-System)                      │
│                                                                             │
│  ┌───────────────────────┐   ┌───────────────────────────────────────────┐  │
│  │  Prefect Orchestrator │   │                Ray Cluster                │  │
│  │  - Pipeline 编排触发   │   │  ┌──────────────┐     ┌───────────────┐  │  │
│  │  - 状态回调更新         │───▶│  │ Parse & Size │ ──▶ │ To Parquet    │  │  │
│  │  - 任务重试与容错       │   │  └──────────────┘     └───────┬───────┘  │  │
│  └───────────────────────┘   │                                 │         │  │
│                              │  ┌──────────────┐     ┌─────────▼─────┐   │  │
│                              │  │ Insert to    │ ◀── │ Vector/Feature│   │  │
│                              │  │ MyScale      │     │ Embedding     │   │  │
│                              │  └──────────────┘     └───────────────┘   │  │
│                              └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 核心子系统与功能映射

本架构通过引入三大系统，替代并增强原生的 HF 机制：

### 3.1 预处理与版本控制 (LakeFS 替代 HF Git/LFS)

在原生的 HuggingFace 数据集设计中，元数据与数据文件都依靠底层以 Git 仓库和 LFS 方式进行存储和管理。本架构中采用 **LakeFS over S3** 来完成这一层：
- **存储映射**：`hf://datasets/repo@branch/file` 被直接映射到基于 LakeFS 的对象存储 `s3://repo/branch/file`。结合开源的 Python 包 `lakefs-spec`，HF `datasets` 库可以直接零成本接入。
- **并行版本控制**：支持通过 `lakectl` 或 Python Client 控制数据的多次迭代（Data Commit, Branching）。在大模型评测和实验时，保障每一版数据（Parquet 快照）在对象存储上均留有不可变的版本。

### 3.2 高性能数据视图与搜索 (MyScale 替代 HF Viewer API)

HF 原生提供了诸如 `/search` (通过 DuckDB 文本搜索) 与 `/filter` (SQL 验证) 以及简单的 `/rows` 等接口，但在大规模且多模态数据集中往往遇到性能瓶颈。
这一层将通过 MyScale (基于 ClickHouse 打造的云原生向量数据库) 提供底层计算能力，它擅长处理高维向量以及海量结构化数据的混查 (Hybrid Search)：
- **基于 VersionedS3MergeTree 的存算分离与零拷贝索引挂载**：为彻底解决原生 ClickHouse 对本地元数据强依赖的问题，MyScale 将引入自描述的 `VersionedS3MergeTree` 引擎，实现真正的云原生数据集版本管理：
    1. **自描述存储 (Self-Describing Storage)**：在底层数据块(`.bin`)、倒排/特征索引(`.idx`) 写入 S3 时，将表结构 (DDL) 与 Part 映射组合成 Manifest 文件一并存入 S3 该版本目录下。脱离对本地磁盘和 ZooKeeper 的强依赖。
    2. **LakeFS 瞬间零拷贝分支**：利用 LakeFS 进行 S3 对象版本控制，创建分支（如 `v2.0`）仅需毫秒级复制对象指针，实现基线数据（含庞大 HNSW 索引体系）的 100% 零拷贝。垃圾清理全面让渡给 LakeFS 处理，保障不可变语义。
    3. **秒级按需无缝挂载 (Zero-copy Attach)**：API 路由时通过 `ATTACH TABLE ... FROM 's3://lakefs/repo/v2.0/...'`，内核拉取分支内的 Manifest 并重建内存结构，实现十亿级向量索引秒级切库复用，绝对避免了重复索引加载开销。
- **`/info` 与 `/size`**：对应的元数据通过 MyScale 的一张统一的 `dataset_metadata` 表来快速执行拉取。
- **`/filter` 的原生支持**：直接将 API 传入的类 SQL `where` 子句拼装到对应的 ClickHouse 表中查询，并结合向量索引进行极速过滤。
- **`/search` 的向量增强**：相比原生的 BM25 文本匹配，通过模型打分提取后的向量，在 MyScale 中使用 `ORDER BY distance(table.vector, query_vector) LIMIT x`，同时实现文本+向量综合打分。
- **完备的多维度检索支持**：除了高维度向量外，MyScale 原生还支持**关键字检索 (Keyword Search)**、**时空检索 (Spatio-Temporal Search)** 以及**时序查询 (Time-Series Queries)** 等高阶数据检索能力，无缝支持对混合模态、日志、地理类型数据集的精细化探索。

### 3.3 分布式流水线驱动引擎 (DataFlow-System 替代 Hub Worker)

原版的 HF Viewer 会在其后台使用并行的 Worker 以及 Queue 数据库完成格式转换与统计。这里使用更通用、扩展性更强的 **DataFlow-System** 来处理复杂的有向无环图 (DAG)，它的底层基于 Prefect 和 Ray。
其执行工作流如下：
1. **触发与部署**：当用户向 LakeFS `main` 提交了新的一批原始数据 (CSV/JSON/Image) 后，Webhook 向 DataFlow-System 接口发起 `POST /api/v1/pipelines/create`。
2. **工作流执行 (Ray Tasks)**：执行 DAG 的拓扑任务：
   - **ParseDatasetOperator**: 解析文件及 `features`，读取数据的结构信息。
   - **ToParquetOperator**: 如果有必要，进行原数据的归一化处理（基于 Arrow），并导出一份不可变的 Parquet 文件回写到 LakeFS (生成新的 commit)。
   - **VectorEmbeddingOperator**: 对文本字段/图像字段，调用对应的 LLM/CLIP 模型，将数据投射成高维度特征 Embedding。
   - **ImportToMyScaleOperator**: 将算出的 Embedding 连同普通行数据批量写入到 MyScale 集群，建立索引以供即时在线检索。

---

## 4. 系统交互流程范例

### 场景 1: 使用 HF `datasets` 客户端读取数据集
1. 客户端使用 `load_dataset("my_dataset", revision="v1.0")`。
2. 封装层内部将地址转化为 `lakefs://repo-my_dataset/v1.0/`。
3. `lakefs-spec` 与 LakeFS OpenAPI 进行鉴权与拉取，并挂载 S3 文件系统下载实际底层 Parquet 切片 (`shards`) 至本地内存/磁盘完成 Arrow 缓存映射。

### 场景 2: 界面发起带条件的语义检索请求
1. 浏览器发送请求 `GET /search?dataset=my_dataset&query=machine%20learning&where=year>=2020`。
2. Gateway 服务器将 query 转化为 Embedding 向量 (例如调用一次 Embedding API)。
3. Gateway 根据规则生成 MyScale 查询：
   ```sql
   SELECT text, label, year 
   FROM dataset_my_dataset_v1_0 
   WHERE year >= 2020 
   ORDER BY distance(vector, [0.12, 0.44, ...]) ASC 
   LIMIT 100 OFFSET 0;
   ```
4. MyScale 将查询结果瞬时响应给网关，组合成标准的 Json `{"features": [...], "rows": [...], "truncated": false}` 发送回前端。

---

## 5. 方案对比与优势总结

| 维度 | HuggingFace Native Architecture | MyScale + LakeFS + DataFlow | 提升/优势 |
|---|---|---|---|
| **数据源控制** | Hub + Git + LFS 托管 | LakeFS (Data-as-Code) + S3 | 提供 S3 原生可扩展性与更专业的 PB 级别数据流版本树管理，完全兼容 HF 接口规范。 |
| **检索范围** | 前 100 行 / 轻量级文本 DuckDB | 百亿级别结构化过滤 + 向量/关键字/时空/时序混合检索 | 引入 MyScale 提供极强的高维空间索引、结构过滤和时序时空联合检索能力。弥补了 HF 不足的多模态混合检索支持。 |
| **任务执行与编排** | Queue (MongoDB) + Worker 进程组 | Prefect (可视化编排) + Ray (云原生算力池) | DataFlow-System 提供完整的 DAG、重试和可视化的执行控制，支持随时扩展海量算子来定制清洗链条。 |
| **分析统计 (Statistics)** | 轮询后台算好存为固定格式 | 实时 SQL OLAP | MyScale 原生具备极高的 ClickHouse OLAP 聚合分析能力，能够毫秒级实时返回任意维度 Histogram/Statistics 参数。 |
