# Hugging Face Spaces / Repo REST API 分析

生成时间：2026-03-19

## 范围

本文调研 Hugging Face Spaces 相关接口，并结合本仓库中的 `csghub-server` 代码，分析：

- Hugging Face 官方/客户端当前暴露的 Space 能力面
- `csghub-server` 已有的 Space 原生接口
- `csghub-server` 已实现的 HF 兼容接口
- `csghub-server` 与 HF Spaces 在接口层的差距与补齐建议

本文适合作为实现 HF 兼容 Space API、代理层或者后端适配层时的参考文档。

## 证据来源

本文使用了两类证据来源：

1. Hugging Face 官方文档，检查时间为 2026-03-19
2. 代码源码
   - `huggingface_hub` 最新公开源码（GitHub `main` 分支，检查时间为 2026-03-19）
   - 本地仓库 `csghub-server` 中的 handler/router/types 实现

标记说明：

- **源码确认**：直接从源码确认了 REST 路径或行为
- **文档确认**：官方文档描述了能力，但未必展开到底层实现细节
- **推断**：基于现有源码和路由组合做出的合理推断

## 高层结论

Hugging Face 的 Space 能力可以分成两层：

1. **Repo/文件平面**
   - 创建 Space repo
   - 获取 Space repo 元数据
   - 解析/下载 Space 仓库文件
   - 提交文件、预上传、复制 repo

2. **Runtime/运维平面**
   - 查询 Space runtime
   - 申请硬件
   - 配置 sleep time
   - pause / restart
   - 配置 persistent storage
   - 管理 secrets / variables

`csghub-server` 当前的情况是：

- 已具备一套**平台原生 Space 管理接口**
- 已实现一部分 **HF 兼容 Repo/文件接口**
- 对 **HF Runtime 管理接口** 的兼容还不完整

也就是说，当前仓库更像是：

- **已兼容 HF Space repo 读写的一部分**
- **未完全兼容 HF Space runtime 管理面**

## Hugging Face Spaces 官方接口面

## A. Space 仓库创建 / 复制

### 创建 Space repo

- Python API：`HfApi.create_repo(..., repo_type="space")`
- REST：`POST /api/repos/create`
- 状态：**源码确认**

`huggingface_hub` 源码中，`create_repo` 对 `repo_type == "space"` 时会额外接受：

- `sdk`
- `hardware`
- `storageTier`
- `sleepTimeSeconds`
- `secrets`
- `variables`

典型请求体：

```json
{
  "type": "space",
  "name": "my-space",
  "organization": "my-org",
  "private": true,
  "sdk": "gradio",
  "hardware": "t4-medium",
  "storageTier": "small",
  "sleepTimeSeconds": 3600,
  "secrets": [
    {
      "key": "HF_TOKEN",
      "value": "xxx"
    }
  ],
  "variables": [
    {
      "key": "MODEL_REPO_ID",
      "value": "my-org/my-model"
    }
  ]
}
```

这说明 HF 的 Space 创建不是只有 repo 元信息，还允许在创建时一次性配置运行资源和环境变量。

### 复制 Space

- Python API：`HfApi.duplicate_space(...)` / `HfApi.duplicate_repo(..., repo_type="space")`
- REST：`POST /api/spaces/{from_id}/duplicate`
- 状态：**源码确认**

典型请求体：

```json
{
  "repository": "target-user/target-space",
  "private": true,
  "hardware": "t4-medium",
  "storageTier": "small",
  "sleepTimeSeconds": 3600,
  "secrets": [],
  "variables": []
}
```

这个接口是服务端复制，不是本地 clone + push。

## B. Space 列表 / 元数据 / 文件访问

### 列出 Spaces

- Python API：`HfApi.list_spaces(...)`
- REST：`GET /api/spaces`
- 状态：**源码确认**

常见查询参数：

- `filter`
- `author`
- `search`
- `datasets`
- `models`
- `linked`
- `sort`
- `limit`
- `expand`
- `full`

### 获取 Space 元数据

- Python API：`HfApi.space_info(...)`
- REST：
  - `GET /api/spaces/{repo_id}`
  - `GET /api/spaces/{repo_id}/revision/{revision}`
- 状态：**文档确认 + 推断**

