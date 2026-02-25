"""
Collection views for ADP Backend
"""
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Collection, CollectionDocument
from .serializers import CollectionSerializer, CollectionCreateSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """Collection CRUD"""
    permission_classes = [IsAuthenticated]
    lookup_field = 'collection_id'
    serializer_class = CollectionSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionCreateSerializer
        return CollectionSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Collection.objects.filter(owner=user)
        
        list_type = self.request.query_params.get('list_type')
        if list_type == 'my':
            queryset = queryset.filter(owner=user)
        
        return queryset
    
    def perform_create(self, serializer):
        collection_id = f"col_{uuid.uuid4().hex[:8]}"
        serializer.save(collection_id=collection_id, owner=self.request.user)
    
    @action(detail=True, methods=['get', 'put', 'delete'])
    def documents(self, request, collection_id=None):
        """Get/add/remove documents in collection"""
        collection = self.get_object()
        
        if request.method == 'GET':
            docs = collection.documents.all()
            return Response({
                'code': 0,
                'msg': 'success',
                'data': [{'document_id': d.document_id, 'kb_id': d.kb_id, 'added_at': d.added_at} for d in docs]
            })
        elif request.method == 'PUT':
            # Add documents
            doc_ids = request.data.get('document_ids', [])
            for doc_id in doc_ids:
                CollectionDocument.objects.get_or_create(
                    collection=collection,
                    document_id=doc_id.get('id'),
                    kb_id=doc_id.get('kb_id')
                )
            return Response({'code': 0, 'msg': 'success', 'data': {}})
        elif request.method == 'DELETE':
            doc_ids = request.data.get('document_ids', [])
            CollectionDocument.objects.filter(collection=collection, document_id__in=doc_ids).delete()
            return Response({'code': 0, 'msg': 'success', 'data': {}})
