"""
Dataset MCP Tools
提供数据集相关的 MCP 工具接口
"""
import os
import sys
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# 添加后端路径以导入 Django 模型
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

import httpx
from fastmcp import FastMCP

# 后端 API 基础 URL
BACKEND_API_URL = os.getenv('BACKEND_API_URL', 'http://localhost:8000/api/v2')


# ============ Pydantic Models ============

class DatasetInfo(BaseModel):
    """数据集信息模型"""
    id: str = Field(..., description="数据集唯一标识符")
    name: str = Field(..., description="数据集名称")
    author: str = Field(..., description="数据集作者")
    description: str = Field(..., description="数据集描述")
    task: str = Field(..., description="任务类型")
    domain: str = Field(..., description="领域")
    downloads: int = Field(..., description="下载次数")
    likes: int = Field(..., description="点赞数")
    lastModified: str = Field(..., description="最后修改时间")
    rows: int = Field(..., description="数据行数")
    size: str = Field(..., description="数据集大小")
    modality: str = Field(..., description="数据模态")
    language: str = Field(..., description="语言")
    license: str = Field(..., description="许可证")


class DatasetListRequest(BaseModel):
    """数据集列表请求模型"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    domain: Optional[str] = Field(None, description="领域筛选")
    task: Optional[str] = Field(None, description="任务类型筛选")


class DatasetListResponse(BaseModel):
    """数据集列表响应模型"""
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    datasets: List[DatasetInfo] = Field(..., description="数据集列表")


class DatasetDetailRequest(BaseModel):
    """数据集详情请求模型"""
    dataset_id: str = Field(..., description="数据集 ID")


class DatasetSearchRequest(BaseModel):
    """数据集搜索请求模型"""
    keyword: str = Field(..., min_length=1, description="搜索关键词")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")


class DatasetStatistics(BaseModel):
    """数据集统计信息"""
    total_datasets: int = Field(..., description="总数据集数量")
    total_downloads: int = Field(..., description="总下载次数")
    total_likes: int = Field(..., description="总点赞数")
    domains: List[Dict[str, Any]] = Field(..., description="各领域统计")
    tasks: List[Dict[str, Any]] = Field(..., description="各任务类型统计")


# ============ MCP Tools ============

def register_dataset_tools(mcp: FastMCP):
    """注册 Dataset 相关的 MCP 工具"""
    
    @mcp.tool()
    async def list_datasets(
        page: int = 1,
        page_size: int = 20,
        domain: Optional[str] = None,
        task: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取数据集列表
        
        Args:
            page: 页码，从 1 开始
            page_size: 每页数量，默认 20
            domain: 领域筛选（可选）
            task: 任务类型筛选（可选）
            
        Returns:
            包含数据集列表和分页信息的字典
        """
        async with httpx.AsyncClient() as client:
            params = {
                'page': page,
                'page_size': page_size
            }
            if domain:
                params['domain'] = domain
            if task:
                params['task'] = task
                
            response = await client.get(
                f"{BACKEND_API_URL}/datasets",
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                result = data.get('data', {})
                return {
                    'success': True,
                    'total': result.get('total', 0),
                    'page': result.get('page', page),
                    'page_size': result.get('page_size', page_size),
                    'datasets': result.get('list', [])
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Unknown error'),
                    'datasets': [],
                    'total': 0
                }
    
    @mcp.tool()
    async def get_dataset_detail(dataset_id: str) -> Dict[str, Any]:
        """
        获取数据集详情
        
        Args:
            dataset_id: 数据集唯一标识符
            
        Returns:
            数据集详细信息
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/datasets/{dataset_id}",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                return {
                    'success': True,
                    'dataset': data.get('data', {})
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Dataset not found')
                }
    
    @mcp.tool()
    async def search_datasets(
        keyword: str,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        搜索数据集
        
        Args:
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量
            
        Returns:
            搜索结果列表
        """
        # 获取所有数据集后进行本地搜索
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/datasets",
                params={'page': 1, 'page_size': 1000},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                all_datasets = data.get('data', {}).get('list', [])
                keyword_lower = keyword.lower()
                
                # 在名称和描述中搜索
                filtered = [
                    d for d in all_datasets
                    if keyword_lower in d.get('name', '').lower()
                    or keyword_lower in d.get('description', '').lower()
                    or keyword_lower in d.get('author', '').lower()
                    or keyword_lower in d.get('domain', '').lower()
                ]
                
                # 分页
                start = (page - 1) * page_size
                end = start + page_size
                paged_results = filtered[start:end]
                
                return {
                    'success': True,
                    'total': len(filtered),
                    'page': page,
                    'page_size': page_size,
                    'datasets': paged_results
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Search failed'),
                    'datasets': []
                }
    
    @mcp.tool()
    async def get_dataset_statistics() -> Dict[str, Any]:
        """
        获取数据集统计信息
        
        Returns:
            数据集统计概览
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/datasets",
                params={'page': 1, 'page_size': 1000},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                datasets = data.get('data', {}).get('list', [])
                
                # 计算统计信息
                total_downloads = sum(d.get('downloads', 0) for d in datasets)
                total_likes = sum(d.get('likes', 0) for d in datasets)
                
                # 按领域统计
                domain_stats = {}
                for d in datasets:
                    domain = d.get('domain', 'unknown')
                    if domain not in domain_stats:
                        domain_stats[domain] = {'count': 0, 'downloads': 0, 'likes': 0}
                    domain_stats[domain]['count'] += 1
                    domain_stats[domain]['downloads'] += d.get('downloads', 0)
                    domain_stats[domain]['likes'] += d.get('likes', 0)
                
                # 按任务类型统计
                task_stats = {}
                for d in datasets:
                    task = d.get('task', 'unknown')
                    if task not in task_stats:
                        task_stats[task] = {'count': 0}
                    task_stats[task]['count'] += 1
                
                return {
                    'success': True,
                    'statistics': {
                        'total_datasets': len(datasets),
                        'total_downloads': total_downloads,
                        'total_likes': total_likes,
                        'domains': [
                            {'name': k, **v} for k, v in domain_stats.items()
                        ],
                        'tasks': [
                            {'name': k, **v} for k, v in task_stats.items()
                        ]
                    }
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Failed to get statistics')
                }
    
    @mcp.tool()
    async def get_popular_datasets(limit: int = 5) -> Dict[str, Any]:
        """
        获取热门数据集（按下载量和点赞数排序）
        
        Args:
            limit: 返回数量，默认 5
            
        Returns:
            热门数据集列表
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/datasets",
                params={'page': 1, 'page_size': 1000},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                datasets = data.get('data', {}).get('list', [])
                
                # 按下载量和点赞数综合排序
                def popularity_score(d):
                    return d.get('downloads', 0) + d.get('likes', 0) * 100
                
                sorted_datasets = sorted(
                    datasets,
                    key=popularity_score,
                    reverse=True
                )[:limit]
                
                return {
                    'success': True,
                    'datasets': sorted_datasets
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Failed to get popular datasets')
                }
    
    @mcp.tool()
    async def get_datasets_by_domain(domain: str) -> Dict[str, Any]:
        """
        按领域获取数据集
        
        Args:
            domain: 领域名称（如 biology, medicine, materials-science 等）
            
        Returns:
            该领域的数据集列表
        """
        return await list_datasets(page=1, page_size=100, domain=domain)
    
    @mcp.tool()
    async def compare_datasets(dataset_ids: List[str]) -> Dict[str, Any]:
        """
        对比多个数据集
        
        Args:
            dataset_ids: 数据集 ID 列表
            
        Returns:
            数据集对比信息
        """
        datasets = []
        errors = []
        
        for dataset_id in dataset_ids:
            result = await get_dataset_detail(dataset_id)
            if result.get('success'):
                datasets.append(result.get('dataset', {}))
            else:
                errors.append(f"Dataset {dataset_id}: {result.get('error')}")
        
        if not datasets:
            return {
                'success': False,
                'error': 'No valid datasets found',
                'details': errors
            }
        
        # 生成对比摘要
        comparison = {
            'total_size': sum(
                int(d.get('size', '0').replace('GB', '').replace('MB', '').replace('KB', ''))
                for d in datasets
            ),
            'total_rows': sum(d.get('rows', 0) for d in datasets),
            'total_downloads': sum(d.get('downloads', 0) for d in datasets),
            'total_likes': sum(d.get('likes', 0) for d in datasets),
            'domains': list(set(d.get('domain', '') for d in datasets)),
            'tasks': list(set(d.get('task', '') for d in datasets)),
            'languages': list(set(d.get('language', '') for d in datasets)),
        }
        
        return {
            'success': True,
            'comparison': comparison,
            'datasets': datasets,
            'errors': errors if errors else None
        }

    return mcp
