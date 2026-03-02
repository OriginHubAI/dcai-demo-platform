# DCAI-Platform MCP Server

DCAI Platform 项目的 Model Context Protocol (MCP) 服务器实现，为 Dataset 和 Knowledge Base 提供标准化的 AI 工具接口。

## 功能特性

### Dataset 工具
- **list_datasets** - 获取数据集列表，支持分页和筛选
- **get_dataset_detail** - 获取数据集详情
- **search_datasets** - 搜索数据集
- **get_dataset_statistics** - 获取数据集统计信息
- **get_popular_datasets** - 获取热门数据集
- **get_datasets_by_domain** - 按领域获取数据集
- **compare_datasets** - 对比多个数据集

### Knowledge Base 工具
- **list_knowledge_bases** - 获取知识库列表，支持状态筛选
- **get_knowledge_base_detail** - 获取知识库详情
- **search_knowledge_bases** - 搜索知识库
- **get_knowledge_base_statistics** - 获取知识库统计信息
- **get_knowledge_base_sources** - 获取知识库数据源
- **get_ready_knowledge_bases** - 获取就绪状态的知识库
- **check_knowledge_base_status** - 检查知识库状态
- **compare_knowledge_bases** - 对比多个知识库
- **find_knowledge_bases_by_source** - 根据数据源查找知识库
- **get_knowledge_base_document_summary** - 获取知识库文档摘要

## 安装

```bash
cd mcp-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 配置

复制环境变量示例文件并修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 后端 API 地址
BACKEND_API_URL=http://localhost:8000/api/v2

# 服务器配置
MCP_HOST=0.0.0.0
MCP_PORT=8080

# 调试模式
DEBUG=false
```

## 运行

### SSE 模式 (推荐用于 Web 集成)

```bash
# 默认端口 8080
python server.py

# 指定端口
python server.py --port 8080

# 指定主机
python server.py --host 0.0.0.0 --port 8080
```

### STDIO 模式

```bash
python server.py --transport stdio
```

## 端点

SSE 模式下可用的 HTTP 端点：

- `GET /health` - 健康检查
- `GET /info` - MCP 服务器信息和工具列表
- `POST /mcp` - MCP 消息端点

## 使用示例

### 连接到 MCP 服务器

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# STDIO 模式连接
server_params = StdioServerParameters(
    command="python",
    args=["server.py", "--transport", "stdio"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # 调用工具
        result = await session.call_tool(
            "list_datasets",
            {"page": 1, "page_size": 10}
        )
        print(result)
```

### SSE 模式连接

```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client("http://localhost:8080/mcp") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # 调用工具
        result = await session.call_tool(
            "get_knowledge_base_detail",
            {"kb_id": "kb-medical-research"}
        )
        print(result)
```

## 项目结构

```
mcp-server/
├── server.py                   # MCP 服务器主入口
├── requirements.txt            # Python 依赖
├── .env.example               # 环境变量示例
├── README.md                  # 本文档
└── tools/
    ├── __init__.py            # 工具包初始化
    ├── dataset_tools.py       # Dataset MCP 工具
    └── knowledgebase_tools.py # Knowledge Base MCP 工具
```

## 与现有 FastAPI 集成

MCP 服务器可以独立运行，也可以集成到现有的 FastAPI 应用中。

### 独立运行

```bash
# 终端 1: 启动后端 API
cd backend
python manage.py runserver 0.0.0.0:8000

# 终端 2: 启动 MCP 服务器
cd mcp-server
python server.py --port 8080
```

### 作为 FastAPI 子应用

```python
# backend/fastapi_app/main.py
from mcp_server.server import create_mcp_server
from fastmcp.integrations.fastapi import mount_mcp_server

# 挂载 MCP 服务器到 /mcp 路径
mount_mcp_server(app, create_mcp_server(), prefix="/mcp")
```

## API 参考

### Dataset 工具详情

#### list_datasets
获取数据集列表

**参数：**
- `page` (int): 页码，从 1 开始，默认 1
- `page_size` (int): 每页数量，默认 20
- `domain` (str, optional): 领域筛选
- `task` (str, optional): 任务类型筛选

**返回：**
```json
{
  "success": true,
  "total": 100,
  "page": 1,
  "page_size": 20,
  "datasets": [...]
}
```

#### get_dataset_detail
获取数据集详情

**参数：**
- `dataset_id` (str): 数据集 ID

**返回：**
```json
{
  "success": true,
  "dataset": {...}
}
```

#### search_datasets
搜索数据集

**参数：**
- `keyword` (str): 搜索关键词
- `page` (int): 页码，默认 1
- `page_size` (int): 每页数量，默认 20

**返回：**
```json
{
  "success": true,
  "total": 10,
  "page": 1,
  "page_size": 20,
  "datasets": [...]
}
```

#### get_dataset_statistics
获取数据集统计信息

**返回：**
```json
{
  "success": true,
  "statistics": {
    "total_datasets": 100,
    "total_downloads": 5000000,
    "total_likes": 10000,
    "domains": [...],
    "tasks": [...]
  }
}
```

### Knowledge Base 工具详情

#### list_knowledge_bases
获取知识库列表

**参数：**
- `status` (str, optional): 状态筛选 (ready, processing, syncing, error)
- `kb_type` (str, optional): 类型筛选 (academic, research, general)

**返回：**
```json
{
  "success": true,
  "total": 10,
  "knowledge_bases": [...]
}
```

#### get_knowledge_base_detail
获取知识库详情

**参数：**
- `kb_id` (str): 知识库 ID

**返回：**
```json
{
  "success": true,
  "knowledge_base": {
    "id": "kb-medical-research",
    "name": "Medical Research Papers",
    "description": "...",
    "status": "ready",
    "vectorStore": {...},
    "documents": {...},
    "sources": [...]
  }
}
```

#### check_knowledge_base_status
检查知识库状态

**参数：**
- `kb_id` (str): 知识库 ID

**返回：**
```json
{
  "success": true,
  "status_info": {
    "kb_id": "kb-medical-research",
    "status": "ready",
    "is_ready": true,
    "status_description": "知识库已就绪，可以正常使用"
  }
}
```

#### get_knowledge_base_statistics
获取知识库统计信息

**返回：**
```json
{
  "success": true,
  "statistics": {
    "total_knowledge_bases": 5,
    "total_vectors": 647000,
    "total_documents": 46700,
    "by_status": {...},
    "by_type": {...}
  }
}
```

## 开发指南

### 添加新工具

1. 在 `tools/dataset_tools.py` 或 `tools/knowledgebase_tools.py` 中添加工具函数
2. 使用 `@mcp.tool()` 装饰器注册工具
3. 添加类型提示和文档字符串

示例：

```python
@mcp.tool()
async def my_new_tool(param: str) -> Dict[str, Any]:
    """
    工具描述
    
    Args:
        param: 参数描述
        
    Returns:
        返回结果描述
    """
    # 实现逻辑
    return {"success": True, "data": ...}
```

### 测试

```bash
# 运行服务器
cd mcp-server
python server.py

# 测试端点
curl http://localhost:8080/health
curl http://localhost:8080/info
```

## 许可证

MIT License
