"""
Dataset V2 URL Configuration
"""
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dataset_v2_list(request):
    """Dataset V2 list"""
    return Response({'code': 0, 'msg': 'success', 'data': {'list': [], 'total': 0}})


urlpatterns = [
    path('dataset/', dataset_v2_list, name='dataset-v2-list'),
]
