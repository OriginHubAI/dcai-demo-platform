# Hugging Face Dataset/Repo REST API 分析

生成时间：2026-03-19

## 范围

本文总结了三个 Hugging Face 组件在数据集与仓库生命周期管理中的协作方式：

- `huggingface_hub`：仓库管理与基于 commit 的写接口
- `datasets`（也就是 `hf-datasets`）：构建在 Hub API 之上的数据集加载与发布流程
- `dataset-viewer` / `datasets-server`：面向数据预览与元信息查询的读优化接口

重点覆盖 **dataset repo** 相关能力：

- 创建
- 列表 / 元数据查询
- 内容查看
- 设置更新
- 上传 / 提交更新

本文适合作为实现 HF 兼容数据集 API、代理层或者本地 mock 服务时的后端参考。

## 观察到的版本

本文使用了两类证据来源：

1. Hugging Face 官方文档，检查时间为 2026-03-19
2. 当前环境中已安装库的本地源码：
   - `huggingface_hub==0.33.0`
   - `datasets==2.21.0`

如果某个 REST 路径是直接从本地库源码中确认的，标记为 **源码确认**。
如果某个行为来自官方文档，但官方文档没有明确展开底层路径，标记为 **文档确认**。

## 高层架构

### 1. 写路径：`datasets` -> `huggingface_hub` -> Hub Repo API

对于数据集创建和更新，`datasets.Dataset.push_to_hub()` 并不会直接调用 viewer 服务。
它的流程大致是：

1. 必要时先创建 dataset repo
2. 将数据写成 Parquet 分片
3. 准备 commit operations
4. 通过 `huggingface_hub.HfApi` 执行上传和 commit

因此，真正的权威写平面是 **Hub repo API**，而不是 dataset viewer API。

### 2. 读路径：`datasets` -> Hub + `datasets-server`

对于数据集加载和查看，`datasets.load_dataset()` 可能会组合使用：

- Hub 仓库元数据与文件解析接口
- dataset viewer 接口，例如 `/parquet` 和 `/info`

在本地源码中，`datasets.utils._dataset_viewer` 明确按下面的方式构造 viewer URL：

- `HF_ENDPOINT` -> `datasets-server.<host>/parquet?dataset=...`
- `HF_ENDPOINT` -> `datasets-server.<host>/info?dataset=...`

这在本地 `datasets==2.21.0` 中是 **源码确认** 的行为。

### 3. Viewer 路径：`dataset-viewer` / `datasets-server`

dataset viewer 服务主要面向：

- split / config 发现
- 首行预览
- 行切片浏览
- Parquet 导出发现
- 轻量元信息与特征查询

它本质上是一个 **读 API**，而不是写 API。

## 按职责划分的 REST API 面

## A. 仓库创建 / 删除 / 重命名 / 设置更新

这部分主要属于 `huggingface_hub` 与 Hub repo API。

### 创建仓库

- Python API：`HfApi.create_repo(..., repo_type="dataset")`
- REST：`POST /api/repos/create`
- 状态：**文档确认** + **源码确认**

典型请求体：

```json
{
  "type": "dataset",
  "name": "my-dataset",
  "organization": "my-org",
  "private": true
}
```

说明：

- dataset 仓库通过 `type: "dataset"` 指定。
- `datasets.Dataset.push_to_hub()` 会先调用 `api.create_repo(..., repo_type="dataset", exist_ok=True)`，然后才上传数据分片。

### 删除仓库

- Python API：`HfApi.delete_repo(..., repo_type="dataset")`
- REST：`DELETE /api/repos/delete`
- 状态：**文档确认** + **源码确认**

典型请求体：

```json
{
  "type": "dataset",
  "name": "my-dataset",
  "organization": "my-org"
}
```

### 更新仓库设置

- Python API：`HfApi.update_repo_settings(..., repo_type="dataset")`
- REST：`PUT /api/datasets/{repo_id}/settings`
- 状态：**源码确认**

当前 Python API 暴露的常见设置包括：

- `private`
- `gated`
- 更新版本客户端中的 `xet_enabled`

典型请求体：

```json
{
  "private": true,
  "gated": "manual"
}
```

