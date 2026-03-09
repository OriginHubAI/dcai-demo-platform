from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .client import DataflowClient

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
