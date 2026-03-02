"""
Knowledge Base MCP Tools
提供知识库相关的 MCP 工具接口
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

class KnowledgeBaseInfo(BaseModel):
    """知识库信息模型"""
    id: str = Field(..., description="知识库唯一标识符")
    name: str = Field(..., description="知识库名称")
    description: str = Field(..., description="知识库描述")
    author: str = Field(..., description="作者")
    status: str = Field(..., description="状态 (ready, processing, syncing, error)")
    type: str = Field(..., description="类型 (academic, research, general)")
    lastModified: str = Field(..., description="最后修改时间")


class VectorStoreInfo(BaseModel):
    """向量存储信息"""
    type: str = Field(..., description="向量存储类型")
    vectorCount: int = Field(..., description="向量数量")


class DocumentStats(BaseModel):
    """文档统计信息"""
    total: int = Field(..., description="文档总数")
    processed: int = Field(..., description="已处理文档数")
    indexed: int = Field(..., description="已索引文档数")


class KnowledgeSource(BaseModel):
    """知识源信息"""
    type: str = Field(..., description="源类型 (dataset, document, url)")
    id: str = Field(..., description="源 ID")
    name: str = Field(..., description="源名称")


class KnowledgeBaseDetail(BaseModel):
    """知识库详细信息"""
    id: str = Field(..., description="知识库 ID")
    name: str = Field(..., description="知识库名称")
    description: str = Field(..., description="描述")
    author: str = Field(..., description="作者")
    status: str = Field(..., description="状态")
    type: str = Field(..., description="类型")
    lastModified: str = Field(..., description="最后修改时间")
    vectorStore: VectorStoreInfo = Field(..., description="向量存储信息")
    documents: DocumentStats = Field(..., description="文档统计")
    sources: List[KnowledgeSource] = Field(..., description="知识源列表")


class SearchResult(BaseModel):
    """搜索结果"""
    content: str = Field(..., description="匹配内容")
    score: float = Field(..., description="相似度分数")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


# ============ MCP Tools ============

def register_knowledgebase_tools(mcp: FastMCP):
    """注册 Knowledge Base 相关的 MCP 工具"""
    
    @mcp.tool()
    async def list_knowledge_bases(
        status: Optional[str] = None,
        kb_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取知识库列表
        
        Args:
            status: 状态筛选 (ready, processing, syncing, error)
            kb_type: 类型筛选 (academic, research, general)
            
        Returns:
            知识库列表
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/knowledgebase",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                knowledge_bases = data.get('data', {}).get('list', [])
                
                # 应用筛选
                if status:
                    knowledge_bases = [
                        kb for kb in knowledge_bases
                        if kb.get('status') == status
                    ]
                
                if kb_type:
                    knowledge_bases = [
                        kb for kb in knowledge_bases
                        if kb.get('type') == kb_type
                    ]
                
                return {
                    'success': True,
                    'total': len(knowledge_bases),
                    'knowledge_bases': knowledge_bases
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Failed to fetch knowledge bases'),
                    'knowledge_bases': []
                }
    
    @mcp.tool()
    async def get_knowledge_base_detail(kb_id: str) -> Dict[str, Any]:
        """
        获取知识库详情
        
        Args:
            kb_id: 知识库唯一标识符
            
        Returns:
            知识库详细信息
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/knowledgebase/{kb_id}",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                kb_data = data.get('data', {})
                
                # 构建详细信息
                detail = {
                    'id': kb_data.get('id'),
                    'name': kb_data.get('name'),
                    'description': kb_data.get('description'),
                    'author': kb_data.get('author'),
                    'status': kb_data.get('status'),
                    'type': kb_data.get('type'),
                    'lastModified': kb_data.get('lastModified'),
                    'vectorStore': kb_data.get('vectorStore', {}),
                    'documents': kb_data.get('documents', {}),
                    'sources': kb_data.get('sources', [])
                }
                
                # 计算处理进度
                docs = detail.get('documents', {})
                total = docs.get('total', 0)
                processed = docs.get('processed', 0)
                indexed = docs.get('indexed', 0)
                
                if total > 0:
                    detail['processing_progress'] = {
                        'processed_percent': round(processed / total * 100, 2),
                        'indexed_percent': round(indexed / total * 100, 2)
                    }
                
                return {
                    'success': True,
                    'knowledge_base': detail
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Knowledge base not found')
                }
    
    @mcp.tool()
    async def search_knowledge_bases(
        keyword: str,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        搜索知识库
        
        Args:
            keyword: 搜索关键词
            status: 状态筛选（可选）
            
        Returns:
            搜索结果列表
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/knowledgebase",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                all_kbs = data.get('data', {}).get('list', [])
                keyword_lower = keyword.lower()
                
                # 在名称和描述中搜索
                filtered = [
                    kb for kb in all_kbs
                    if keyword_lower in kb.get('name', '').lower()
                    or keyword_lower in kb.get('description', '').lower()
                    or keyword_lower in kb.get('author', '').lower()
                ]
                
                # 应用状态筛选
                if status:
                    filtered = [
                        kb for kb in filtered
                        if kb.get('status') == status
                    ]
                
                return {
                    'success': True,
                    'total': len(filtered),
                    'knowledge_bases': filtered
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Search failed'),
                    'knowledge_bases': []
                }
    
    @mcp.tool()
    async def get_knowledge_base_statistics() -> Dict[str, Any]:
        """
        获取知识库统计信息
        
        Returns:
            知识库统计概览
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/knowledgebase",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                knowledge_bases = data.get('data', {}).get('list', [])
                
                # 计算统计信息
                total_vectors = sum(
                    kb.get('vectorStore', {}).get('vectorCount', 0)
                    for kb in knowledge_bases
                )
                total_documents = sum(
                    kb.get('documents', {}).get('total', 0)
                    for kb in knowledge_bases
                )
                total_processed = sum(
                    kb.get('documents', {}).get('processed', 0)
                    for kb in knowledge_bases
                )
                total_indexed = sum(
                    kb.get('documents', {}).get('indexed', 0)
                    for kb in knowledge_bases
                )
                
                # 按状态统计
                status_stats = {}
                for kb in knowledge_bases:
                    status = kb.get('status', 'unknown')
                    if status not in status_stats:
                        status_stats[status] = 0
                    status_stats[status] += 1
                
                # 按类型统计
                type_stats = {}
                for kb in knowledge_bases:
                    kb_type = kb.get('type', 'unknown')
                    if kb_type not in type_stats:
                        type_stats[kb_type] = 0
                    type_stats[kb_type] += 1
                
                return {
                    'success': True,
                    'statistics': {
                        'total_knowledge_bases': len(knowledge_bases),
                        'total_vectors': total_vectors,
                        'total_documents': total_documents,
                        'total_processed': total_processed,
                        'total_indexed': total_indexed,
                        'processing_rate': round(total_processed / total_documents * 100, 2) if total_documents > 0 else 0,
                        'indexing_rate': round(total_indexed / total_documents * 100, 2) if total_documents > 0 else 0,
                        'by_status': status_stats,
                        'by_type': type_stats
                    }
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Failed to get statistics')
                }
    
    @mcp.tool()
    async def get_knowledge_base_sources(kb_id: str) -> Dict[str, Any]:
        """
        获取知识库的数据源
        
        Args:
            kb_id: 知识库 ID
            
        Returns:
            数据源列表
        """
        result = await get_knowledge_base_detail(kb_id)
        
        if result.get('success'):
            kb = result.get('knowledge_base', {})
            sources = kb.get('sources', [])
            
            # 按类型分组
            sources_by_type = {}
            for source in sources:
                source_type = source.get('type', 'unknown')
                if source_type not in sources_by_type:
                    sources_by_type[source_type] = []
                sources_by_type[source_type].append(source)
            
            return {
                'success': True,
                'kb_id': kb_id,
                'kb_name': kb.get('name'),
                'total_sources': len(sources),
                'sources': sources,
                'sources_by_type': sources_by_type
            }
        else:
            return result
    
    @mcp.tool()
    async def get_ready_knowledge_bases() -> Dict[str, Any]:
        """
        获取所有就绪状态的知识库
        
        Returns:
            就绪状态的知识库列表
        """
        return await list_knowledge_bases(status='ready')
    
    @mcp.tool()
    async def check_knowledge_base_status(kb_id: str) -> Dict[str, Any]:
        """
        检查知识库状态
        
        Args:
            kb_id: 知识库 ID
            
        Returns:
            知识库状态信息
        """
        result = await get_knowledge_base_detail(kb_id)
        
        if result.get('success'):
            kb = result.get('knowledge_base', {})
            status = kb.get('status')
            documents = kb.get('documents', {})
            
            status_info = {
                'kb_id': kb_id,
                'name': kb.get('name'),
                'status': status,
                'is_ready': status == 'ready',
                'is_processing': status == 'processing',
                'is_syncing': status == 'syncing',
                'has_error': status == 'error',
                'document_stats': documents,
                'vector_count': kb.get('vectorStore', {}).get('vectorCount', 0)
            }
            
            # 添加状态描述
            status_descriptions = {
                'ready': '知识库已就绪，可以正常使用',
                'processing': '知识库正在处理中，请稍后再试',
                'syncing': '知识库正在同步中，部分功能可能不可用',
                'error': '知识库处理出错，需要检查配置'
            }
            status_info['status_description'] = status_descriptions.get(
                status, '未知状态'
            )
            
            return {
                'success': True,
                'status_info': status_info
            }
        else:
            return result
    
    @mcp.tool()
    async def compare_knowledge_bases(kb_ids: List[str]) -> Dict[str, Any]:
        """
        对比多个知识库
        
        Args:
            kb_ids: 知识库 ID 列表
            
        Returns:
            知识库对比信息
        """
        knowledge_bases = []
        errors = []
        
        for kb_id in kb_ids:
            result = await get_knowledge_base_detail(kb_id)
            if result.get('success'):
                knowledge_bases.append(result.get('knowledge_base', {}))
            else:
                errors.append(f"Knowledge base {kb_id}: {result.get('error')}")
        
        if not knowledge_bases:
            return {
                'success': False,
                'error': 'No valid knowledge bases found',
                'details': errors
            }
        
        # 生成对比摘要
        total_vectors = sum(
            kb.get('vectorStore', {}).get('vectorCount', 0)
            for kb in knowledge_bases
        )
        total_docs = sum(
            kb.get('documents', {}).get('total', 0)
            for kb in knowledge_bases
        )
        
        comparison = {
            'total_knowledge_bases': len(knowledge_bases),
            'total_vectors': total_vectors,
            'total_documents': total_docs,
            'avg_vectors_per_kb': round(total_vectors / len(knowledge_bases), 2) if knowledge_bases else 0,
            'statuses': [kb.get('status') for kb in knowledge_bases],
            'types': list(set(kb.get('type', '') for kb in knowledge_bases)),
            'all_ready': all(kb.get('status') == 'ready' for kb in knowledge_bases)
        }
        
        return {
            'success': True,
            'comparison': comparison,
            'knowledge_bases': knowledge_bases,
            'errors': errors if errors else None
        }
    
    @mcp.tool()
    async def find_knowledge_bases_by_source(
        source_type: str,
        source_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        根据数据源查找知识库
        
        Args:
            source_type: 源类型 (dataset, document, url)
            source_id: 源 ID（可选）
            
        Returns:
            包含该数据源的知识库列表
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BACKEND_API_URL}/knowledgebase",
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('code') == 0:
                all_kbs = data.get('data', {}).get('list', [])
                
                # 筛选包含指定数据源的知识库
                matched_kbs = []
                for kb in all_kbs:
                    sources = kb.get('sources', [])
                    for source in sources:
                        if source.get('type') == source_type:
                            if source_id is None or source.get('id') == source_id:
                                matched_kbs.append({
                                    'knowledge_base': kb,
                                    'matched_source': source
                                })
                                break
                
                return {
                    'success': True,
                    'total': len(matched_kbs),
                    'source_type': source_type,
                    'source_id': source_id,
                    'knowledge_bases': matched_kbs
                }
            else:
                return {
                    'success': False,
                    'error': data.get('msg', 'Failed to search knowledge bases')
                }
    
    @mcp.tool()
    async def get_knowledge_base_document_summary(kb_id: str) -> Dict[str, Any]:
        """
        获取知识库文档摘要
        
        Args:
            kb_id: 知识库 ID
            
        Returns:
            文档处理摘要
        """
        result = await get_knowledge_base_detail(kb_id)
        
        if result.get('success'):
            kb = result.get('knowledge_base', {})
            docs = kb.get('documents', {})
            
            total = docs.get('total', 0)
            processed = docs.get('processed', 0)
            indexed = docs.get('indexed', 0)
            
            pending = total - processed
            unindexed = processed - indexed
            
            summary = {
                'kb_id': kb_id,
                'kb_name': kb.get('name'),
                'status': kb.get('status'),
                'document_summary': {
                    'total': total,
                    'processed': processed,
                    'indexed': indexed,
                    'pending': pending,
                    'unindexed': unindexed
                },
                'progress': {
                    'processing': round(processed / total * 100, 2) if total > 0 else 0,
                    'indexing': round(indexed / total * 100, 2) if total > 0 else 0
                },
                'is_fully_processed': total > 0 and total == processed,
                'is_fully_indexed': total > 0 and total == indexed
            }
            
            return {
                'success': True,
                'summary': summary
            }
        else:
            return result

    return mcp