### 移动 / 重命名仓库

- Python API：`HfApi.move_repo(from_id, to_id, repo_type="dataset")`
- REST：`POST /api/repos/move`
- 状态：**源码确认**

典型请求体：

```json
{
  "fromRepo": "user/old-name",
  "toRepo": "org/new-name",
  "type": "dataset"
}
```

## B. 仓库列表 / 元数据 / 文件解析

### 列出 dataset 仓库

- Python API：`HfApi.list_datasets(...)`
- REST：`GET /api/datasets`
- 状态：**源码确认**

`huggingface_hub` 组装的常见查询参数包括：

- `filter`
- `author`
- `gated`
- `search`
- `sort`
- `direction`
- `limit`
- `expand`
- `full`

这是 dataset repo 发现的主入口。

### 获取 dataset 仓库元数据

- Python API：`HfApi.dataset_info(repo_id, revision=None, ...)`
- REST：
  - `GET /api/datasets/{repo_id}`
  - `GET /api/datasets/{repo_id}/revision/{revision}`
- 状态：**源码确认**

客户端常用的重要返回字段包括：

- `id`
- `sha`
- `private`
- `siblings`
- `tags`
- `lastModified`
- `cardData`

`datasets` 和 `huggingface_hub` 都会依赖这些元数据做 revision、文件列表和仓库属性判断。

### 解析 / 下载 dataset 仓库中的文件

- 公共文件 URL 模式：
  - `GET /datasets/{repo_id}/resolve/{revision}/{path}`
- 状态：**文档确认**

这个路径很关键，因为数据集加载最终需要稳定的文件 URL 来获取原始文件或 Parquet 文件。

#### 详细定义

- 用途：
  - 下载文件内容
  - 获取文件最终落点
  - 为前端生成可直接访问的文件下载链接
- 路径参数：
  - `repo_id`: `namespace/name`
  - `revision`: 分支、tag、commit SHA
  - `path`: 仓库内相对路径
- 常见行为：
  - 普通小文件可能直接由 Hub 域名返回
  - 大文件和 LFS 文件通常会重定向到 CDN / CloudFront / S3 一类签名 URL

#### 获取 S3 / CDN 签名下载链接

如果前端需要最终的直链地址，而不是 Hub 的逻辑 URL，可以把 `resolve` 当作跳板：

1. 对 `resolve` URL 发起 `HEAD`
2. 禁止自动跟随跨域重定向
3. 读取响应头中的 `Location`

本地 `huggingface_hub` 下载逻辑明确会通过 `HEAD` 获取：

- `Location`
- `X-Repo-Commit`
- `X-Linked-Etag`
- `X-Linked-Size`

然后把 `Location` 作为实际下载地址使用。

这意味着：

- `GET /datasets/{repo_id}/resolve/{revision}/{path}` 是统一下载入口
- 若出现跨域跳转，`Location` 往往就是签名 CDN / S3 URL

#### 前端实现建议

- 下载按钮：直接使用 `resolve` URL
- “复制直链”按钮：由后端代发 `HEAD resolve`，解析 `Location` 后返回前端
- 私有仓库：不要让浏览器直接持有 HF token，建议走后端代理

### 文本文件查看与 Blob 页面链接

对于类 Hugging Face repo viewer 的前端，通常要同时支持两类链接：

- 原始内容 / 下载：`/resolve/...`
- 页面查看 / 文本预览：`/blob/...`

#### Blob 页面 URL

`huggingface_hub` 在 `upload_file()` 返回值中，明确构造了文件页面 URL：

- `/{repo_prefix}{repo_id}/blob/{revision}/{path}`

对 dataset repo，形式通常是：

- `/datasets/{repo_id}/blob/{revision}/{path}`

它适合：

- 打开文件详情页
- 对文本文件做 inline viewer
- 保持和 Hugging Face Web UI 一致的文件浏览体验

#### 文本查看实现建议

Hugging Face 更偏向“blob 页面 + resolve 原始下载”的组合，而不是统一的文本 JSON API。
因此如果你要实现 repo viewer，建议采用下面的服务端策略：

