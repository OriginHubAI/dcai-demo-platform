"""
MCP Server for HF-Frontend
提供 Dataset 和 Knowledge Base 的 Model Context Protocol 接口

运行方式:
    # SSE 模式 (推荐用于 Web 集成)
    python server.py
    
    # 或标准输入输出模式
    python server.py --transport stdio
    
    # 或指定端口
    python server.py --port 8080
"""
import os
import sys
import argparse
from typing import Optional

from fastmcp import FastMCP
from fastmcp.transports.sse import SSETransport

# 导入工具注册函数
from tools import register_dataset_tools, register_knowledgebase_tools

# MCP 服务器配置
MCP_SERVER_NAME = "hf-frontend-mcp"
MCP_SERVER_VERSION = "1.0.0"


def create_mcp_server() -> FastMCP:
    """
    创建并配置 MCP 服务器
    
    Returns:
        配置好的 FastMCP 实例
    """
    # 创建 MCP 服务器实例
    mcp = FastMCP(
        MCP_SERVER_NAME,
        instructions="""
        HF-Frontend MCP Server 提供对 Dataset 和 Knowledge Base 的访问能力。
        
        ## Dataset 工具
        - list_datasets: 获取数据集列表，支持分页和筛选
        - get_dataset_detail: 获取数据集详情
        - search_datasets: 搜索数据集
        - get_dataset_statistics: 获取数据集统计信息
        - get_popular_datasets: 获取热门数据集
        - get_datasets_by_domain: 按领域获取数据集
        - compare_datasets: 对比多个数据集
        
        ## Knowledge Base 工具
        - list_knowledge_bases: 获取知识库列表，支持状态筛选
        - get_knowledge_base_detail: 获取知识库详情
        - search_knowledge_bases: 搜索知识库
        - get_knowledge_base_statistics: 获取知识库统计信息
        - get_knowledge_base_sources: 获取知识库数据源
        - get_ready_knowledge_bases: 获取就绪状态的知识库
        - check_knowledge_base_status: 检查知识库状态
        - compare_knowledge_bases: 对比多个知识库
        - find_knowledge_bases_by_source: 根据数据源查找知识库
        - get_knowledge_base_document_summary: 获取知识库文档摘要
        """
    )
    
    # 注册 Dataset 工具
    register_dataset_tools(mcp)
    
    # 注册 Knowledge Base 工具
    register_knowledgebase_tools(mcp)
    
    return mcp


def run_stdio_server():
    """运行 STDIO 传输模式的 MCP 服务器"""
    mcp = create_mcp_server()
    print(f"Starting {MCP_SERVER_NAME} v{MCP_SERVER_VERSION} in STDIO mode...", file=sys.stderr)
    mcp.run(transport='stdio')


def run_sse_server(host: str = "0.0.0.0", port: int = 8080):
    """
    运行 SSE 传输模式的 MCP 服务器
    
    Args:
        host: 服务器主机地址
        port: 服务器端口
    """
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.responses import JSONResponse
    
    mcp = create_mcp_server()
    
    # 健康检查端点
    async def health_check(request):
        return JSONResponse({
            "status": "healthy",
            "service": MCP_SERVER_NAME,
            "version": MCP_SERVER_VERSION,
            "transport": "sse"
        })
    
    # MCP 信息端点
    async def mcp_info(request):
        tools = []
        for tool_name, tool_func in mcp._tools.items():
            tools.append({
                "name": tool_name,
                "description": tool_func.__doc__ or "No description available"
            })
        
        return JSONResponse({
            "name": MCP_SERVER_NAME,
            "version": MCP_SERVER_VERSION,
            "tools": tools,
            "transport": "sse",
            "endpoints": {
                "mcp": "/mcp",
                "health": "/health",
                "info": "/info"
            }
        })
    
    # 创建 SSE 传输
    sse_transport = SSETransport(mcp)
    
    # 创建 Starlette 应用
    app = Starlette(
        debug=os.getenv('DEBUG', 'false').lower() == 'true',
        routes=[
            Route("/health", health_check),
            Route("/info", mcp_info),
            Mount("/mcp", app=sse_transport.handle_post),
        ]
    )
    
    print(f"Starting {MCP_SERVER_NAME} v{MCP_SERVER_VERSION} on http://{host}:{port}", file=sys.stderr)
    print(f"  - Health check: http://{host}:{port}/health", file=sys.stderr)
    print(f"  - MCP Info:     http://{host}:{port}/info", file=sys.stderr)
    print(f"  - MCP Endpoint: http://{host}:{port}/mcp", file=sys.stderr)
    
    uvicorn.run(app, host=host, port=port)


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(
        description="HF-Frontend MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # SSE 模式 (默认)
  python server.py
  
  # SSE 模式指定端口
  python server.py --port 8080
  
  # STDIO 模式
  python server.py --transport stdio
        """
    )
    
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="sse",
        help="传输模式: stdio 或 sse (默认: sse)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="SSE 模式下服务器主机地址 (默认: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="SSE 模式下服务器端口 (默认: 8080)"
    )
    
    args = parser.parse_args()
    
    # 根据传输模式运行服务器
    if args.transport == "stdio":
        run_stdio_server()
    else:
        run_sse_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
