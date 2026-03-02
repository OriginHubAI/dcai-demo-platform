"""
Standalone FastAPI Application with MCP Support
Run with: uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload
"""
import os
import sys
from typing import Dict, Any, Optional

# Add parent directory to path to import Django models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from fastapi import FastAPI, Depends, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List

# Import Django models after setup
from agent.models import Agent
from task.models import Task

app = FastAPI(
    title="FastAPI Backend with MCP",
    description="High-performance API endpoints migrated from Django with MCP (Model Context Protocol) support",
    version="2.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Pydantic Schemas ==============

class AgentSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: int
    title: str
    status: str
    
    class Config:
        from_attributes = True


# ============== MCP Pydantic Schemas ==============

class MCPToolInfo(BaseModel):
    """MCP 工具信息"""
    name: str = Field(..., description="工具名称")
    description: str = Field(..., description="工具描述")
    category: str = Field(..., description="工具类别 (dataset/knowledgebase)")


class MCPDiscoveryResponse(BaseModel):
    """MCP 发现响应"""
    server_name: str = Field("hf-frontend-mcp", description="MCP 服务器名称")
    version: str = Field("1.0.0", description="MCP 服务器版本")
    tools: List[MCPToolInfo] = Field(..., description="可用工具列表")
    endpoints: Dict[str, str] = Field(..., description="API 端点")


class DatasetListParams(BaseModel):
    """数据集列表参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    domain: Optional[str] = Field(None, description="领域筛选")
    task: Optional[str] = Field(None, description="任务类型筛选")


class DatasetSearchParams(BaseModel):
    """数据集搜索参数"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class DatasetCompareParams(BaseModel):
    """数据集对比参数"""
    dataset_ids: List[str] = Field(..., min_items=2, max_items=10, description="数据集 ID 列表")


class KnowledgeBaseListParams(BaseModel):
    """知识库列表参数"""
    status: Optional[str] = Field(None, description="状态筛选 (ready, processing, syncing, error)")
    kb_type: Optional[str] = Field(None, description="类型筛选 (academic, research, general)")


class KnowledgeBaseSearchParams(BaseModel):
    """知识库搜索参数"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    status: Optional[str] = Field(None, description="状态筛选")


class KnowledgeBaseCompareParams(BaseModel):
    """知识库对比参数"""
    kb_ids: List[str] = Field(..., min_items=2, max_items=10, description="知识库 ID 列表")


# ============== Agent Endpoints ==============

@app.get("/api/v2/agents", response_model=List[AgentSchema])
async def list_agents():
    """List all agents"""
    agents = Agent.objects.all()
    return list(agents)


@app.get("/api/v2/agents/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: int):
    """Get a specific agent"""
    try:
        agent = Agent.objects.get(id=agent_id)
        return agent
    except Agent.DoesNotExist:
        raise HTTPException(status_code=404, detail="Agent not found")


# ============== Task Endpoints ==============

@app.get("/api/v2/tasks", response_model=List[TaskSchema])
async def list_tasks():
    """List all tasks"""
    tasks = Task.objects.all()
    return list(tasks)


@app.get("/api/v2/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int):
    """Get a specific task"""
    try:
        task = Task.objects.get(id=task_id)
        return task
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")


# ============== MCP Discovery Endpoint ==============

@app.get("/api/v2/mcp/discovery", response_model=MCPDiscoveryResponse)
async def mcp_discovery():
    """
    MCP 服务发现端点
    返回 MCP 服务器信息和可用工具列表
    """
    return MCPDiscoveryResponse(
        server_name="hf-frontend-mcp",
        version="1.0.0",
        tools=[
            # Dataset Tools
            MCPToolInfo(name="list_datasets", description="获取数据集列表，支持分页和筛选", category="dataset"),
            MCPToolInfo(name="get_dataset_detail", description="获取数据集详情", category="dataset"),
            MCPToolInfo(name="search_datasets", description="搜索数据集", category="dataset"),
            MCPToolInfo(name="get_dataset_statistics", description="获取数据集统计信息", category="dataset"),
            MCPToolInfo(name="get_popular_datasets", description="获取热门数据集", category="dataset"),
            MCPToolInfo(name="get_datasets_by_domain", description="按领域获取数据集", category="dataset"),
            MCPToolInfo(name="compare_datasets", description="对比多个数据集", category="dataset"),
            # Knowledge Base Tools
            MCPToolInfo(name="list_knowledge_bases", description="获取知识库列表，支持状态筛选", category="knowledgebase"),
            MCPToolInfo(name="get_knowledge_base_detail", description="获取知识库详情", category="knowledgebase"),
            MCPToolInfo(name="search_knowledge_bases", description="搜索知识库", category="knowledgebase"),
            MCPToolInfo(name="get_knowledge_base_statistics", description="获取知识库统计信息", category="knowledgebase"),
            MCPToolInfo(name="get_knowledge_base_sources", description="获取知识库数据源", category="knowledgebase"),
            MCPToolInfo(name="get_ready_knowledge_bases", description="获取就绪状态的知识库", category="knowledgebase"),
            MCPToolInfo(name="check_knowledge_base_status", description="检查知识库状态", category="knowledgebase"),
            MCPToolInfo(name="compare_knowledge_bases", description="对比多个知识库", category="knowledgebase"),
            MCPToolInfo(name="find_knowledge_bases_by_source", description="根据数据源查找知识库", category="knowledgebase"),
            MCPToolInfo(name="get_knowledge_base_document_summary", description="获取知识库文档摘要", category="knowledgebase"),
        ],
        endpoints={
            "discovery": "/api/v2/mcp/discovery",
            "invoke": "/api/v2/mcp/invoke",
            "dataset_tools": "/api/v2/mcp/dataset",
            "knowledgebase_tools": "/api/v2/mcp/knowledgebase"
        }
    )


@app.post("/api/v2/mcp/invoke")
async def mcp_invoke(tool_name: str, params: Dict[str, Any] = Body(...)):
    """
    MCP 工具调用端点 (简化版)
    用于直接调用 MCP 工具
    """
    # 这里可以实现 MCP 工具的路由逻辑
    return {
        "success": False,
        "error": f"Tool '{tool_name}' not implemented in FastAPI. Use standalone MCP server at /mcp-server/"
    }


# ============== MCP Dataset Tools Endpoints ==============

@app.get("/api/v2/mcp/dataset/list")
async def mcp_dataset_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    domain: Optional[str] = None,
    task: Optional[str] = None
):
    """
    MCP Dataset: 获取数据集列表
    """
    import httpx
    async with httpx.AsyncClient() as client:
        params = {"page": page, "page_size": page_size}
        if domain:
            params["domain"] = domain
        if task:
            params["task"] = task
        
        response = await client.get(
            "http://localhost:8000/api/v2/datasets",
            params=params,
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            result = data.get("data", {})
            return {
                "success": True,
                "total": result.get("total", 0),
                "page": result.get("page", page),
                "page_size": result.get("page_size", page_size),
                "datasets": result.get("list", [])
            }
        return {"success": False, "error": data.get("msg", "Unknown error")}


@app.get("/api/v2/mcp/dataset/{dataset_id}")
async def mcp_dataset_detail(dataset_id: str):
    """
    MCP Dataset: 获取数据集详情
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/v2/datasets/{dataset_id}",
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            return {"success": True, "dataset": data.get("data", {})}
        return {"success": False, "error": data.get("msg", "Dataset not found")}


@app.get("/api/v2/mcp/dataset/search")
async def mcp_dataset_search(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    MCP Dataset: 搜索数据集
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v2/datasets",
            params={"page": 1, "page_size": 1000},
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            all_datasets = data.get("data", {}).get("list", [])
            keyword_lower = keyword.lower()
            
            filtered = [
                d for d in all_datasets
                if keyword_lower in d.get("name", "").lower()
                or keyword_lower in d.get("description", "").lower()
            ]
            
            start = (page - 1) * page_size
            end = start + page_size
            
            return {
                "success": True,
                "total": len(filtered),
                "page": page,
                "page_size": page_size,
                "datasets": filtered[start:end]
            }
        return {"success": False, "error": data.get("msg", "Search failed")}


@app.get("/api/v2/mcp/dataset/stats")
async def mcp_dataset_statistics():
    """
    MCP Dataset: 获取数据集统计信息
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v2/datasets",
            params={"page": 1, "page_size": 1000},
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            datasets = data.get("data", {}).get("list", [])
            
            total_downloads = sum(d.get("downloads", 0) for d in datasets)
            total_likes = sum(d.get("likes", 0) for d in datasets)
            
            domain_stats = {}
            for d in datasets:
                dom = d.get("domain", "unknown")
                if dom not in domain_stats:
                    domain_stats[dom] = {"count": 0, "downloads": 0, "likes": 0}
                domain_stats[dom]["count"] += 1
                domain_stats[dom]["downloads"] += d.get("downloads", 0)
                domain_stats[dom]["likes"] += d.get("likes", 0)
            
            task_stats = {}
            for d in datasets:
                t = d.get("task", "unknown")
                if t not in task_stats:
                    task_stats[t] = {"count": 0}
                task_stats[t]["count"] += 1
            
            return {
                "success": True,
                "statistics": {
                    "total_datasets": len(datasets),
                    "total_downloads": total_downloads,
                    "total_likes": total_likes,
                    "domains": [{"name": k, **v} for k, v in domain_stats.items()],
                    "tasks": [{"name": k, **v} for k, v in task_stats.items()]
                }
            }
        return {"success": False, "error": data.get("msg", "Failed to get statistics")}


# ============== MCP Knowledge Base Tools Endpoints ==============

@app.get("/api/v2/mcp/knowledgebase/list")
async def mcp_knowledgebase_list(
    status: Optional[str] = None,
    kb_type: Optional[str] = None
):
    """
    MCP Knowledge Base: 获取知识库列表
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v2/knowledgebase",
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            kbs = data.get("data", {}).get("list", [])
            
            if status:
                kbs = [kb for kb in kbs if kb.get("status") == status]
            if kb_type:
                kbs = [kb for kb in kbs if kb.get("type") == kb_type]
            
            return {
                "success": True,
                "total": len(kbs),
                "knowledge_bases": kbs
            }
        return {"success": False, "error": data.get("msg", "Failed to fetch knowledge bases")}


@app.get("/api/v2/mcp/knowledgebase/{kb_id}")
async def mcp_knowledgebase_detail(kb_id: str):
    """
    MCP Knowledge Base: 获取知识库详情
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/v2/knowledgebase/{kb_id}",
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            kb = data.get("data", {})
            return {
                "success": True,
                "knowledge_base": {
                    "id": kb.get("id"),
                    "name": kb.get("name"),
                    "description": kb.get("description"),
                    "author": kb.get("author"),
                    "status": kb.get("status"),
                    "type": kb.get("type"),
                    "lastModified": kb.get("lastModified"),
                    "vectorStore": kb.get("vectorStore", {}),
                    "documents": kb.get("documents", {}),
                    "sources": kb.get("sources", [])
                }
            }
        return {"success": False, "error": data.get("msg", "Knowledge base not found")}


@app.get("/api/v2/mcp/knowledgebase/{kb_id}/status")
async def mcp_knowledgebase_status(kb_id: str):
    """
    MCP Knowledge Base: 检查知识库状态
    """
    result = await mcp_knowledgebase_detail(kb_id)
    
    if result.get("success"):
        kb = result.get("knowledge_base", {})
        status = kb.get("status")
        
        status_descriptions = {
            "ready": "知识库已就绪，可以正常使用",
            "processing": "知识库正在处理中，请稍后再试",
            "syncing": "知识库正在同步中，部分功能可能不可用",
            "error": "知识库处理出错，需要检查配置"
        }
        
        return {
            "success": True,
            "status_info": {
                "kb_id": kb_id,
                "name": kb.get("name"),
                "status": status,
                "is_ready": status == "ready",
                "is_processing": status == "processing",
                "is_syncing": status == "syncing",
                "has_error": status == "error",
                "status_description": status_descriptions.get(status, "未知状态"),
                "document_stats": kb.get("documents", {}),
                "vector_count": kb.get("vectorStore", {}).get("vectorCount", 0)
            }
        }
    return result


@app.get("/api/v2/mcp/knowledgebase/stats")
async def mcp_knowledgebase_statistics():
    """
    MCP Knowledge Base: 获取知识库统计信息
    """
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v2/knowledgebase",
            timeout=30.0
        )
        data = response.json()
        
        if data.get("code") == 0:
            kbs = data.get("data", {}).get("list", [])
            
            total_vectors = sum(kb.get("vectorStore", {}).get("vectorCount", 0) for kb in kbs)
            total_docs = sum(kb.get("documents", {}).get("total", 0) for kb in kbs)
            
            status_stats = {}
            type_stats = {}
            for kb in kbs:
                s = kb.get("status", "unknown")
                t = kb.get("type", "unknown")
                status_stats[s] = status_stats.get(s, 0) + 1
                type_stats[t] = type_stats.get(t, 0) + 1
            
            return {
                "success": True,
                "statistics": {
                    "total_knowledge_bases": len(kbs),
                    "total_vectors": total_vectors,
                    "total_documents": total_docs,
                    "by_status": status_stats,
                    "by_type": type_stats
                }
            }
        return {"success": False, "error": data.get("msg", "Failed to get statistics")}


# ============== Health Check ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "fastapi",
        "version": "2.1.0",
        "features": ["mcp", "dataset", "knowledgebase"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