1. 先用 tree / paths-info 获取文件元数据
2. 判断文件是否属于可文本预览类型
3. 对可预览文件，走后端代理读取 `resolve` 内容，返回：
   - `content`
   - `encoding`
   - `content_type`
   - `truncated`
4. 对大文件或二进制文件，只展示：
   - 文件大小
   - LFS 信息
   - 下载链接
   - blob 页面链接

#### 推荐可预览文本类型

- `txt`
- `md`
- `json`
- `jsonl`
- `yaml` / `yml`
- `csv`
- `tsv`
- `py`
- `js`
- `ts`
- `sh`
- `xml`
- `html`

#### 推荐补充的后端文本查看接口

这不是 Hugging Face 官方接口，但对前端实现非常实用：

- `GET /viewer/file-text?repo_type=dataset&repo_id={repo_id}&revision={revision}&path={path}`

建议返回：

```json
{
  "path": "README.md",
  "revision": "main",
  "content_type": "text/markdown; charset=utf-8",
  "encoding": "utf-8",
  "size": 2379,
  "truncated": false,
  "content": "# Dataset Card\\n...",
  "resolve_url": "/datasets/user/repo/resolve/main/README.md",
  "blob_url": "/datasets/user/repo/blob/main/README.md"
}
```

### 批量路径元信息查询

- Python API：`HfApi.get_paths_info(...)`
- REST：`POST /api/datasets/{repo_id}/paths-info/{revision}`
- 状态：**源码确认**

#### 用途

- 一次查询多个路径的类型和元数据
- 文件树选中多项后的批量 enrich
- 搜索结果、差异列表、下载列表的补充信息查询

#### 请求

客户端以表单方式发送：

```http
POST /api/datasets/{repo_id}/paths-info/{revision}
Content-Type: application/x-www-form-urlencoded
```

字段：

- `paths`: 可重复提交多个
- `expand`: `true/false`

#### 响应元素

文件路径通常返回：

```json
{
  "type": "file",
  "path": "README.md",
  "size": 2379,
  "oid": "f84cb4c97182890fc1dbdeaf1a6a468fd27b4fff",
  "lfs": null
}
```

目录路径通常返回：

```json
{
  "type": "directory",
  "path": "data",
  "oid": "dc943c4c40f53d02b31ced1defa7e5f438d5862e"
}
```

### Hub 侧 Parquet 列表捷径

- REST：`GET /api/datasets/{repo_id}/parquet`
- 状态：**文档确认**

这个接口会返回按 config / split 组织的 Parquet URL。
它对轻量客户端很有价值，但在当前本地 `datasets` 源码中，实际仍然直接请求 viewer 服务的 `/parquet?dataset=...`。

## C. 上传 / 更新内容

### 核心模型：基于 commit，而不是文件级 CRUD

Hub 写平面的核心是 **commit**。
`upload_file()`、`upload_folder()`、`Dataset.push_to_hub()` 这些高级接口，本质上都是对 commit 创建的封装。

### commit 前先确定上传模式

- 内部 Python 流程：`_fetch_upload_modes(...)`
- REST：`POST /api/datasets/{repo_id}/preupload/{revision}`
- 状态：**源码确认**

用途：

- 判断每个文件应使用哪种上传方式：
  - 普通 Git blob
  - Git LFS 对象
  - Xet 对象
- 判断文件是否应被忽略
- 获取 OID 信息，用于去重或 no-op 判定

典型请求体结构：

```json
{
  "files": [
    {
      "path": "data/train-00000-of-00001.parquet",
      "sample": "<base64-sample>",
      "size": 524288000
    }
  ]
}
```

#### `preupload` 具体在干什么

`preupload` 不是“真正上传文件内容”的接口，它本质上是一个**上传前协商接口**。

它的职责是：在客户端正式发起 commit 之前，先让服务端看一眼每个待上传文件的基础信息，然后告诉客户端：

1. 这个文件应该按什么方式上传
2. 这个文件是否应该被忽略
3. 这个文件在远端是否已经存在相同内容

也就是说，`preupload` 解决的是“怎么传、要不要传、是否已经传过”的问题，而不是“把完整文件字节写进去”。

#### 服务端通常会基于什么信息判断

客户端提交给 `preupload` 的只有很轻量的信息：