虽然本次主要直接验证了 `list_spaces` 和 `huggingface_hub` 的 Space 运行管理方法，但 Hugging Face Hub 对 model/dataset/space 的元数据读取模式是一致的，`csghub-server` 目前也是按这一模式实现兼容。

### 解析 / 下载 Space 文件

- 公共文件 URL 模式：
  - `GET /spaces/{repo_id}/resolve/{revision}/{path}`
- 状态：**文档确认**

该路径用于：

- 下载 Space 仓库中的文件
- 为 SDK 生成稳定的文件解析路径
- 支撑 `snapshot_download` / `hf_hub_download` 一类调用

## C. Space Runtime / 运维接口

这部分是 Hugging Face Spaces 与普通 repo API 的核心差异。

### 获取运行时信息

- Python API：`HfApi.get_space_runtime(repo_id)`
- REST：`GET /api/spaces/{repo_id}/runtime`
- 状态：**源码确认**

该接口返回 `SpaceRuntime`，通常包含：

- 当前 stage / status
- 当前硬件
- 请求中的硬件
- 可能的 storage/runtime 信息

### 申请硬件

- Python API：`HfApi.request_space_hardware(repo_id, hardware, sleep_time=None)`
- REST：`POST /api/spaces/{repo_id}/hardware`
- 状态：**源码确认**

典型请求体：

```json
{
  "flavor": "t4-medium",
  "sleepTimeSeconds": 3600
}
```

### 设置休眠时间

- Python API：`HfApi.set_space_sleep_time(repo_id, sleep_time)`
- REST：`POST /api/spaces/{repo_id}/sleeptime`
- 状态：**源码确认**

典型请求体：

```json
{
  "seconds": 3600
}
```

### 暂停 Space

- Python API：`HfApi.pause_space(repo_id)`
- REST：`POST /api/spaces/{repo_id}/pause`
- 状态：**源码确认**

### 重启 Space

- Python API：`HfApi.restart_space(repo_id, factory_reboot=False)`
- REST：`POST /api/spaces/{repo_id}/restart`
- 状态：**源码确认**

如果 `factory_reboot=true`，则带 query 参数：

```text
POST /api/spaces/{repo_id}/restart?factory=true
```

### 申请持久化存储

- Python API：`HfApi.request_space_storage(repo_id, storage)`
- REST：`POST /api/spaces/{repo_id}/storage`
- 状态：**源码确认**

典型请求体：

```json
{
  "tier": "small"
}
```

### 管理 Space Secrets

- Python API：
  - `HfApi.add_space_secret(...)`
  - `HfApi.delete_space_secret(...)`
- REST：
  - `POST /api/spaces/{repo_id}/secrets`
  - `DELETE /api/spaces/{repo_id}/secrets`
- 状态：**源码确认**

新增/更新 secret：

```json
{
  "key": "HF_TOKEN",
  "value": "xxx",
  "description": "optional"
}
```

删除 secret：

```json
{
  "key": "HF_TOKEN"
}
```

### 管理 Space Variables

- Python API：
  - `HfApi.get_space_variables(...)`
  - `HfApi.add_space_variable(...)`
  - `HfApi.delete_space_variable(...)`
- REST：
  - `GET /api/spaces/{repo_id}/variables`
  - `POST /api/spaces/{repo_id}/variables`
  - `DELETE /api/spaces/{repo_id}/variables`
- 状态：**源码确认**

新增/更新 variable：

```json
{
  "key": "MODEL_REPO_ID",
  "value": "my-org/my-model",
  "description": "optional"
}
```

删除 variable：

```json
{
  "key": "MODEL_REPO_ID"
}
```

## `csghub-server` 当前已有的 Space 接口

## A. 平台原生 Space 管理接口

根据 `csghub-server/api/router/api.go` 和 `csghub-server/api/handler/space.go`，当前已提供：

### 基础 CRUD / 查询

- `GET /spaces`
- `POST /spaces`
- `GET /spaces/{namespace}/{name}`
- `PUT /spaces/{namespace}/{name}`
- `DELETE /spaces/{namespace}/{name}`

### 运行与状态

- `POST /spaces/{namespace}/{name}/run`
- `POST /spaces/{namespace}/{name}/wakeup`
- `POST /spaces/{namespace}/{name}/stop`
- `GET /spaces/{namespace}/{name}/status`
- `GET /spaces/{namespace}/{name}/logs`
- `GET /spaces/{namespace}/{name}/cuda-versions/{resource_type}`

