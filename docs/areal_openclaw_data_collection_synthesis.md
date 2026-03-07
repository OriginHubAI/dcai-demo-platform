# AReaL 从 OpenClaw 等异构系统收集与合成 Agent 调优数据分析

AReaL 面向如 OpenClaw（及其轻量级实现 ZeroClaw）等外部智能体（Agent）系统，提供了一套强大的 **在线强化学习（Online RL）** 机制。此机制的核心在于 **无侵入式的 Proxy Gateway 代理网关架构**，使得外部系统在感知不到底层模型训练的情况下，自发地生成并提交用于调优模型的高质量轨迹数据。

以下是对 AReaL 数据收集与合成机制的详细分析：

## 1. 核心架构：代理网关（Proxy Gateway）模型

外部 Agent 系统通常通过 OpenAI Chat-Completions 或 Anthropic Messages 协议与大模型进行通信。AReaL 并没有强制这些系统直接集成训练代码，而是提供了一个符合标准的 **Proxy Gateway** 及其后端的 **Proxy Worker** 组件：

- **无侵入拦截**：Proxy Gateway 作为一个标准的 HTTP API 存在。OpenClaw 只需要将其配置的 Base URL 指向该网关，所有的 LLM 请求都在这里被拦截并代理转发给底层的推理引擎（如 SGLang 或 vLLM）。
- **实时特征记录**：当推理引擎生成文本响应时，紧贴推理引擎运行的 Proxy Worker 会在生成过程中静默收集强化学习必需的张量级数据，包括 **Prompt 的 Token IDs 和 Logprobs**、**Response 的 Token IDs 和 Logprobs**。

## 2. 数据收集的完整生命周期（Session Lifecycle）

数据的收集按“回合（Episode）”或“会话（Session）”为粒度进行打包，一个完整的周期包含如下步骤：

1. **会话开启 (`/rl/start_session`)**：
   - 外部调用该接口获取一个专属的会话 ID 和临时 API Key。
   - 网关会将该 API Key 路由固定到某一个可用的后端 Proxy Worker，保障单次回合上下文的数据连续性。
2. **多轮交互 (`/chat/completions`)**：
   - OpenClaw 使用发放的 API Key，像普通平台一样与系统持续对话进行多步骤推理与工具调用（Tool Calling）。
   - Proxy Worker 将多次 LLM 调用的记录暂存在当前的 Session 会下中。
3. **分配奖励 (`/rl/set_reward`)**：
   - 当 Agent 执行物理环境操作或得到外部系统的阶段性/最终评分后，可通过此专用 API，为当前交互分配一个评价标量（Reward，推荐在 `[-1, 1]` 区间）。
4. **会话结算与导出**：
   - 当调用 `/rl/end_session` 或使用原 API Key 触发刷新（再次调用 `start_session`）时，网关会自动结束这一个回合。
   - 会话中的所有记录将与步骤 3 中拿到的 Reward 绑定，被组装为标准化的 `InteractionWithTokenLogpReward` 结构（即包含 `input`, `output`, `logprob`, `reward` 的元组）。
   - 最后，这条轨迹数据会被正式 **导出（Export）** 进入 AReaL 的底层训练管道。

## 3. 多轮对话的数据合成策略

对于包含多步思考或执行过程的 Agent 任务，AReaL 支持在同一次 Session 中发生任意次 LLM 对话。
- **轨迹合并**：所有被截获的单次推理片段会构成一个序列。
- **奖励折算**：在此模式下配置有 `turn_discount` 参数，能够根据生成步数的先后顺序或对应关系，合理将总回合得到的标量 Reward 分摊、折算并合成到整个多轮推理轨迹上，从而支持复杂的长序列 Agent RL 任务调优。

## 4. 异步调优与飞轮闭环

累积提取出的轨迹数据不会被静态封存，而是用来驱动 **异步在线训练（Asynchronous Online Training）**：

- 流入的数据暂存在内存中的训练数据集（Train Dataset）中。
- 当积攒的数量达到 `config.train_dataset.batch_size` 阈值时，后端的 `PPOTrainer` （或其他如 GRPO 实现）将立即启动模型权重更新。
- 参数梯度更新完毕后，新的模型权重通过框架内的机制 **热更新广播** 给底层的推理引擎（Inference Engine）。

**总结：** 外部的 OpenClaw 系统在不重启、不感知的情况下，下一个请求就会被由刚才它自身产生的数据优化过的新模型接管。这种“收集 -> 评估 -> 训练更新 -> 再次交互”的无缝衔接，构成了全自动的 Agent 强化学习数据飞轮。