- `path`
- `size`
- 文件内容前一小段 `sample` 的 base64
- 可选的 `.gitignore` 内容

服务端会据此做几类判定：

- 判断走 `regular` 还是 `lfs`
- 判断该文件是否应被 `.gitignore` 忽略
- 判断远端是否已有相同 OID，可否跳过实际上传
- 某些后端还可能判断走 `xet`

#### 为什么必须先做这一步

如果没有 `preupload`，客户端就无法提前知道：

- 大文件是否要走 LFS
- 空文件是否要特殊处理
- 某些文件是否可以直接跳过
- commit payload 里该按哪种 operation 元数据写入

所以在 `huggingface_hub` 里，`preupload` 是 `create_commit` 之前的关键准备步骤。

#### 典型返回语义

根据本地客户端解析逻辑，服务端返回的每个文件项至少应能表达：

- `path`
- `uploadMode`
  - 常见值：`regular`、`lfs`
- `shouldIgnore`
- `oid`

可理解为类似：

```json
{
  "files": [
    {
      "path": "data/train-00000-of-00001.parquet",
      "uploadMode": "lfs",
      "shouldIgnore": false,
      "oid": "sha256-or-blob-id"
    }
  ]
}
```

#### 与后续接口的关系

整条链路通常是：

1. `preupload`
2. 如果需要，执行 LFS / Xet 预上传
3. `commit`

其中：

- `preupload` 决定传输策略
- LFS/Xet 预上传负责把大文件本体放到对象存储
- `commit` 负责把这次变更登记成仓库历史中的一次提交

#### 对前端或兼容层的实现含义

如果你只是在前端做 repo viewer，通常不会直接碰 `preupload`。
但如果你要做：

- Web 端文件上传
- 浏览器内编辑后保存
- dataset push / repo write 兼容层

那么 `preupload` 基本是必需接口，因为它决定了后续上传链路如何走。

### 创建 commit

- Python API：`HfApi.create_commit(..., repo_type="dataset")`
- REST：`POST /api/datasets/{repo_id}/commit/{revision}`
- Content-Type：`application/x-ndjson`
- 状态：**文档确认** + **源码确认**

这是最核心的数据集更新接口。
请求体是 NDJSON 流，里面包含 commit 操作，例如：

- 添加文件
- 删除文件
- 复制文件

如果目标是最大程度兼容 `huggingface_hub`，这个接口必须模拟。

### 上传单文件

- Python API：`HfApi.upload_file(..., repo_type="dataset")`
- REST 使用方式：当前客户端实现中并没有单独的独立写接口路径
- 状态：**基于源码的推断**

关键澄清：

- `upload_file()` 在当前 `huggingface_hub` 客户端逻辑里，并不是直接调一个独立的 `/upload` 接口。
- 它会创建一个 `CommitOperationAdd`，再转而调用 `create_commit()`。

因此在兼容层实现里，真正必要的是：

- 支持 `preupload`
- 支持 `commit`

### 上传目录

- Python API：`HfApi.upload_folder(..., repo_type="dataset")`
- REST 使用方式：同样是基于 commit 的写平面
- 状态：**基于源码的推断**

和 `upload_file()` 一样，它只是对 commit 操作的高级封装，不是必须单独模拟的一套独立 REST 族。

## D. `datasets.push_to_hub()` 的发布链路

当数据生产端是 `hf-datasets` 时，`Dataset.push_to_hub()` 是最关键的写流程。

### 观察到的流程

从本地 `datasets==2.21.0` 源码看，流程大致是：

1. `HfApi.create_repo(repo_type="dataset", exist_ok=True)`
2. 如有需要，调用 `create_branch(...)`
3. 把数据集转换为 Parquet 分片
4. 检查 repo tree 和已有元数据
5. 准备 `README.md` 与 metadata config 更新
6. 调用 `HfApi.create_commit(...)`

### 关键结论

- 发布到 Hub 的数据集是 **Parquet-first** 的。
- 默认分片目标大小大约是 **500 MB**，除非显式覆盖。
- 旧 split 分片可以在同一组 commit 中被删除或替换。
- `README.md` 和 dataset metadata 也是同一个 commit 工作流的一部分。