### Repo 文件能力

- `GET /spaces/{namespace}/{name}/branches`
- `GET /spaces/{namespace}/{name}/tags`
- `POST /spaces/{namespace}/{name}/preupload/{revision}`
- `POST /spaces/{namespace}/{name}/commit/{revision}`
- `GET /spaces/{namespace}/{name}/tree`
- `GET /spaces/{namespace}/{name}/refs/{ref}/tree/*path`
- `GET /spaces/{namespace}/{name}/resolve/*file_path`
- `GET /spaces/{namespace}/{name}/raw/*file_path`
- `PUT /spaces/{namespace}/{name}/raw/*file_path`
- `DELETE /spaces/{namespace}/{name}/raw/*file_path`
- `POST /spaces/{namespace}/{name}/upload_file`
- `POST /spaces/{namespace}/{name}/mirror`
- `POST /spaces/{namespace}/{name}/mirror/sync`

这套接口是平台原生设计，并不完全等价于 HF 的 `/api/spaces/{repo_id}/runtime` 一族，但已经覆盖了很多平台管理能力。

## B. Space 辅助管理接口

### Space 资源规格

- `GET /space_resources`
- `POST /space_resources`
- `PUT /space_resources/{id}`
- `DELETE /space_resources/{id}`
- `GET /space_resources/hardware_types`

这些接口对应本平台“可申请资源池/硬件类型”的管理，不是 HF 官方对外标准接口。

### Space 模板

- `GET /space_templates`
- `POST /space_templates`
- `PUT /space_templates/{id}`
- `DELETE /space_templates/{id}`
- `GET /space_templates/{type}`

### Space SDK 管理

- `GET /space_sdks`
- `POST /space_sdks`
- `PUT /space_sdks/{id}`
- `DELETE /space_sdks/{id}`

### 用户 / 组织 /批量列表

- `GET /organization/{namespace}/spaces`
- `GET /user/{username}/spaces`
- `GET /user/{username}/likes/spaces`
- `POST /list/spaces_by_path`

## C. `csghub-server` 已实现的 HF 兼容 Space 接口

在 `createMappingRoutes(...)` 中，仓库已经暴露了一部分 Hugging Face 兼容路由。

### 1. HF 文件下载兼容层

- `GET /api/hf/spaces/{namespace}/{name}/resolve/{branch}/*file_path`
- `HEAD /api/hf/spaces/{namespace}/{name}/resolve/{branch}/*file_path`

这部分用于兼容 HF SDK 的文件解析/下载行为。

### 2. HF Space 元数据兼容层

- `GET /api/hf/api/spaces/{namespace}/{name}`
- `GET /api/hf/api/spaces/{namespace}/{name}/revision/{ref}`

当前这两个接口最终复用了 `repoCommonHandler.SDKListFiles`。

这意味着它们更偏向“repo file listing / repo info 兼容”，而不是完整的 HF Space runtime 元数据面。

### 3. HF 创建 repo 兼容层

- `POST /api/hf/api/repos/create`

由于 `repoCommonHandler.CreateRepo` 是通用 repo 创建入口，**推断** 只要 payload 中传 `type: "space"`，并且后端已支持对应字段解析，就可以兼容 HF 的创建 Space repo 行为。

但是否已经完整支持以下 HF Space 创建参数，还需要继续检查 `CreateRepo` 的请求体解析逻辑：

- `sdk`
- `hardware`
- `storageTier`
- `sleepTimeSeconds`
- `secrets`
- `variables`

从当前 Space 原生接口类型定义看，平台内部主要使用的是：

- `resource_id`
- `cluster_id`
- `env`
- `secrets`
- `variables`
- `template`
- `sdk`

因此它和 HF 原生字段并非一一同名。

## 兼容性对照

