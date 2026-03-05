# LLM 强化学习融合 DCAI Platform 产品与架构设计

> 本文档描述如何将 AReaL (Advanced Reasoning and Learning) 强化学习框架集成到 DCAI Platform 中，为用户提供从数据准备、模型训练到模型部署的全流程 RL 能力。

---

## 目录

1. [产品概述](#1-产品概述)
2. [用户场景与用例](#2-用户场景与用例)
3. [功能需求](#3-功能需求)
4. [系统架构设计](#4-系统架构设计)
5. [数据模型设计](#5-数据模型设计)
6. [API 设计](#6-api-设计)
7. [核心流程设计](#7-核心流程设计)
8. [基础设施与部署](#8-基础设施与部署)
9. [安全与权限](#9-安全与权限)
10. [性能与扩展性](#10-性能与扩展性)

---

## 1. 产品概述

### 1.1 愿景

将 DCAI Platform 打造为支持全生命周期 LLM 开发的平台，在现有数据管理、模型评估、应用部署能力基础上，增加**强化学习训练**能力，形成 **Data → RL Training → Evaluation → Deployment** 的完整闭环。

### 1.2 核心能力矩阵

| 能力域 | 现有功能 | 新增 RL 功能 |
|--------|----------|--------------|
| **数据** | 数据集上传、管理、版本控制 | RL 训练数据格式支持、轨迹数据存储 |
| **训练** | 基础微调 (Fine-tuning) | PPO/GRPO/DPO 强化学习训练 |
| **评估** | 基准测试、人工评估 | RL 奖励模型评估、策略对比 |
| **部署** | 模型发布、API 服务 | RL 训练模型版本管理、热更新 |
| **监控** | 训练日志、指标图表 | 奖励曲线、KL 散度、策略熵监控 |

### 1.3 目标用户

1. **AI 研究员**: 需要快速迭代 RL 算法，对比不同策略效果
2. **模型开发者**: 需要基于反馈优化模型行为
3. **企业用户**: 需要基于私有数据训练专属模型
4. **开源贡献者**: 需要复现和分享 RL 训练配置

---

## 2. 用户场景与用例

### 2.1 用户场景

#### 场景 1: 基于人类反馈的模型对齐 (RLHF)
```
用户流程:
1. 上传提示数据集到 DCAI Platform
2. 配置奖励模型 (使用内置或自定义)
3. 创建 PPO 训练任务，选择基础模型
4. 配置训练参数 (学习率、KL 系数、批次大小等)
5. 启动训练，实时监控奖励曲线和 KL 散度
6. 训练完成后，自动评估并与基础模型对比
7. 发布训练好的模型到模型市场
```

#### 场景 2: 数学推理能力强化 (RLVR)
```
用户流程:
1. 选择公开的 GSM8K 数学数据集
2. 配置可验证奖励函数 (基于答案正确性)
3. 使用 GRPO 算法训练 (无需单独训练 Critic)
4. 训练过程中实时查看 pass@k 指标
5. 导出训练轨迹用于分析错误模式
6. 将优化后的模型部署为推理服务
```

#### 场景 3: 多轮对话策略优化
```
用户流程:
1. 导入多轮对话数据集
2. 配置多轮奖励函数 (考虑对话连贯性、有用性)
3. 使用 Multi-Turn Workflow 进行训练
4. 对比单轮 vs 多轮训练效果
5. A/B 测试不同策略在真实场景的表现
```

### 2.2 用例图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DCAI Platform RL System                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
│  │   研究员     │    │  模型开发者  │    │   企业用户   │              │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
│         │                   │                   │                       │
│         │ 创建训练实验      │ 配置 RL 任务      │ 部署私有模型          │
│         │ 对比算法效果      │ 监控训练过程      │ 管理模型版本          │
│         │ 分享训练配置      │ 评估模型质量      │ 控制访问权限          │
│         │                   │                   │                       │
│         └───────────────────┼───────────────────┘                       │
│                             ▼                                           │
│         ┌─────────────────────────────────────────┐                     │
│         │         RL Training Core                │                     │
│         │  ┌─────────┐ ┌─────────┐ ┌─────────┐   │                     │
│         │  │ Dataset │ │  Train  │ │ Evaluate│   │                     │
│         │  └────┬────┘ └────┬────┘ └────┬────┘   │                     │
│         │       └───────────┼───────────┘        │                     │
│         │                   ▼                    │                     │
│         │            ┌────────────┐              │                     │
│         │            │   Model    │              │                     │
│         │            │ Repository │              │                     │
│         │            └────────────┘              │                     │
│         └─────────────────────────────────────────┘                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. 功能需求

### 3.1 功能模块划分

```
DCAI Platform RL Module
│
├── 📁 RL Project Management
│   ├── 创建/编辑/删除 RL 项目
│   ├── 项目模板 (PPO/GRPO/DPO/RLVR)
│   └── 项目版本与实验追踪
│
├── 📁 Dataset Integration
│   ├── 训练数据格式转换 (SFT → RL)
│   ├── 轨迹数据可视化
│   └── 在线数据增强
│
├── 📁 Training Orchestration
│   ├── 训练任务生命周期管理
│   ├── 超参数配置界面
│   ├── 分布式训练调度
│   └── 训练任务队列管理
│
├── 📁 Reward Function
│   ├── 内置奖励函数库
│   ├── 自定义奖励函数上传
│   ├── 奖励模型训练
│   └── 奖励函数 A/B 测试
│
├── 📁 Monitoring & Logging
│   ├── 实时训练指标 (TensorBoard)
│   ├── 奖励曲线可视化
│   ├── 样本输出检查
│   └── 异常检测与告警
│
├── 📁 Evaluation & Comparison
│   ├── 自动化评估流水线
│   ├── 策略对比工具
│   ├── 人工评估接口
│   └── 基准测试集成
│
└── 📁 Model Deployment
    ├── RL 模型版本管理
    ├── 模型发布工作流
    └── 推理服务热更新
```

### 3.2 详细功能需求

#### 3.2.1 RL 项目管理 (FR-PM)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-PM-001 | 项目创建 | P0 | 支持基于模板创建 RL 项目 |
| FR-PM-002 | 项目模板 | P0 | 内置 PPO、GRPO、DPO、RLVR 模板 |
| FR-PM-003 | 实验追踪 | P1 | 集成 MLflow 记录超参数和指标 |
| FR-PM-004 | 项目共享 | P1 | 支持项目配置导出/导入 |
| FR-PM-005 | 版本对比 | P1 | 对比不同实验的训练结果 |

#### 3.2.2 数据集集成 (FR-DS)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-DS-001 | 格式支持 | P0 | 支持 JSONL、Parquet、HuggingFace Dataset |
| FR-DS-002 | 数据预览 | P0 | 预览训练数据和奖励标注 |
| FR-DS-003 | 轨迹存储 | P1 | 存储和查询训练轨迹数据 |
| FR-DS-004 | 数据增强 | P2 | 在线数据增强和采样策略 |

#### 3.2.3 训练编排 (FR-TR)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-TR-001 | 任务提交 | P0 | 提交 RL 训练任务到集群 |
| FR-TR-002 | 超参数配置 | P0 | 可视化配置训练参数 |
| FR-TR-003 | 分布式训练 | P0 | 支持多节点、多 GPU 训练 |
| FR-TR-004 | 断点续训 | P1 | 支持从 checkpoint 恢复训练 |
| FR-TR-005 | 自动调参 | P2 | 超参数自动搜索 (Optuna) |

#### 3.2.4 奖励函数 (FR-RF)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-RF-001 | 内置奖励 | P0 | 规则奖励、模型奖励、混合奖励 |
| FR-RF-002 | 自定义奖励 | P1 | 上传自定义 Python 奖励函数 |
| FR-RF-003 | 奖励模型训练 | P1 | 基于偏好数据训练奖励模型 |
| FR-RF-004 | 奖励调试 | P2 | 奖励函数调试和测试工具 |

#### 3.2.5 监控日志 (FR-MO)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-MO-001 | 实时指标 | P0 | 奖励、KL、Loss、学习率实时曲线 |
| FR-MO-002 | 样本检查 | P1 | 查看训练生成的样本输出 |
| FR-MO-003 | 资源监控 | P1 | GPU/CPU/内存使用率监控 |
| FR-MO-004 | 告警通知 | P2 | 训练异常邮件/钉钉通知 |

#### 3.2.6 评估对比 (FR-EV)

| ID | 需求 | 优先级 | 描述 |
|----|------|--------|------|
| FR-EV-001 | 自动评估 | P0 | 训练完成后自动运行评估 |
| FR-EV-002 | 策略对比 | P1 | 并排对比多个策略输出 |
| FR-EV-003 | 基准测试 | P1 | 集成常见基准 (GSM8K, HumanEval 等) |
| FR-EV-004 | 人工评估 | P2 | 人工打分和偏好标注界面 |

---

## 4. 系统架构设计

### 4.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 DCAI Platform (User Layer)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  │   Web UI    │  │  API Gateway │  │   CLI Tool  │  │   SDK       │  │  Notebook │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘  │
│         │                │                │                │               │        │
└─────────┼────────────────┼────────────────┼────────────────┼───────────────┼────────┘
          │                │                │                │               │
          └────────────────┴────────────────┴────────────────┘               │
                                       │                                      │
                                       ▼                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DCAI Backend (API Layer)                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         Django + FastAPI (REST/gRPC)                        │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │    │
│  │  │  RL Project │ │  Training   │ │  Dataset    │ │   Model     │           │    │
│  │  │    Service  │ │   Service   │ │   Service   │ │   Service   │           │    │
│  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │    │
│  │         └───────────────┼───────────────┴───────────────┘                  │    │
│  │                         │                                                  │    │
│  │         ┌───────────────▼───────────────┐                                  │    │
│  │         │      RL Orchestrator          │                                  │    │
│  │         │  (Training Job Management)    │                                  │    │
│  │         └───────────────┬───────────────┘                                  │    │
│  └─────────────────────────┼──────────────────────────────────────────────────┘    │
└────────────────────────────┼────────────────────────────────────────────────────────┘
                             │
                             │ REST/gRPC/消息队列
                             ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            AReaL RL Engine (Compute Layer)                           │
│                                                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────┐      │
│   │                      Training Cluster Scheduler                           │      │
│   │                    (Kubernetes / Slurm / Ray)                             │      │
│   └──────────────────────────────────────┬───────────────────────────────────┘      │
│                                          │                                           │
│        ┌─────────────────────────────────┼─────────────────────────────────┐        │
│        │                                 │                                 │        │
│        ▼                                 ▼                                 ▼        │
│   ┌──────────┐                     ┌──────────┐                     ┌──────────┐   │
│   │  Train   │◄───────────────────►│  Train   │◄───────────────────►│  Train   │   │
│   │ Worker 1 │    XCCL AllReduce   │ Worker 2 │                     │ Worker N │   │
│   └────┬─────┘                     └────┬─────┘                     └────┬─────┘   │
│        │                                │                                │         │
│        │ Rollout (Async)                │ Rollout (Async)                │         │
│        ▼                                ▼                                ▼         │
│   ┌──────────┐                     ┌──────────┐                     ┌──────────┐   │
│   │  vLLM    │                     │  vLLM    │                     │  vLLM    │   │
│   │Inference │◄───────────────────►│Inference │◄───────────────────►│Inference │   │
│   │ Engine 1 │                     │ Engine 2 │                     │ Engine N │   │
│   └──────────┘                     └──────────┘                     └──────────┘   │
│                                                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────┐      │
│   │                         Shared Storage                                  │      │
│   │     (NFS / Ceph / S3 for Checkpoints, Logs, Trajectories)               │      │
│   └──────────────────────────────────────────────────────────────────────────┘      │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 核心组件设计

#### 4.2.1 RL Orchestrator (训练编排器)

```python
class RLOrchestrator:
    """
    核心编排组件，负责:
    1. 接收训练任务请求
    2. 资源调度与分配
    3. 训练生命周期管理
    4. 状态同步与事件广播
    """
    
    def submit_training_job(self, config: RLTrainingConfig) -> JobID:
        """提交训练任务"""
        # 1. 验证配置
        # 2. 分配资源
        # 3. 创建任务记录
        # 4. 启动训练进程
        pass
    
    def get_job_status(self, job_id: JobID) -> JobStatus:
        """查询任务状态"""
        pass
    
    def cancel_job(self, job_id: JobID) -> bool:
        """取消训练任务"""
        pass
    
    def stream_metrics(self, job_id: JobID) -> AsyncIterator[Metrics]:
        """流式返回训练指标"""
        pass
```

#### 4.2.2 AReaL Integration Adapter

```python
class AReaLAdapter:
    """
    AReaL 框架适配器，负责:
    1. 将 DCAI 配置转换为 AReaL 配置
    2. 管理 AReaL 训练进程
    3. 指标收集与转发
    """
    
    def convert_config(self, dcai_config: DCAIRLConfig) -> AReaLConfig:
        """配置转换"""
        return AReaLConfig(
            experiment_name=dcai_config.project_name,
            actor=PPOActorConfig(
                path=dcai_config.base_model,
                eps_clip=dcai_config.ppo_eps_clip,
                kl_ctl=dcai_config.kl_coefficient,
            ),
            rollout=InferenceEngineConfig(
                backend=dcai_config.inference_backend,  # vllm/sglang
                max_concurrent_rollouts=dcai_config.concurrent_rollouts,
            ),
            gconfig=GenerationHyperparameters(
                temperature=dcai_config.temperature,
                max_new_tokens=dcai_config.max_tokens,
                n_samples=dcai_config.grpo_group_size,
            ),
        )
    
    def launch_training(self, config: AReaLConfig, 
                       resource_spec: ResourceSpec) -> TrainingProcess:
        """启动 AReaL 训练进程"""
        pass
```

### 4.3 服务间通信架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Service Communication                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   DCAI Backend              Message Queue               AReaL Cluster  │
│   ┌─────────┐               ┌──────────┐               ┌───────────┐   │
│   │ API     │──────────────►│  Redis   │◄──────────────│  Trainer  │   │
│   │ Server  │   Publish     │  Pub/Sub │    Subscribe   │  Workers  │   │
│   └────┬────┘               └────┬─────┘               └─────┬─────┘   │
│        │                         │                          │         │
│        │  REST/gRPC              │  Metrics Stream          │         │
│        ▼                         ▼                          ▼         │
│   ┌─────────┐               ┌──────────┐               ┌───────────┐   │
│   │ WebSocket│◄─────────────│  SSE     │◄──────────────│  Monitor  │   │
│   │ Gateway  │   Push       │  Server  │   Forward      │  Agent    │   │
│   └─────────┘               └──────────┘               └───────────┘   │
│                                                                         │
│   Communication Patterns:                                               │
│   1. Sync:  REST API for CRUD operations                                │
│   2. Async: Message Queue for job submission                            │
│   3. Stream: WebSocket/SSE for real-time metrics                        │
│   4. File:  Shared Storage for checkpoints/datasets                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. 数据模型设计

### 5.1 实体关系图

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   RLProject      │       │   RLTrainingJob  │       │   RLCheckpoint   │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │◄──────│ project_id (FK)  │       │ job_id (FK)      │
│ name             │       │ id (PK)          │◄──────┤ id (PK)          │
│ description      │       │ name             │       │ step             │
│ owner_id (FK)    │       │ status           │       │ path             │
│ base_model       │       │ algorithm        │       │ metrics          │
│ algorithm        │       │ config (JSON)    │       │ created_at       │
│ config_template  │       │ resource_spec    │       └──────────────────┘
│ created_at       │       │ started_at       │
└──────────────────┘       │ ended_at         │       ┌──────────────────┐
                           │ current_step     │       │   RLDataset      │
                           │ total_steps      │       ├──────────────────┤
                           │ metrics_summary  │◄──────│ job_id (FK)      │
                           └──────────────────┘       │ trajectory_path  │
                                                      │ reward_stats     │
                                                      └──────────────────┘
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   RewardFunction │       │   RLExperiment   │       │   ModelVersion   │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)          │
│ project_id (FK)  │◄──────│ project_id (FK)  │       │ job_id (FK)      │
│ name             │       │ name             │       │ model_id (FK)    │
│ type             │       │ hyperparams      │       │ version_tag      │
│ config (JSON)    │       │ baseline_job_id  │       │ metrics          │
│ code_path        │       │ variant_job_ids  │       │ status           │
└──────────────────┘       └──────────────────┘       └──────────────────┘
```

### 5.2 核心模型定义

#### 5.2.1 RLProject (RL 项目)

```python
class RLProject(models.Model):
    """RL 项目，对应一个强化学习任务"""
    
    # 基础信息
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, 
                                     on_delete=models.CASCADE, 
                                     null=True, blank=True)
    
    # 模型配置
    base_model = models.CharField(max_length=255)  # 如: Qwen/Qwen2.5-7B
    algorithm = models.CharField(max_length=50, choices=[
        ('ppo', 'PPO'),
        ('grpo', 'GRPO'),
        ('dpo', 'DPO'),
        ('rlvr', 'RLVR'),
    ])
    
    # 配置模板 (存储为 JSON)
    config_template = models.JSONField(default=dict)
    
    # 关联数据集
    train_dataset = models.ForeignKey(Dataset, 
                                      on_delete=models.SET_NULL,
                                      related_name='rl_train_projects',
                                      null=True)
    eval_dataset = models.ForeignKey(Dataset,
                                     on_delete=models.SET_NULL,
                                     related_name='rl_eval_projects',
                                     null=True)
    
    # 状态
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('ready', 'Ready'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='draft')
    
    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.JSONField(default=list)
```

#### 5.2.2 RLTrainingJob (训练任务)

```python
class RLTrainingJob(models.Model):
    """RL 训练任务实例"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    project = models.ForeignKey(RLProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    # 任务状态
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    
    # 详细配置 (覆盖项目模板)
    config = models.JSONField(default=dict)
    # 示例配置结构:
    # {
    #     "actor": {
    #         "learning_rate": 1e-6,
    #         "eps_clip": 0.2,
    #         "kl_ctl": 0.01,
    #         "adv_norm": "batch"
    #     },
    #     "critic": {
    #         "learning_rate": 1e-5,
    #         "ppo_n_minibatches": 4
    #     },
    #     "rollout": {
    #         "backend": "vllm",
    #         "max_concurrent_rollouts": 128,
    #         "temperature": 0.7,
    #         "max_new_tokens": 2048
    #     },
    #     "training": {
    #         "max_steps": 1000,
    #         "save_interval": 100,
    #         "eval_interval": 50
    #     },
    #     "resources": {
    #         "gpus": 8,
    #         "allocation_mode": "train:dp=8;gen:tp=4"
    #     }
    # }
    
    # 资源规格
    resource_spec = models.JSONField(default=dict)
    
    # 执行信息
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    current_step = models.IntegerField(default=0)
    total_steps = models.IntegerField(default=0)
    
    # 指标摘要
    metrics_summary = models.JSONField(default=dict)
    # {
    #     "final_reward": 0.85,
    #     "final_kl": 0.02,
    #     "best_step": 850,
    #     "training_time": "2h 30m"
    # }
    
    # 日志与输出
    log_path = models.CharField(max_length=1024, blank=True)
    output_model_path = models.CharField(max_length=1024, blank=True)
    
    # 外部任务 ID (AReaL 内部 ID)
    external_job_id = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

#### 5.2.3 RLCheckpoint (检查点)

```python
class RLCheckpoint(models.Model):
    """训练检查点"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    job = models.ForeignKey(RLTrainingJob, on_delete=models.CASCADE)
    
    step = models.IntegerField()
    path = models.CharField(max_length=1024)  # 存储路径
    
    # 检查点类型
    checkpoint_type = models.CharField(max_length=50, choices=[
        ('regular', 'Regular'),
        ('best', 'Best'),
        ('final', 'Final'),
        ('user_saved', 'User Saved'),
    ])
    
    # 存储指标
    metrics = models.JSONField(default=dict)
    # {
    #     "reward": 0.82,
    #     "kl": 0.015,
    #     "loss": 0.34,
    #     "entropy": 0.67
    # }
    
    file_size = models.BigIntegerField(default=0)  # 字节
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-step']
```

#### 5.2.4 RewardFunction (奖励函数)

```python
class RewardFunction(models.Model):
    """奖励函数定义"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    project = models.ForeignKey(RLProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # 类型
    reward_type = models.CharField(max_length=50, choices=[
        ('rule_based', 'Rule Based'),
        ('model_based', 'Model Based'),
        ('hybrid', 'Hybrid'),
        ('custom', 'Custom Python'),
    ])
    
    # 配置
    config = models.JSONField(default=dict)
    # 规则奖励示例:
    # {
    #     "rules": [
    #         {"pattern": "answer is (\\d+)", "match_group": 1, "reward": 1.0},
    #         {"contains": "incorrect", "reward": -0.5}
    #     ]
    # }
    #
    # 模型奖励示例:
    # {
    #     "model_path": "path/to/reward/model",
    #     "score_field": "score"
    # }
    
    # 自定义代码 (当 type=custom 时使用)
    code = models.TextField(blank=True)
    
    # 验证状态
    is_validated = models.BooleanField(default=False)
    validation_result = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

### 5.3 指标数据模型 (时序数据)

```python
class RLTrainingMetrics(models.Model):
    """
    训练指标时序数据
    存储在时序数据库 (如 InfluxDB) 或专门的 metrics 表中
    """
    
    job = models.ForeignKey(RLTrainingJob, on_delete=models.CASCADE)
    step = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # 训练指标
    loss = models.FloatField(null=True)
    actor_loss = models.FloatField(null=True)
    critic_loss = models.FloatField(null=True)
    
    # RL 特有指标
    mean_reward = models.FloatField(null=True)
    std_reward = models.FloatField(null=True)
    kl_divergence = models.FloatField(null=True)
    policy_entropy = models.FloatField(null=True)
    
    # 资源指标
    gpu_utilization = models.JSONField(default=dict)  # {"gpu_0": 95, "gpu_1": 92}
    memory_usage = models.JSONField(default=dict)
    
    # 生成统计
    tokens_generated = models.IntegerField(default=0)
    samples_collected = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['job', 'step']),
            models.Index(fields=['job', 'timestamp']),
        ]
```

---

## 6. API 设计

### 6.1 REST API 概览

| 资源 | 端点 | 方法 | 描述 |
|------|------|------|------|
| RL Project | `/api/v2/rl/projects` | GET/POST | 列表/创建项目 |
| RL Project | `/api/v2/rl/projects/{id}` | GET/PUT/DELETE | 项目详情/更新/删除 |
| Training Job | `/api/v2/rl/jobs` | GET/POST | 列表/提交任务 |
| Training Job | `/api/v2/rl/jobs/{id}` | GET/PUT/DELETE | 任务详情/控制/删除 |
| Job Control | `/api/v2/rl/jobs/{id}/start` | POST | 启动任务 |
| Job Control | `/api/v2/rl/jobs/{id}/stop` | POST | 停止任务 |
| Job Control | `/api/v2/rl/jobs/{id}/pause` | POST | 暂停任务 |
| Job Control | `/api/v2/rl/jobs/{id}/resume` | POST | 恢复任务 |
| Metrics | `/api/v2/rl/jobs/{id}/metrics` | GET | 获取指标数据 |
| Metrics Stream | `/api/v2/rl/jobs/{id}/metrics/stream` | WebSocket | 实时指标流 |
| Checkpoints | `/api/v2/rl/jobs/{id}/checkpoints` | GET | 检查点列表 |
| Checkpoint | `/api/v2/rl/checkpoints/{id}` | GET/POST | 详情/从检查点恢复 |
| Reward Func | `/api/v2/rl/reward-functions` | GET/POST | 奖励函数管理 |
| Evaluation | `/api/v2/rl/jobs/{id}/evaluate` | POST | 触发评估 |
| Comparison | `/api/v2/rl/compare` | POST | 对比多个任务 |

### 6.2 核心 API 详情

#### 6.2.1 创建 RL 项目

```http
POST /api/v2/rl/projects
Content-Type: application/json
Authorization: Bearer {token}

{
  "name": "Qwen2.5-7B Math RLVR",
  "description": "使用 RLVR 训练数学推理能力",
  "base_model": "Qwen/Qwen2.5-7B-Instruct",
  "algorithm": "grpo",
  "config_template": {
    "actor": {
      "learning_rate": 1e-6,
      "eps_clip": 0.2,
      "kl_ctl": 0.01
    },
    "rollout": {
      "backend": "vllm",
      "temperature": 0.7,
      "max_new_tokens": 2048,
      "n_samples": 8
    },
    "training": {
      "max_steps": 1000,
      "save_interval": 100
    }
  },
  "train_dataset_id": "dataset-uuid",
  "eval_dataset_id": "eval-dataset-uuid",
  "tags": ["math", "reasoning", "grpo"]
}
```

响应:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "proj-uuid",
    "name": "Qwen2.5-7B Math RLVR",
    "status": "draft",
    "created_at": "2026-03-04T10:00:00Z"
  }
}
```

#### 6.2.2 提交训练任务

```http
POST /api/v2/rl/jobs
Content-Type: application/json
Authorization: Bearer {token}

{
  "project_id": "proj-uuid",
  "name": "Experiment #1 - Baseline",
  "config_override": {
    "actor": {
      "learning_rate": 5e-7
    }
  },
  "resources": {
    "gpus": 8,
    "gpu_type": "A100",
    "allocation_mode": "train:dp=8;gen:tp=4"
  },
  "priority": 1
}
```

响应:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "job-uuid",
    "project_id": "proj-uuid",
    "name": "Experiment #1 - Baseline",
    "status": "pending",
    "queue_position": 3,
    "estimated_start": "2026-03-04T10:15:00Z",
    "created_at": "2026-03-04T10:00:00Z"
  }
}
```

#### 6.2.3 获取任务详情

```http
GET /api/v2/rl/jobs/{job_id}
Authorization: Bearer {token}
```

响应:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "job-uuid",
    "project": {
      "id": "proj-uuid",
      "name": "Qwen2.5-7B Math RLVR"
    },
    "name": "Experiment #1 - Baseline",
    "status": "running",
    "current_step": 450,
    "total_steps": 1000,
    "progress": 45,
    "started_at": "2026-03-04T10:15:00Z",
    "estimated_end": "2026-03-04T12:30:00Z",
    "resources": {
      "gpus": 8,
      "gpu_utilization": [92, 94, 91, 93, 95, 92, 94, 91]
    },
    "metrics_summary": {
      "mean_reward": 0.78,
      "kl_divergence": 0.018,
      "best_step": 420
    },
    "latest_metrics": {
      "step": 450,
      "loss": 0.34,
      "actor_loss": 0.21,
      "mean_reward": 0.78,
      "kl": 0.018,
      "entropy": 0.65
    }
  }
}
```

#### 6.2.4 获取训练指标

```http
GET /api/v2/rl/jobs/{job_id}/metrics?metric_types=loss,reward,kl&start_step=0&end_step=500
Authorization: Bearer {token}
```

响应:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "steps": [0, 10, 20, ..., 500],
    "metrics": {
      "loss": [1.2, 0.9, 0.7, ..., 0.34],
      "mean_reward": [0.45, 0.52, 0.58, ..., 0.78],
      "kl_divergence": [0.0, 0.005, 0.012, ..., 0.018]
    }
  }
}
```

#### 6.2.5 WebSocket 实时指标流

```javascript
// WebSocket 连接
const ws = new WebSocket(
  'wss://api.dcai.com/v2/rl/jobs/{job_id}/metrics/stream?token={jwt}'
);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // {
  //   "type": "metrics",
  //   "timestamp": "2026-03-04T10:30:00Z",
  //   "data": {
  //     "step": 451,
  //     "loss": 0.33,
  //     "mean_reward": 0.79,
  //     "kl": 0.019,
  //     "gpu_util": [93, 95, 92, 94, 96, 93, 95, 92]
  //   }
  // }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

#### 6.2.6 检查点管理

```http
GET /api/v2/rl/jobs/{job_id}/checkpoints
Authorization: Bearer {token}
```

响应:
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "checkpoints": [
      {
        "id": "ckpt-001",
        "step": 100,
        "type": "regular",
        "metrics": {
          "reward": 0.62,
          "kl": 0.008
        },
        "size": 14700000000,
        "created_at": "2026-03-04T10:45:00Z"
      },
      {
        "id": "ckpt-best",
        "step": 420,
        "type": "best",
        "metrics": {
          "reward": 0.81,
          "kl": 0.017
        },
        "size": 14700000000,
        "created_at": "2026-03-04T12:00:00Z"
      }
    ]
  }
}
```

从检查点恢复训练:
```http
POST /api/v2/rl/jobs
Content-Type: application/json
Authorization: Bearer {token}

{
  "project_id": "proj-uuid",
  "name": "Experiment #2 - From Checkpoint",
  "resume_from_checkpoint": "ckpt-uuid",
  "config_override": {
    "training": {
      "max_steps": 2000
    }
  }
}
```

### 6.3 gRPC API (内部服务通信)

```protobuf
// rl_service.proto
syntax = "proto3";
package dcai.rl;

service RLOrchestratorService {
  // 训练任务管理
  rpc SubmitJob(SubmitJobRequest) returns (SubmitJobResponse);
  rpc GetJobStatus(GetJobStatusRequest) returns (JobStatus);
  rpc CancelJob(CancelJobRequest) returns (CancelJobResponse);
  rpc StreamMetrics(StreamMetricsRequest) returns (stream MetricsBatch);
  
  // 资源管理
  rpc GetClusterStatus(GetClusterStatusRequest) returns (ClusterStatus);
  rpc AllocateResources(AllocateResourcesRequest) returns (AllocateResourcesResponse);
  
  // 检查点管理
  rpc SaveCheckpoint(SaveCheckpointRequest) returns (CheckpointInfo);
  rpc ListCheckpoints(ListCheckpointsRequest) returns (ListCheckpointsResponse);
}

message SubmitJobRequest {
  string project_id = 1;
  string job_config_json = 2;
  ResourceSpec resources = 3;
}

message JobStatus {
  string job_id = 1;
  string state = 2;  // PENDING, RUNNING, COMPLETED, FAILED
  int32 current_step = 3;
  int32 total_steps = 4;
  string error_message = 5;
  map<string, double> latest_metrics = 6;
}

message MetricsBatch {
  int64 timestamp = 1;
  int32 step = 2;
  map<string, double> scalars = 3;
  repeated SampleOutput samples = 4;
}

message SampleOutput {
  string prompt = 1;
  string completion = 2;
  double reward = 3;
}

message ResourceSpec {
  int32 num_gpus = 1;
  string gpu_type = 2;
  int32 num_nodes = 3;
  string allocation_mode = 4;
}
```

---

## 7. 核心流程设计

### 7.1 训练任务生命周期

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Training Job Lifecycle                                │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────┐
    │  DRAFT  │ ◄────────────────────────────────────────────┐
    └────┬────┘                                              │
         │ User submits job                                  │
         ▼                                                    │
    ┌─────────┐    ┌─────────┐    Validation Failed         │
    │ PENDING │───►│VALIDATE │───────────────────────────────┤
    └────┬────┘    └────┬────┘                              │
         │ Valid         │ Valid                             │
         ▼               ▼                                   │
    ┌─────────┐    ┌─────────┐                               │
    │ QUEUED  │───►│ RUNNING │                               │
    └────┬────┘    └────┬────┘                               │
         │ Queue pop      │                                   │
         │               │ User pauses                         │
         │               ▼                                   │
         │          ┌─────────┐    Resume                    │
         │          │ PAUSED  │───────────────────────────────┤
         │          └────┬────┘                              │
         │               │                                   │
         │               │ Complete/Error                    │
         │               ▼                                   │
         │          ┌─────────┐    ┌─────────┐               │
         └─────────►│COMPLETED│    │ FAILED  │───────────────┘
                    └────┬────┘    └─────────┘  (Retry)
                         │
                         ▼
                    ┌─────────┐
                    │ARCHIVED │
                    └─────────┘
```

### 7.2 分布式训练启动流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Distributed Training Launch Flow                          │
└─────────────────────────────────────────────────────────────────────────────┘

DCAI Backend                    RL Orchestrator                 AReaL Cluster
     │                               │                              │
     │  1. Submit Training Job       │                              │
     │──────────────────────────────►│                              │
     │                               │                              │
     │                               │  2. Validate Config          │
     │                               │  3. Check Resource Quota     │
     │                               │                              │
     │                               │  4. Allocate Resources       │
     │                               │──────────────────────────────►│
     │                               │                              │
     │                               │  5. Create Job in K8s/Slurm  │
     │                               │──────────────────────────────►│
     │                               │                              │
     │                               │  6. Launch AReaL Trainer     │
     │                               │                              │
     │                               │◄─────────────────────────────│
     │                               │  7. Job Started              │
     │                               │                              │
     │  8. Job Status Update         │                              │
     │◄──────────────────────────────│                              │
     │                               │                              │
     │  9. Stream Metrics (WebSocket)│                              │
     │◄══════════════════════════════│◄═════════════════════════════│
     │                               │                              │

Step Details:
1. 用户通过 API 提交训练任务
2. Orchestrator 验证配置合法性
3. 检查用户资源配额和优先级
4. 向集群调度器申请资源
5. 创建 Kubernetes Job 或 Slurm Job
6. 在每个节点启动 AReaL 训练进程
7. AReaL 进程启动后上报状态
8. DCAI 更新任务状态为 RUNNING
9. AReaL 通过消息队列实时推送指标
```

### 7.3 异步 Rollout 数据流

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Async Rollout Data Flow                                │
└─────────────────────────────────────────────────────────────────────────────┘

AReaL Trainer                    Inference Engine              Reward Function
     │                                  │                            │
     │  1. Prepare Batch                │                            │
     │  (prompts + metadata)            │                            │
     │─────────────────────────────────►│                            │
     │                                  │                            │
     │                                  │  2. Async Generate         │
     │                                  │  (vLLM/SGLang)             │
     │                                  │                            │
     │  3. Return Completions           │                            │
     │◄─────────────────────────────────│                            │
     │                                  │                            │
     │  4. Compute Rewards              │                            │
     │───────────────────────────────────────────────────────────────►│
     │                                  │                            │
     │  5. Return Rewards               │                            │
     │◄───────────────────────────────────────────────────────────────│
     │                                  │                            │
     │  6. Build Trajectory             │                            │
     │  (states, actions, rewards)      │                            │
     │                                  │                            │
     │  7. Store in Replay Buffer       │                            │
     │                                  │                            │
     │  8. PPO Update                   │                            │
     │  (actor + critic)                │                            │
     │                                  │                            │
     │  9. Sync Weights                 │                            │
     │─────────────────────────────────►│                            │
     │                                  │                            │

Data Flow Optimizations:
- 使用异步提交避免阻塞训练
- 批量生成提高 GPU 利用率
- 奖励计算并行化
- 权重更新使用 XCCL 广播
```

### 7.4 奖励函数执行流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Reward Function Execution                              │
└─────────────────────────────────────────────────────────────────────────────┘

                              Reward Function Types
                    ┌─────────────────────────────────────┐
                    │                                     │
        ┌───────────▼───────────┐  ┌───────────▼───────────┐  ┌──────────────▼────────┐
        │    Rule Based         │  │     Model Based       │  │     Custom Python     │
        │                       │  │                       │  │                       │
        │  - Regex matching     │  │  - Pretrained model   │  │  - User uploaded      │
        │  - String contains    │  │  - API calls          │  │  - Sandboxed exec     │
        │  - JSON extraction    │  │  - Embedding sim      │  │  - Predefined imports │
        └───────────┬───────────┘  └───────────┬───────────┘  └──────────────┬────────┘
                    │                          │                             │
                    └──────────────────────────┼─────────────────────────────┘
                                               │
                                               ▼
                              ┌────────────────────────────────┐
                              │    Reward Function Sandbox     │
                              │                                │
                              │  - Secure execution env        │
                              │  - Timeout control             │
                              │  - Resource limits             │
                              │  - Result caching              │
                              └───────────────┬────────────────┘
                                              │
                              ┌───────────────▼────────────────┐
                              │     Batch Reward Computation    │
                              │                                │
                              │  Input:  [prompts, completions] │
                              │  Output: [rewards]              │
                              └────────────────────────────────┘

Execution Flow:
1. Trainer 收集一批完成样本
2. 根据配置调用对应的奖励函数
3. 在沙箱中安全执行 (针对自定义代码)
4. 返回奖励值列表
5. 可选: 缓存结果避免重复计算
```

---

## 8. 基础设施与部署

### 8.1 部署架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Deployment Architecture                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              Kubernetes Cluster                             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DCAI Platform Services                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │   Django    │  │   FastAPI   │  │   Celery    │  │   Redis    │  │   │
│  │  │   Backend   │  │   Gateway   │  │   Workers   │  │   Cache    │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      RL Training Namespace                           │   │
│  │                                                                      │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │   │
│  │  │  RL Orchestrator │    │  Metrics Server │    │  Object Storage │  │   │
│  │  │   (Deployment)   │    │   (StatefulSet) │    │    (MinIO/S3)   │  │   │
│  │  └────────┬────────┘    └─────────────────┘    └─────────────────┘  │   │
│  │           │                                                          │   │
│  │           │  Creates                                                 │   │
│  │           ▼                                                          │   │
│  │  ┌────────────────────────────────────────────────────────────────┐  │   │
│  │  │                    Training Jobs (Jobs/CronJobs)                │  │   │
│  │  │                                                                 │  │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │  │   │
│  │  │  │ Train Pod 0 │  │ Train Pod 1 │  │ Train Pod N │  ...        │  │   │
│  │  │  │ (AReaL)     │  │ (AReaL)     │  │ (AReaL)     │             │  │   │
│  │  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │  │   │
│  │  │         │                │                │                     │  │   │
│  │  │         └────────────────┴────────────────┘                     │  │   │
│  │  │                      XCCL Network                               │  │   │
│  │  │                                                                 │  │   │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │  │   │
│  │  │  │ vLLM Pod 0  │  │ vLLM Pod 1  │  │ vLLM Pod N  │  ...        │  │   │
│  │  │  │ (Inference) │  │ (Inference) │  │ (Inference) │             │  │   │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘             │  │   │
│  │  │                                                                 │  │   │
│  │  └────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  │  Storage:                                                           │   │
│  │  - Shared PVC (NFS/Ceph) for checkpoints                            │   │
│  │  - ConfigMap for training configs                                   │   │
│  │  - Secret for model credentials                                     │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 资源调度策略

```python
class ResourceScheduler:
    """
    训练任务资源调度器
    """
    
    def schedule_job(self, job: RLTrainingJob) -> AllocationPlan:
        """
        为训练任务分配资源
        """
        config = job.config
        resources = config.get('resources', {})
        
        # 解析分配模式
        # e.g., "train:dp=8,tp=2;gen:tp=4" means:
        # - Training: 8-way DP + 2-way TP = 16 GPUs
        # - Generation: 4-way TP per instance
        allocation_mode = resources.get('allocation_mode', 'train:dp=8')
        
        # 计算所需 GPU 数量
        total_gpus = self._calculate_gpu_requirement(allocation_mode)
        
        # 检查集群资源
        available = self.cluster.get_available_resources()
        
        if available.gpus < total_gpus:
            # 加入队列等待
            return AllocationPlan(
                status='queued',
                queue_position=self.queue.add(job),
                estimated_wait=self._estimate_wait_time(total_gpus)
            )
        
        # 分配节点
        nodes = self._allocate_nodes(total_gpus, resources.get('gpu_type', 'A100'))
        
        return AllocationPlan(
            status='allocated',
            nodes=nodes,
            allocation_mode=allocation_mode
        )
    
    def preempt_if_needed(self, priority_job: RLTrainingJob) -> bool:
        """
        高优先级任务抢占低优先级任务资源
        """
        running_jobs = self.get_running_jobs()
        
        # 按优先级排序
        candidates = [j for j in running_jobs if j.priority < priority_job.priority]
        
        if candidates:
            # 暂停最低优先级的任务
            victim = min(candidates, key=lambda j: j.priority)
            self.pause_job(victim)
            return True
        
        return False
```

### 8.3 存储设计

| 数据类型 | 存储方案 | 保留策略 |
|----------|----------|----------|
| 训练配置 | PostgreSQL | 永久 |
| 任务元数据 | PostgreSQL | 永久 |
| 指标数据 | InfluxDB/TimescaleDB | 30天聚合 |
| 检查点 | S3/MinIO + 本地缓存 | 用户配置 |
| 日志文件 | S3/MinIO | 7天 |
| 轨迹数据 | S3/MinIO (Parquet) | 用户配置 |

---

## 9. 安全与权限

### 9.1 权限模型

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Permission Model                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Roles:
┌─────────────┬─────────────────────────────────────────────────────────────┐
│   Role      │                         Permissions                         │
├─────────────┼─────────────────────────────────────────────────────────────┤
│   Admin     │ Full access to all RL resources                             │
│   Org Admin │ Manage organization RL projects and quotas                  │
│   Researcher│ Create RL projects, submit training jobs                    │
│   Viewer    │ View projects and training results, cannot submit jobs      │
└─────────────┴─────────────────────────────────────────────────────────────┘

Resource Level Permissions:
- RLProject: read, write, admin
- RLTrainingJob: read, write, cancel, delete
- RLCheckpoint: read, write, deploy
- RewardFunction: read, write, execute

Permission Checks:
1. User can only access their own projects
2. Organization members can access org projects
3. Public projects are readable by all
4. Training job cancellation requires write permission
5. Checkpoint deployment requires deploy permission
```

### 9.2 沙箱安全

```python
class RewardFunctionSandbox:
    """
    自定义奖励函数沙箱执行环境
    """
    
    def execute(self, code: str, inputs: List[dict]) -> List[float]:
        """
        在安全环境中执行用户代码
        """
        # 1. 代码静态分析
        if not self._validate_code(code):
            raise SecurityError("Code contains forbidden operations")
        
        # 2. 创建隔离环境 (使用 gVisor 或 Kata Containers)
        container = self._create_sandbox_container()
        
        # 3. 限制资源
        container.set_limits(
            cpu_limit='1',
            memory_limit='512Mi',
            timeout=30,  # 30秒超时
            network_access=False  # 禁止网络访问
        )
        
        # 4. 执行代码
        results = []
        for inp in inputs:
            result = container.run(code, inp)
            results.append(result)
        
        # 5. 清理环境
        container.destroy()
        
        return results
    
    def _validate_code(self, code: str) -> bool:
        """静态代码检查"""
        forbidden_patterns = [
            r'import\s+os',
            r'import\s+sys',
            r'open\s*\(',
            r'__import__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'subprocess',
            r'urllib',
            r'requests',
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, code):
                return False
        
        return True
```

### 9.3 资源配额

```python
class ResourceQuotaManager:
    """
    用户资源配额管理
    """
    
    QUOTA_LIMITS = {
        'free': {
            'max_parallel_jobs': 1,
            'max_gpus_per_job': 2,
            'max_total_gpus': 2,
            'max_storage_gb': 50,
            'max_job_duration_hours': 4,
        },
        'pro': {
            'max_parallel_jobs': 5,
            'max_gpus_per_job': 8,
            'max_total_gpus': 16,
            'max_storage_gb': 500,
            'max_job_duration_hours': 24,
        },
        'enterprise': {
            'max_parallel_jobs': 20,
            'max_gpus_per_job': 64,
            'max_total_gpus': 128,
            'max_storage_gb': 5000,
            'max_job_duration_hours': 168,  # 7 days
        }
    }
    
    def check_quota(self, user: User, requested_resources: dict) -> QuotaCheck:
        """检查用户是否超出配额"""
        tier = user.subscription_tier
        limits = self.QUOTA_LIMITS[tier]
        
        current_usage = self._get_current_usage(user)
        
        # 检查各项配额
        if current_usage['parallel_jobs'] >= limits['max_parallel_jobs']:
            return QuotaCheck(passed=False, reason="Max parallel jobs exceeded")
        
        if requested_resources['gpus'] > limits['max_gpus_per_job']:
            return QuotaCheck(passed=False, reason="GPU request exceeds per-job limit")
        
        if current_usage['total_gpus'] + requested_resources['gpus'] > limits['max_total_gpus']:
            return QuotaCheck(passed=False, reason="Total GPU quota exceeded")
        
        return QuotaCheck(passed=True)
```

---

## 10. 性能与扩展性

### 10.1 性能优化策略

| 优化点 | 策略 | 预期效果 |
|--------|------|----------|
| 训练速度 | 使用 AReaL 的异步 Rollout + FSDP2 | 提升 2-3x |
| 显存优化 | 梯度检查点 + CPU Offload | 节省 40% 显存 |
| 数据加载 | 预取 + 并行数据加载 | 消除数据瓶颈 |
| 指标存储 | 批量写入 + 降采样 | 支持 10K+ 并发 |
| 检查点保存 | 异步保存 + 增量保存 | 减少 90% 阻塞时间 |

### 10.2 扩展性设计

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Horizontal Scaling                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                              Load Balancer
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
     ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
     │  DCAI API   │        │  DCAI API   │        │  DCAI API   │
     │  Server 1   │        │  Server 2   │        │  Server N   │
     └─────────────┘        └─────────────┘        └─────────────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                                   ▼
                         ┌─────────────────┐
                         │   Redis Cluster │
                         │  (Pub/Sub Queue)│
                         └────────┬────────┘
                                  │
           ┌──────────────────────┼──────────────────────┐
           │                      │                      │
           ▼                      ▼                      ▼
    ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
    │RL Orchestrator│      │RL Orchestrator│      │RL Orchestrator│
    │   Node 1    │        │   Node 2    │        │   Node N    │
    └──────┬──────┘        └──────┬──────┘        └──────┬──────┘
           │                      │                      │
           └──────────────────────┼──────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   Kubernetes Cluster    │
                    │  (Auto-scaling Training)│
                    └─────────────────────────┘

Scaling Triggers:
- API Server: CPU > 70% for 2 minutes
- RL Orchestrator: Queue depth > 100
- Training Cluster: Pending jobs > 5
```

### 10.3 监控与告警

```yaml
# 监控指标配置
monitoring:
  metrics:
    # 训练指标
    - name: rl_training_reward
      type: gauge
      labels: [job_id, project_id]
      
    - name: rl_training_kl_divergence
      type: gauge
      labels: [job_id]
      
    - name: rl_training_loss
      type: gauge
      labels: [job_id, loss_type]
      
    # 资源指标
    - name: rl_gpu_utilization
      type: gauge
      labels: [job_id, node_id, gpu_id]
      
    - name: rl_gpu_memory_used
      type: gauge
      labels: [job_id, node_id, gpu_id]
      
    # 业务指标
    - name: rl_jobs_submitted_total
      type: counter
      labels: [algorithm, status]
      
    - name: rl_job_queue_wait_seconds
      type: histogram
      labels: [algorithm]

  alerts:
    - name: HighKLDivergence
      condition: rl_training_kl_divergence > 0.1
      duration: 5m
      severity: warning
      message: "KL divergence too high for job {{ $labels.job_id }}"
      
    - name: TrainingStalled
      condition: increase(rl_training_step[10m]) == 0
      duration: 10m
      severity: critical
      message: "Training job {{ $labels.job_id }} appears stalled"
      
    - name: GPUOOM
      condition: rl_gpu_memory_used / rl_gpu_memory_total > 0.95
      duration: 2m
      severity: critical
      message: "GPU OOM risk for job {{ $labels.job_id }}"
      
    - name: LowRewardTrend
      condition: deriv(rl_training_reward[30m]) < -0.01
      duration: 30m
      severity: warning
      message: "Reward decreasing for job {{ $labels.job_id }}"
```

---

## 11. 实施路线图

### 阶段 1: MVP (8 周)
- [ ] 基础数据模型和 API
- [ ] PPO/GRPO 训练任务提交
- [ ] 基础监控指标展示
- [ ] 单节点训练支持

### 阶段 2: 核心功能 (12 周)
- [ ] 分布式训练支持
- [ ] 奖励函数管理
- [ ] WebSocket 实时指标
- [ ] 检查点管理和恢复
- [ ] 自动评估流水线

### 阶段 3: 高级功能 (10 周)
- [ ] DPO/RLVR 算法支持
- [ ] 自定义 Workflow
- [ ] 超参数自动搜索
- [ ] 多任务对比工具
- [ ] 模型 A/B 测试

### 阶段 4: 企业特性 (8 周)
- [ ] 资源配额管理
- [ ] 审计日志
- [ ] SSO 集成
- [ ] 私有化部署支持

---

## 附录

### A. 术语表

| 术语 | 解释 |
|------|------|
| PPO | Proximal Policy Optimization，近端策略优化 |
| GRPO | Group Relative Policy Optimization，组相对策略优化 |
| DPO | Direct Preference Optimization，直接偏好优化 |
| RLVR | RL with Verifiable Rewards，可验证奖励强化学习 |
| GAE | Generalized Advantage Estimation，广义优势估计 |
| KL | Kullback-Leibler divergence，KL 散度 |
| FSDP | Fully Sharded Data Parallel，全分片数据并行 |
| XCCL | Cross-Cluster Communication Library，跨集群通信库 |
| Rollout | 策略生成轨迹的过程 |
| Trajectory | 状态和动作的序列 |

### B. 参考文档

- [AReaL Architecture](../areal_architecture.md)
- [DCAI API Documentation](../api_docs.md)
- [AReaL GitHub Repository](https://github.com/inspirai/areal)
- [PPO Paper](https://arxiv.org/abs/1707.06347)
- [GRPO Paper](https://arxiv.org/abs/2402.03300)

---

*文档版本: v1.0*
*最后更新: 2026-03-04*
*作者: DCAI Platform Team*
