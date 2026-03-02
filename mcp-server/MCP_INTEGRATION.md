# MCP (Model Context Protocol) 集成指南

本文档描述如何将 MCP 服务集成到 HF-Frontend 项目中，以便 AI 助手能够访问 Dataset 和 Knowledge Base 数据。

## 什么是 MCP?

Model Context Protocol (MCP) 是一种开放协议，用于标准化 AI 模型与外部数据源和工具之间的通信。它允许 AI 助手安全地访问和操作外部系统。

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Assistant / Client                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server (mcp-server/)                 │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   Dataset Tools     │    │    Knowledge Base Tools     │ │
│  │ - list_datasets     │    │ - list_knowledge_bases      │ │
│  │ - get_dataset_detail│    │ - get_knowledge_base_detail │ │
│  │ - search_datasets   │    │ - search_knowledge_bases    │ │
│  │ - ...               │    │ - ...                       │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (backend/fastapi_app/)             │
│                    or Django Backend                        │
└─────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 安装依赖

```bash
# 进入 MCP 服务器目录
cd mcp-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或: venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`:

```env
# 后端 API 地址
BACKEND_API_URL=http://localhost:8000/api/v2

# 服务器配置
MCP_HOST=0.0.0.0
MCP_PORT=8080
```

### 3. 运行服务

```bash
# 方式 1: 独立 MCP 服务器 (SSE 模式)
python server.py --port 8080

# 方式 2: STDIO 模式
python server.py --transport stdio
```

## 使用方式

### 方式一: 独立 MCP 服务器 (推荐)

MCP 服务器作为独立进程运行，通过 HTTP SSE (Server-Sent Events) 与客户端通信。

**优点:**
- 可独立部署和扩展
- 支持多客户端连接
- 更好的性能和隔离性

**运行:**

```bash
# 终端 1: 启动 Django 后端
cd backend
python manage.py runserver 0.0.0.0:8000

# 终端 2: 启动 MCP 服务器
cd mcp-server
python server.py --port 8080
```

**连接:**

```python
from mcp import ClientSession
from mcp.client.sse import sse_client

async with sse_client("http://localhost:8080/mcp") as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # 调用工具
        result = await session.call_tool(
            "list_datasets",
            {"page": 1, "page_size": 10}
        )
        print(result)
```

### 方式二: FastAPI 集成端点

MCP 工具通过 FastAPI 的 RESTful 端点暴露。

**可用端点:**

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/v2/mcp/discovery` | GET | MCP 服务发现 |
| `/api/v2/mcp/dataset/list` | GET | 获取数据集列表 |
| `/api/v2/mcp/dataset/{id}` | GET | 获取数据集详情 |
| `/api/v2/mcp/dataset/search` | GET | 搜索数据集 |
| `/api/v2/mcp/dataset/stats` | GET | 数据集统计 |
| `/api/v2/mcp/knowledgebase/list` | GET | 获取知识库列表 |
| `/api/v2/mcp/knowledgebase/{id}` | GET | 获取知识库详情 |
| `/api/v2/mcp/knowledgebase/{id}/status` | GET | 知识库状态 |
| `/api/v2/mcp/knowledgebase/stats` | GET | 知识库统计 |

**示例:**

```bash
# 服务发现
curl http://localhost:8001/api/v2/mcp/discovery

# 获取数据集列表
curl http://localhost:8001/api/v2/mcp/dataset/list?page=1&page_size=10

# 获取知识库详情
curl http://localhost:8001/api/v2/mcp/knowledgebase/kb-medical-research
```

## 工具参考

### Dataset 工具

| 工具名 | 描述 | 主要参数 |
|--------|------|----------|
| `list_datasets` | 获取数据集列表 | `page`, `page_size`, `domain`, `task` |
| `get_dataset_detail` | 获取数据集详情 | `dataset_id` |
| `search_datasets` | 搜索数据集 | `keyword`, `page`, `page_size` |
| `get_dataset_statistics` | 获取统计信息 | - |
| `get_popular_datasets` | 获取热门数据集 | `limit` |
| `get_datasets_by_domain` | 按领域获取 | `domain` |
| `compare_datasets` | 对比数据集 | `dataset_ids` |

### Knowledge Base 工具

| 工具名 | 描述 | 主要参数 |
|--------|------|----------|
| `list_knowledge_bases` | 获取知识库列表 | `status`, `kb_type` |
| `get_knowledge_base_detail` | 获取知识库详情 | `kb_id` |
| `search_knowledge_bases` | 搜索知识库 | `keyword`, `status` |
| `get_knowledge_base_statistics` | 获取统计信息 | - |
| `get_knowledge_base_sources` | 获取数据源 | `kb_id` |
| `get_ready_knowledge_bases` | 获取就绪的知识库 | - |
| `check_knowledge_base_status` | 检查状态 | `kb_id` |
| `compare_knowledge_bases` | 对比知识库 | `kb_ids` |
| `find_knowledge_bases_by_source` | 按源查找 | `source_type`, `source_id` |
| `get_knowledge_base_document_summary` | 文档摘要 | `kb_id` |

## AI 助手集成示例

### Claude Desktop 配置

在 Claude Desktop 配置文件中添加 MCP 服务器:

```json
{
  "mcpServers": {
    "hf-frontend": {
      "command": "python",
      "args": ["/path/to/mcp-server/server.py", "--transport", "stdio"],
      "env": {
        "BACKEND_API_URL": "http://localhost:8000/api/v2"
      }
    }
  }
}
```

配置位置:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

### Cursor 配置

在 Cursor 设置中添加 MCP 服务器配置:

```json
{
  "mcpServers": {
    "hf-frontend": {
      "command": "python",
      "args": ["/path/to/mcp-server/server.py", "--transport", "stdio"],
      "env": {
        "BACKEND_API_URL": "http://localhost:8000/api/v2"
      }
    }
  }
}
```

### 自定义客户端

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_mcp():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp-server/server.py", "--transport", "stdio"],
        env={"BACKEND_API_URL": "http://localhost:8000/api/v2"}
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 列出可用工具
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # 调用数据集工具
            result = await session.call_tool(
                "list_datasets",
                arguments={"page": 1, "page_size": 5}
            )
            print(result)

asyncio.run(use_mcp())
```

## 开发指南

### 添加新工具

1. 在 `mcp-server/tools/dataset_tools.py` 或 `mcp-server/tools/knowledgebase_tools.py` 中添加:

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

2. 在 FastAPI 中添加对应端点 (可选)

### 测试

```bash
# 测试 MCP 服务器
cd mcp-server
python server.py

# 在另一个终端测试
curl http://localhost:8080/health
curl http://localhost:8080/info
```

## 故障排除

### 问题: 无法连接到后端 API

**解决:**
1. 检查 `BACKEND_API_URL` 环境变量
2. 确认 Django 后端正在运行
3. 检查网络连接

### 问题: 导入 Django 模型失败

**解决:**
1. 确保已正确设置 `DJANGO_SETTINGS_MODULE`
2. 确认 Django 项目路径在 Python 路径中

### 问题: MCP 客户端无法连接

**解决:**
1. 检查 MCP 服务器是否正在运行
2. 确认端口没有被占用
3. 查看 MCP 服务器日志

## 相关文档

- [MCP Protocol Specification](https://modelcontextprotocol.io/spec)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [项目 README](./README.md)