### 集成含义

如果你要让自定义后端兼容 `Dataset.push_to_hub()`，最低写接口面应包括：

- `POST /api/repos/create`
- 非 main revision 场景下的 branch 创建支持
- `POST /api/datasets/{repo_id}/preupload/{revision}`
- `POST /api/datasets/{repo_id}/commit/{revision}`
- 用于元数据协调的 repo metadata / tree / download 类接口

## E. 数据集查看 / 预览 API

这部分主要属于 `dataset-viewer` / `datasets-server`。

### 检查数据集是否支持 viewer

- REST：`GET /is-valid?dataset={repo_id}`
- 状态：**文档确认**

这个接口适合前端决定是否启用 preview / search / filter 等能力。

### 列出 splits 和 subsets

- REST：`GET /splits?dataset={repo_id}`
- 状态：**文档确认**

它是发现以下信息的核心接口：

- configs / subsets
- split 名称
- 各 split 级别统计和元数据

### 预览前几行

- REST：`GET /first-rows?dataset={repo_id}&config={config}&split={split}`
- 状态：**文档确认**

这是 UI 或快速检查工具最常用的预览路径。

### 分页读取 rows

- REST：`GET /rows?dataset={repo_id}&config={config}&split={split}&offset={offset}&length={length}`
- 状态：**文档确认**

说明：

- `length` 会受到服务端限制
- 这个接口主要用于表格浏览、分页和行级查看

### 获取导出的 Parquet 文件列表

- REST：`GET /parquet?dataset={repo_id}`
- 状态：**文档确认** + **源码确认**

响应通常包含：

- `partial`
- `pending`
- `failed`
- `parquet_files[]`

在本地 `datasets` 源码中，这个接口会被用来发现 Parquet 导出结果。

### 获取 viewer 侧 dataset info

- REST：`GET /info?dataset={repo_id}`
- 状态：**文档确认** + **源码确认**

响应通常包含：

- `partial`
- `pending`
- `failed`
- `dataset_info`

在本地 `datasets` 源码中，这个接口用于获取导出的 dataset info，尤其是 features 和 config 级别信息。

## F. Repo Tree / Refs / Commits / Branch 详细定义

这部分是实现“类 Hugging Face repo viewer”前端时最关键的 Hub API 集合。

### Repo Tree 列表

- Python API：`HfApi.list_repo_tree(...)`
- REST：`GET /api/datasets/{repo_id}/tree/{revision}` 或 `GET /api/datasets/{repo_id}/tree/{revision}/{path}`
- 状态：**源码确认**

#### 查询参数

- `recursive`: 是否递归列出
- `expand`: 是否返回更丰富信息

#### 典型用途

- 左侧文件树
- 某个目录的 children 列表
- 递归扫描整个 repo

#### 典型返回字段

文件节点：

```json
{
  "type": "file",
  "path": "README.md",
  "size": 2379,
  "oid": "f84cb4c97182890fc1dbdeaf1a6a468fd27b4fff",
  "lfs": null,
  "lastCommit": null,
  "security": null
}
```

目录节点：

```json
{
  "type": "directory",
  "path": "data",
  "oid": "dc943c4c40f53d02b31ced1defa7e5f438d5862e",
  "lastCommit": null
}
```

#### `expand=true` 建议关注的字段

- `lastCommit.oid`
- `lastCommit.title`
- `lastCommit.date`
- `security.safe`
- `security.av_scan`
- `security.pickle_import_scan`

#### 前端建议

- 默认目录浏览用 `recursive=false&expand=false`
- 文件审计或详情浮层再按需请求 `expand=true`
- 大仓库不要首次就递归全量拉树

### Repo Refs 列表

- Python API：`HfApi.list_repo_refs(...)`
- REST：`GET /api/datasets/{repo_id}/refs`
- 状态：**源码确认**

#### 查询参数

- `include_prs=1`：是否包含 pull request refs

#### 典型响应

```json
{
  "branches": [
    {
      "name": "main",
      "ref": "refs/heads/main",
      "targetCommit": "e7da7f221d5bf496a48136c0cd264e630fe9fcc8"
    }
  ],
  "converts": [
    {
      "name": "parquet",
      "ref": "refs/convert/parquet",
      "targetCommit": "abc123"
    }
  ],
  "tags": [],
  "pullRequests": []
}
```

