"""
Knowledge base compatibility URLs.
"""
from django.urls import path

from hub import api as hub_api


urlpatterns = [
    path('knowledgebase', hub_api.knowledge_list_v2, name='knowledgebase-list'),
    path('knowledgebase/<path:repo_id>', hub_api.knowledge_detail_v2, name='knowledgebase-detail'),
]