| 能力 | Hugging Face 标准接口 | `csghub-server` 当前状态 | 说明 |
|---|---|---|---|
| 创建 Space repo | `POST /api/repos/create` | 部分兼容 | 路由已存在，但 Space 特有字段是否完全兼容需继续校验 |
| 复制 Space | `POST /api/spaces/{repo_id}/duplicate` | 未见兼容 | 当前未看到 HF duplicate 路由 |
| 列出 Spaces | `GET /api/spaces` | 未见 HF 兼容；有原生 `GET /spaces` | 语义接近，但不是同一路径/参数 |
| 获取 Space info | `GET /api/spaces/{repo_id}` | 已有 HF 兼容 | 通过 `/api/hf/api/spaces/{namespace}/{name}` 提供 |
| 获取 revision info | `GET /api/spaces/{repo_id}/revision/{ref}` | 已有 HF 兼容 | 已有对应路由 |
| resolve 下载 | `GET /spaces/{repo_id}/resolve/{ref}/{path}` | 已有 HF 兼容 | `/api/hf/spaces/.../resolve/...` |
| 获取 runtime | `GET /api/spaces/{repo_id}/runtime` | 未兼容 | 当前只有原生 `GET /spaces/{namespace}/{name}/status` |
| 申请 hardware | `POST /api/spaces/{repo_id}/hardware` | 未兼容 | 平台有 `/space_resources` 和创建时 `resource_id`，但不是 HF 路径 |
| 设置 sleep time | `POST /api/spaces/{repo_id}/sleeptime` | 未兼容 | 当前未见等价路由 |
| pause | `POST /api/spaces/{repo_id}/pause` | 未兼容 | 平台是 `stop` 语义，不完全等价 |
| restart | `POST /api/spaces/{repo_id}/restart` | 未兼容 | 平台是 `run` / `wakeup` |
| storage | `POST /api/spaces/{repo_id}/storage` | 未兼容 | 当前无 HF storage 管理路由 |
| secrets | `POST/DELETE /api/spaces/{repo_id}/secrets` | 未兼容 | 平台字段存在，但缺 HF 专用管理路由 |
| variables | `GET/POST/DELETE /api/spaces/{repo_id}/variables` | 未兼容 | 平台字段存在，但缺 HF 专用管理路由 |

## 关键差异分析

## 1. HF 的 Space 是“Repo + Runtime”的组合体

对 HF 来说，Space 不只是一个 git repo。

它还天然包含：

- sdk 类型
- 硬件申请状态
- storage
- sleep 策略
- secrets / variables
- pause / restart 等运行控制

而 `csghub-server` 当前的架构更像：

- repo 侧接口单独复用通用 repo handler
- runtime 侧接口通过平台原生 `/spaces/.../run|stop|status|logs` 处理
- 资源规格通过 `/space_resources` 独立管理

这导致它对 HF SDK 的 repo 兼容已经有基础，但对 HF 的 runtime 管理面还没有直接对齐。

## 2. `stop/wakeup/run` 与 `pause/restart/runtime` 不是一一等价

HF 语义：

- `runtime`：查询当前运行态细节
- `pause`：主动暂停
- `restart`：重新拉起，支持 factory reboot

当前平台语义：

- `run`：触发部署 / 启动
- `wakeup`：唤醒 sleeping space
- `stop`：停止
- `status`：通过 SSE 持续推送状态
- `logs`：通过 SSE 推送 build/container 日志

两者语义相近，但不完全一致，直接映射时需要显式做状态机转换。

## 3. 资源模型不一致

HF 用的是：

- `hardware`
- `storageTier`
- `sleepTimeSeconds`

`csghub-server` 用的是：

- `resource_id`
- `cluster_id`
- `min_replica`
- `driver_version`

因此若要做 HF 完整兼容，必须新增一层“HF Space 配置 -> 平台资源模型”的映射。

## 建议的补齐顺序

如果目标是优先让 `huggingface_hub` 的 Space 能力可用，建议按下面顺序补齐：

### 第一阶段：补齐最小 HF 兼容面

1. `GET /api/spaces`
2. `GET /api/spaces/{repo_id}`
3. `GET /api/spaces/{repo_id}/revision/{revision}`
4. `GET /spaces/{repo_id}/resolve/{revision}/{path}`
5. `POST /api/repos/create` 对 `type=space` 的完整字段兼容

这一阶段完成后，Space 的发现、创建、元数据读取和文件访问会更接近 HF 标准。

### 第二阶段：补齐 runtime 管理面