#### 前端用途

- 顶部 branch/tag 切换器
- revision 下拉框
- 展示 `refs/convert/parquet` 这类系统生成 ref

### Commit History

- Python API：`HfApi.list_repo_commits(...)`
- REST：`GET /api/datasets/{repo_id}/commits/{revision}`
- 状态：**源码确认**

#### 查询参数

- `expand[]=formatted`：返回格式化后的 title / message

#### 典型响应元素

```json
{
  "id": "47b62b20b20e06b9de610e840282b7e6c3d51190",
  "authors": [{"user": "alice"}],
  "date": "2023-03-21T09:05:27.000Z",
  "title": "Upload diffusers weights (#48)",
  "message": "Detailed commit message",
  "formatted": {
    "title": "<span>Upload diffusers weights (#48)</span>",
    "message": "<p>Detailed commit message</p>"
  }
}
```

#### 前端用途

- 仓库历史页
- branch 的时间线
- 选择任意 commit 作为快照 revision

### Branch 创建

- Python API：`HfApi.create_branch(...)`
- REST：`POST /api/datasets/{repo_id}/branch/{branch}`
- 状态：**源码确认**

#### 典型请求体

从某个分支创建：

```json
{
  "startingPoint": "main"
}
```

从某个 commit 创建：

```json
{
  "startingPoint": "47b62b20b20e06b9de610e840282b7e6c3d51190"
}
```

#### 前端用途

- “从当前 revision 新建分支”
- 从历史 commit 拉出临时分析分支
- 与后续写接口结合实现编辑 / PR 风格体验

#### 常见错误语义

- `404`: repo 不存在
- `409`: branch 已存在
- `400`: ref 非法

### 单文件下载

- Python API：`HfApi.hf_hub_download(...)`
- 基础 URL：`GET /datasets/{repo_id}/resolve/{revision}/{path}`
- 状态：**源码确认**

`hf_hub_download()` 是“下载到本地缓存”的高级封装，但它底层依赖的仍然是 `resolve`。
因此对前端 viewer 来说，真正必须具备的是：

- `resolve`
- HEAD 元信息获取
- 可选的代理下载

### 整仓下载

- Python API：`snapshot_download(...)`
- 依赖接口：repo tree + resolve
- 状态：**源码确认**

前端通常不会直接逐文件调用它，但后端可以据此设计：

- 下载整个仓库
- 下载某个目录
- 按 pattern 批量导出

## G. 面向前端实现类 Hugging Face Repo Viewer 的接口编排

如果目标是实现一个接近 Hugging Face 官方仓库页的前端 viewer，建议把接口编排拆成下面几个视图层。

### 仓库首页

建议初始化请求：

1. `GET /api/datasets/{repo_id}`
2. `GET /api/datasets/{repo_id}/refs`
3. `GET /api/datasets/{repo_id}/tree/{selected_revision}`

页面可展示：

- repo 基本信息
- 当前默认 branch
- branches / tags / converts
- 根目录文件树
- README 入口

### 文件树浏览页

建议请求：

- `GET /api/datasets/{repo_id}/tree/{revision}/{path}?recursive=false&expand=false`

必要时补充：

- `POST /api/datasets/{repo_id}/paths-info/{revision}`

页面可展示：

- 文件名 / 文件夹名
- 文件大小
- blob id / tree id
- LFS 标记

### 文本文件详情页

建议请求链路：

1. `GET /api/datasets/{repo_id}/tree/{revision}/{parent_path}`
2. 后端自定义 `GET /viewer/file-text?...`
3. 同时构造：
   - `blob_url`
   - `resolve_url`

页面可展示：

- 文本内容
- 语法高亮
- 原始下载
- 复制 resolve 链接
- 复制 blob 链接

### 二进制 / 大文件详情页

建议请求：

1. `POST /api/datasets/{repo_id}/paths-info/{revision}`
2. 后端代理 `HEAD /datasets/{repo_id}/resolve/{revision}/{path}`

