# AgentFlow 框架各 Agent 算法 Pipeline 详细分析总结

AgentFlow 是一个通用的智能体框架，在 `examples` 目录下提供了 5 种不同场景的 Agent 实现：**DSAgent**、**DocDancer**、**RAGAgent**、**Text2SQL** 和 **WebAgent**。

通过对这五种 Agent 的分析可以发现，它们都在底层复用了**相似的核心算法与数据处理流水线**，其主要区别在于**交互工具（Tools）**和**探索所依赖的数据后端（Sandbox Backends）**的不同。

---

## 🚀 一、 核心通用 Pipeline (Universal Pipeline)

所有 Agent 的主要任务流都遵循一个高度统一的核心范式，即：

```
Seed (种子数据) 
   → Trajectory Tree Sampling (轨迹树采样 / TrajectorySampler)
   → Trajectory Selection (轨迹选择 / TrajectorySelector)
   → QA Synthesis (问答合成 / QASynthesizer)
   → 输出 QA 对 (synthesized_qa.jsonl) 与 轨迹数据 (trajectories.jsonl)
```

**通用五步工作流：**
1. **Sandbox Setup (沙箱环境配置):** 启动包含各种外部工具或知识库的沙箱服务端（Sandbox Server）。
2. **QA Synthesis (问答合成):** 使用 `synthesize` 工具基于大模型（LLM）探索沙箱环境，自动生成（复杂的、需要进行多跳推理的）QA 数据对。
3. **Trajectory Rollout (轨迹生成):** 使用在预定基准测试集上生成完整的多智能体探索轨迹（Trajectory data），用于后续监督微调（SFT）或模仿学习。
4. **Model Training & Deployment (模型训练与部署):** 经微调模型后，利用 `vLLM` 部署提供兼容 OpenAI API 的推理服务。
5. **Inference & Evaluation (推理与评估):** 利用部署的微调后模型回答评测基准上的数据，生成推理结果并进行自动评估。

---

## 🤖 二、 各 Agent 算法 Pipeline 详情

### 1. 📊 DSAgent (CSV / Table Data Agent)
*专注数据科学与表格分析（无模型微调示例）*

- **业务场景：** 本地 CSV 目录数据的预读、摘要扫描以及在安全沙箱环境中执行 Python 代码。
- **Pipeline 路线：** `Sandbox Setup` → `QA Synthesis (+ Trajectories)`
- **Agent 工具箱：**
  - `ds_inspect_data`: 扫描给定的文件目录，提供 CSV 的数据表结构信息以及缺失值等概览。
  - `ds_read_csv`: 读取和预览具体的 CSV 数据的前 N 行。
  - `ds_run_python`: 在沙箱中执行自定义的 Python 分析脚本（例如 pandas, sklearn）。
- **种子数据 (Seed)：** 指向包含 CSV 文件的目录路径。

### 2. 💃 DocDancer (Doc QA Agent)
*专注针对文档的多跳推理阅读理解及信息提取（VLM + LLM协同）*

- **业务场景：** 利用搜索和基于视觉语言模型（VLM）的多页、跨模态阅读，完成深度文档问答任务。
- **Pipeline 路线：** 完整的 `Sandbox Setup` → `QA Synthesis` → `Trajectory Rollout` → `Model Training` → `Inference & Evaluation`
- **Agent 工具箱：**
  - `doc_search`: 在预先处理的文档的标题、段落、表格、图表说明中搜索关键词。
  - `doc_read`: 阅读并提取具体的文档章节内容，采用视觉大模型（VLM）处理图文结构。
- **种子数据 (Seed)：** 给定预处理的文档（包含生成的文档目录 `outline.xml` 表和 PDF 资源路径）。

### 3. 📚 RAGAgent (Knowledge-Base Grounded Agent)
*基于本地知识库支持的问答智能体*

- **业务场景：** 获取特定的知识库检索块（结合 DenseE5 向量化检索与 FAISS 索引），通过大规模的文本检索作答。
- **Pipeline 路线：** 完整的 5 阶段工作流。
- **Agent 工具箱：**
  - `rag_search` / `rag:search`: 对大规模语料（如 Wiki 数据集）进行相似度检索，获取相关上下文块。
- **种子数据 (Seed)：** 单个实体或初始主题相关的描述（例如："Python programming language"）。

### 4. 🗄️ Text2SQL (SQL Query Generation Agent)
*基于关系型数据库的 SQL Agent*

- **业务场景：** 对接多种 SQLite 数据库样例，通过多跳查询探索结构、外键以及验证和生成复杂的执行 SQL。
- **Pipeline 路线：** 需要额外初始化的 5 阶段工作流，即 `Database Setup` → `Sandbox Setup` → `QA Synthesis` → `Model Training` → `Inference & Evaluation`。
- **Agent 工具箱：**
  - `sql:list_databases`: 列出可用查询的所有数据库。
  - `sql:get_schema`: 探索指定的数据库或者表结构（列名，外键），以支撑后续关联查询组装。
  - `sql:execute`: 将拼接好的 SQL 发往沙箱执行验证并拿回返回集结果。
- **种子数据 (Seed)：** 目标探索数据库的名字（如 "chinook", "sakila" 数据库）。

### 5. 🖱️ WebAgent (Deep Research Agent)
*深度的 Web 研究与网页抓取智能体*

- **业务场景：** 利用实际搜索引擎和爬虫提取网页数据，针对复杂的外部网络问题进行推理和阅读理解。
- **Pipeline 路线：** 完整的 5 阶段工作流。
- **Agent 工具箱：**
  - `web_search`: 使用 Serper 接入 Google Search 等引擎的实时网页搜索结果。
  - `web_visit`: 使用 Jina 进行网页拉取、深度访问并借助 LLM 将内容转化为便于分析的文本摘要。
- **种子数据 (Seed)：** 一些具体要开展搜索的研究主题（例如 "Machine learning", "Deep learning frameworks"）。

---

## 💡 总结与启发

1. **核心逻辑的泛化性：** 即使 5 个智能体的目标对象截然不同（CSV、长文档、RAG语料、SQL数据库、Web互联网），AgentFlow 通过高度抽象的 **TrajectorySampler → TrajectorySelector → QASynthesizer** 管线，让所有生成流程收敛于同一个逻辑闭环之下。只有 Sandbox 后端和具体的 Prompt/Tips 表现出了多样性。
2. **闭环的数据飞轮设计：** 这些 examples 的示例完美展示了一种基于规则（例如：验证生成的 SQL 能跑通、要求生成跨页搜索的 QA）使用强大 LLM “自主游荡于沙箱获取经验轨迹（Trajectories）” 并 “提纯生成高质量数据集以供更小模型训练（QA Synthesis）”的范式。
3. **安全与模块化：** 利用 Sandbox Server 提供独立端口的 API 工具访问服务，有效把智能体所需要的各种第三方 API 调用与代码执行危险（比如通过 `ds_run_python` 和 `sql:execute`）隔绝开，这为训练数据集合成提供了安全保障。