1. `GET /api/spaces/{repo_id}/runtime`
2. `POST /api/spaces/{repo_id}/hardware`
3. `POST /api/spaces/{repo_id}/sleeptime`
4. `POST /api/spaces/{repo_id}/pause`
5. `POST /api/spaces/{repo_id}/restart`

这一阶段完成后，`huggingface_hub` 的运行时控制方法才能真正工作。

### 第三阶段：补齐环境与存储

1. `POST /api/spaces/{repo_id}/storage`
2. `DELETE /api/spaces/{repo_id}/storage`
3. `POST /api/spaces/{repo_id}/secrets`
4. `DELETE /api/spaces/{repo_id}/secrets`
5. `GET /api/spaces/{repo_id}/variables`
6. `POST /api/spaces/{repo_id}/variables`
7. `DELETE /api/spaces/{repo_id}/variables`

### 第四阶段：补齐复制

1. `POST /api/spaces/{repo_id}/duplicate`

这个接口对模板化/一键 fork Space 场景很重要。

## 对 `csghub-server` 的实现建议

## 1. 新增一层 HF Space Adapter

建议不要直接把 HF 路由硬绑到现有 `/spaces/...` handler 上，而是新增一个明确的适配层，负责：

- 路径参数 `repo_id <-> namespace/name` 的转换
- HF 字段到平台字段的转换
- 平台状态到 HF `SpaceRuntime` 结构的转换

这样可以减少对现有原生 API 的侵入。

## 2. 统一 Space 状态映射

建议建立标准映射表，例如：

- `Building` -> HF building stage
- `Running` -> HF running stage
- `Sleeping` -> HF sleeping stage
- `Stopped` -> HF paused/stopped stage
- `DeployFailed` / `RuntimeError` -> HF error stage

这里需要注意：HF 的 `pause` 与平台 `stop` 是否完全一致，需要产品语义确认。

## 3. 把资源选择抽象成 HF hardware flavor

建议维护一张映射表：

- HF `cpu-basic` / `t4-medium` / `a10g-large` ...
- 平台 `resource_id + cluster_id + driver_version`

只有建立这层映射，`request_space_hardware` 才能自然落到现有资源体系。

## 4. Secrets / Variables 单独做专用路由

虽然 `CreateSpaceReq` / `UpdateSpaceReq` 已经有：

- `secrets`
- `variables`
- `env`

但 HF 客户端期望的是独立增删接口，而不是只能在创建/更新 Space 时整体覆盖。

因此最好新增专用 handler，避免把 HF 细粒度操作强行塞进当前更新接口。

## 参考代码位置

### `csghub-server`

- `csghub-server/api/router/api.go`
- `csghub-server/api/handler/space.go`
- `csghub-server/api/handler/space_resource.go`
- `csghub-server/api/handler/space_template.go`
- `csghub-server/api/handler/space_sdk.go`
- `csghub-server/common/types/space.go`
- `csghub-server/common/types/space_resource.go`

### Hugging Face / `huggingface_hub`

- `https://raw.githubusercontent.com/huggingface/huggingface_hub/main/src/huggingface_hub/hf_api.py`
- `https://huggingface.co/docs/huggingface_hub/package_reference/hf_api`
- `https://huggingface.co/docs/hub/spaces-overview`
- `https://huggingface.co/docs/hub/spaces-gpus`

## 总结

如果从“HF Spaces 兼容性”这个角度看，`csghub-server` 当前最强的是：

- Space repo 本身的管理能力
- 平台原生运行控制能力
- 一部分 HF 文件/元数据兼容路由

当前最明显的缺口是：

- `GET /api/spaces`
- `GET /api/spaces/{repo_id}/runtime`
- `POST /api/spaces/{repo_id}/hardware`
- `POST /api/spaces/{repo_id}/sleeptime`
- `POST /api/spaces/{repo_id}/pause`
- `POST /api/spaces/{repo_id}/restart`
- `POST/DELETE /api/spaces/{repo_id}/secrets`
- `GET/POST/DELETE /api/spaces/{repo_id}/variables`
- `POST /api/spaces/{repo_id}/storage`
- `POST /api/spaces/{repo_id}/duplicate`

因此，若你的目标是让 `huggingface_hub` 的 Space 相关 API 在本平台上“开箱可用”，下一步最值得做的是先补一层 **HF Space runtime 适配接口**，而不是继续扩展平台原生 `/spaces/...` 路由。