页面可展示：

- 文件大小
- LFS 信息
- ETag
- 最终下载地址
- 下载按钮

### 数据集预览页

对结构化文本数据集，不要只靠 repo tree。
应组合 viewer API：

1. `GET /splits?dataset={repo_id}`
2. `GET /first-rows?dataset={repo_id}&config={config}&split={split}`
3. `GET /rows?dataset={repo_id}&config={config}&split={split}&offset={offset}&length={length}`
4. `GET /info?dataset={repo_id}`
5. `GET /parquet?dataset={repo_id}`

页面可展示：

- config / split 切换
- 行级预览
- schema / features
- Parquet 导出入口

### 历史与 revision 切换页

建议请求：

1. `GET /api/datasets/{repo_id}/refs`
2. `GET /api/datasets/{repo_id}/commits/{revision}`

页面可展示：

- branch/tag 列表
- commit 时间线
- 选定 commit 后重载 tree 和文件内容

## H. 推荐补充的后端聚合接口

仅靠 Hugging Face 原生接口，前端能实现大部分 viewer，但为了获得更稳定的体验，建议补几个内部聚合接口。

### 获取文本文件内容

- `GET /viewer/file-text`

参数：

- `repo_type`
- `repo_id`
- `revision`
- `path`
- `max_bytes`

### 获取可下载直链

- `GET /viewer/file-download-link`

参数：

- `repo_type`
- `repo_id`
- `revision`
- `path`

建议返回：

```json
{
  "resolve_url": "/datasets/user/repo/resolve/main/data/train.parquet",
  "redirect_url": "https://cdn-lfs.huggingface.co/...signed...",
  "etag": "abc123",
  "size": 123456789,
  "commit_hash": "47b62b20b20e06b9de610e840282b7e6c3d51190"
}
```

### 获取 repo viewer 页面模型

- `GET /viewer/repo-page`

建议聚合：

- repo 基本信息
- refs
- 当前目录 tree
- README 摘要
- 默认预览文件

## I. `load_dataset()` 与 REST 的映射关系

`load_dataset()` 不是单个 REST 调用，而是一套组合流程。

### 典型的 Hub 数据集加载路径

对于一个 Hub dataset repo，读取流程通常会包含：

1. 检查 repo / builder 元数据
2. 解析 config / splits
3. 获取原始文件或导出的 Parquet 文件
4. 构造 `Dataset` 或 `IterableDataset`

### viewer 加速路径

从本地源码看，`datasets` 会显式请求：

- `/parquet?dataset=...`
- `/info?dataset=...`

并且要求返回头中的 `X-Revision` 与目标 revision 一致。

这是一个关键兼容细节。
如果自定义后端要暴露 viewer 兼容能力，需要返回：

- 正确的 `X-Revision`
- `partial/pending/failed`
- `parquet_files` 或 `dataset_info`

否则 `datasets` 可能会把该 Parquet 导出视为不可用或版本过期。

### 原始文件路径依赖

即便使用了 viewer API，实际的 Parquet 文件 URL 也通常会回到 Hub 文件路径，例如：

- `/datasets/{repo_id}/resolve/refs%2Fconvert%2Fparquet/...`

所以一个完整的兼容后端往往同时需要：

- repo / 文件服务
- viewer 元数据接口

## J. 建议的兼容接口矩阵

### 仓库管理最小接口集

- `POST /api/repos/create`
- `DELETE /api/repos/delete`
- `GET /api/datasets`
- `GET /api/datasets/{repo_id}`
- `GET /api/datasets/{repo_id}/revision/{revision}`
- `GET /api/datasets/{repo_id}/tree/{revision}`
- `POST /api/datasets/{repo_id}/paths-info/{revision}`
- `GET /api/datasets/{repo_id}/refs`
- `GET /api/datasets/{repo_id}/commits/{revision}`
- `POST /api/datasets/{repo_id}/branch/{branch}`
- `PUT /api/datasets/{repo_id}/settings`
- `POST /api/repos/move`

### 数据集内容更新最小接口集

