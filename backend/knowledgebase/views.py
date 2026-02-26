"""
Knowledgebase views for ADP Backend
"""
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import KnowledgeBase, KnowledgeBaseDocument
from .serializers import KnowledgeBaseSerializer, KnowledgeBaseCreateSerializer


class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    """Knowledge base CRUD"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'kb_id'
    serializer_class = KnowledgeBaseSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return KnowledgeBaseCreateSerializer
        return KnowledgeBaseSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = KnowledgeBase.objects.filter(owner=user)
        
        list_type = self.request.query_params.get('list_type')
        group_id = self.request.query_params.get('group_id')
        keyword = self.request.query_params.get('keyword')
        
        if keyword:
            queryset = queryset.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        
        return queryset
    
    def perform_create(self, serializer):
        kb_id = f"kb_{uuid.uuid4().hex[:8]}"
        serializer.save(kb_id=kb_id, owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def refresh(self, request, kb_id=None):
        """Refresh knowledge base"""
        kb = self.get_object()
        # TODO: Implement refresh logic
        return Response({'code': 0, 'msg': 'success', 'data': {}})
    
    @action(detail=True, methods=['get', 'post', 'delete'])
    def documents(self, request, kb_id=None):
        """Get/add/remove documents"""
        kb = self.get_object()
        
        if request.method == 'GET':
            docs = kb.documents.all()
            return Response({
                'code': 0,
                'msg': 'success',
                'data': [{'id': d.id, 'document_id': d.document_id, 'name': d.name, 'status': d.status} for d in docs]
            })
        
        if request.method == 'POST':
            # TODO: Implement document upload
            return Response({'code': 0, 'msg': 'success', 'data': {}})
        
        if request.method == 'DELETE':
            doc_ids = request.data.get('document_ids', [])
            KnowledgeBaseDocument.objects.filter(knowledge_base=kb, document_id__in=doc_ids).delete()
            return Response({'code': 0, 'msg': 'success', 'data': {}})
