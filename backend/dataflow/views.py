from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from code_server.manager import manager as code_server_manager

from .services import catalog
from .client import DataflowClient

def _not_found(message: str) -> Response:
    return Response({'code': 404, 'msg': message, 'data': {}}, status=404)

@api_view(['GET'])
@permission_classes([AllowAny])
def package_list(request):
    packages = catalog.list_packages()
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'list': packages,
            'total': len(packages),
        },
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def package_detail(request, package_id):
    package = catalog.get_package(package_id)
    if not package:
        return _not_found('package not found')
    return Response({'code': 0, 'msg': 'success', 'data': package})

@api_view(['GET'])
@permission_classes([AllowAny])
def package_files(request, package_id):
    try:
        tree = catalog.build_tree(package_id)
    except FileNotFoundError:
        return _not_found('package not found')
    return Response({'code': 0, 'msg': 'success', 'data': tree})

@api_view(['GET'])
@permission_classes([AllowAny])
def package_file_content(request, package_id):
    relative_path = request.query_params.get('path', '')
    try:
        payload = catalog.read_file(package_id, relative_path)
    except PermissionError:
        return Response({'code': 403, 'msg': 'invalid path', 'data': {}}, status=403)
    except FileNotFoundError:
        return _not_found('file not found')
    return Response({'code': 0, 'msg': 'success', 'data': payload})

@api_view(['POST'])
@permission_classes([AllowAny])
def package_editor_start(request, package_id):
    package = catalog.get_package(package_id)
    if not package:
        return _not_found('package not found')
    session = code_server_manager.get_or_start(package_id, catalog.get_package_repo_path(package_id))
    return Response({
        'code': 0,
        'msg': 'success',
        'data': {
            'mode': session.mode,
            'url': session.url,
            'port': session.port,
            'reason': session.reason,
        },
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def package_editor_stop(request, package_id):
    stopped = code_server_manager.stop(package_id)
    return Response({'code': 0, 'msg': 'success', 'data': {'stopped': stopped}})

@api_view(['POST'])
@permission_classes([AllowAny])
def package_test(request, package_id):
    try:
        payload = catalog.run_package_test(package_id)
    except FileNotFoundError:
        return _not_found('package not found')
    return Response({'code': 0, 'msg': 'success', 'data': payload})

class OperatorListView(APIView):
    """
    View to list available operators from the Dataflow System.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = DataflowClient()
        operators = client.list_operators()
        
        # Return in the standard envelope
        return Response({
            "code": 0,
            "msg": "success",
            "data": operators
        })

class PipelineStatusView(APIView):
    """
    View to check pipeline status.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pipeline_id):
        client = DataflowClient()
        result = client.get_pipeline_status(pipeline_id)
        return Response(result)