- `POST /api/datasets/{repo_id}/preupload/{revision}`
- `POST /api/datasets/{repo_id}/commit/{revision}`
- `GET /datasets/{repo_id}/resolve/{revision}/{path}`
- `GET /datasets/{repo_id}/blob/{revision}/{path}` 或等价页面路由

### 数据集查看最小接口集

- `GET /is-valid?dataset={repo_id}`
- `GET /splits?dataset={repo_id}`
- `GET /first-rows?dataset={repo_id}&config={config}&split={split}`
- `GET /rows?dataset={repo_id}&config={config}&split={split}&offset={offset}&length={length}`
- `GET /parquet?dataset={repo_id}`
- `GET /info?dataset={repo_id}`

### 强烈建议补充的兼容能力

- Hub 风格的 `/api/datasets/{repo_id}/parquet`
- `refs/convert/parquet` 支持
- 基于 `resolve` 的 HEAD 元信息读取
- 文本文件聚合查看接口
- 下载直链解析接口

## K. 实践结论

### 1. 要把 Hub 和 Viewer 当成两个平面看待

不要把它们混成一层：

- Hub API = 权威仓库 / 写平面
- Viewer API = 读优化的分析 / 预览平面

### 2. `upload_file()` 不是最核心的兼容目标

真正的写契约是：

- preupload 协商
- commit 创建

只要这两层兼容，多数高级 Python API 都可以工作。

### 3. `Dataset.push_to_hub()` 是 Parquet-first

如果你的平台要和 `datasets` 高度互操作，应该优先规划：

- Parquet 分片存储
- metadata card 更新
- split / config 感知的目录布局

### 4. `datasets` 已经默认假设 viewer 加速存在

如果只实现 Hub metadata 与原始文件下载接口，一些读取优化、预览能力和部分流程会退化甚至失败。

### 5. revision 相关响应头非常重要

对 viewer 兼容来说，`X-Revision` 不是装饰字段。
本地 `datasets` 源码会用它来判断 `/parquet` 和 `/info` 返回结果是否和目标 revision 匹配。

### 6. 真正完整的 repo viewer 不能只靠 dataset viewer API

如果目标是 Hugging Face 风格 repo viewer，至少要组合两套接口：

- Hub repo API：tree / refs / commits / branch / resolve / blob
- dataset viewer API：splits / first-rows / rows / parquet / info

前者解决“仓库浏览”，后者解决“数据集预览”。

## L. 建议的实现优先级

如果要构建一个 HF 兼容的内部服务，建议按这个顺序实现：

1. repo metadata 和文件解析
2. repo create / delete / settings
3. preupload + commit 写平面
4. `/parquet` + `/info`
5. `/splits` + `/first-rows` + `/rows`
6. 可选的 repo tree / history / parquet convenience APIs

这个顺序的增量收益最好：

- 先兼容 `huggingface_hub`
- 再兼容 `datasets.push_to_hub()`
- 最后补齐 viewer / UI 兼容性

## 参考来源

### 官方文档

- Hugging Face Hub API Endpoints: https://huggingface.co/docs/hub/en/api
- `huggingface_hub` `HfApi` reference: https://huggingface.co/docs/huggingface_hub/package_reference/hf_api
- `huggingface_hub` repository guide: https://huggingface.co/docs/huggingface_hub/en/guides/repository
- `datasets` loading guide: https://huggingface.co/docs/datasets/en/loading
- `datasets` main classes reference: https://huggingface.co/docs/datasets/package_reference/main_classes
- Dataset viewer index: https://huggingface.co/docs/dataset-viewer/en/index
- Dataset viewer `/parquet`: https://huggingface.co/docs/dataset-viewer/parquet
- Dataset viewer `/splits`: https://huggingface.co/docs/dataset-viewer/en/splits
- Dataset viewer `/first-rows`: https://huggingface.co/docs/dataset-viewer/en/first_rows
- Dataset viewer `/rows`: https://huggingface.co/docs/dataset-viewer/rows

### 本地源码

- `.../site-packages/huggingface_hub/hf_api.py`
- `.../site-packages/huggingface_hub/_commit_api.py`
- `.../site-packages/datasets/load.py`
- `.../site-packages/datasets/arrow_dataset.py`
- `.../site-packages/datasets/utils/_dataset_viewer.py`
