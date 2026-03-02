"""
MCP Tools Package
包含 Dataset 和 Knowledge Base 的 MCP 工具定义
"""
from .dataset_tools import register_dataset_tools
from .knowledgebase_tools import register_knowledgebase_tools

__all__ = ['register_dataset_tools', 'register_knowledgebase_tools']
