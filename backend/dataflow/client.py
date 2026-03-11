import logging
import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

class DataflowClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or settings.DATAFLOW_MOCK_URL
        self.api_url = f"{self.base_url.rstrip('/')}/api/v1"

    def list_operators(self):
        """Fetch all available operators from Dataflow System"""
        url = f"{self.api_url}/operators"
        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                # Operators endpoint returns a list directly in the mock (and likely real system)
                # If it uses the envelope, we'd handle it here.
                return response.json()
        except Exception as e:
            logger.error(f"DataflowClient: Failed to list operators: {e}")
            return []

    def create_pipeline(self, pipeline_request: dict):
        """Submit a pipeline to Dataflow System"""
        url = f"{self.api_url}/pipelines/create"
        try:
            with httpx.Client() as client:
                response = client.post(url, json=pipeline_request)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"DataflowClient: Failed to create pipeline: {e}")
            return {"code": 500, "message": str(e), "data": None}

    def get_pipeline_status(self, pipeline_id: str):
        """Get status of a specific pipeline"""
        url = f"{self.api_url}/pipelines/{pipeline_id}/status"
        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"DataflowClient: Failed to get pipeline status: {e}")
            return {"code": 500, "message": str(e), "data": None}

    def get_pipeline_results(self, pipeline_id: str):
        """Get results of a specific pipeline"""
        url = f"{self.api_url}/pipelines/{pipeline_id}/results"
        try:
            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"DataflowClient: Failed to get pipeline results: {e}")
            return {"code": 500, "message": str(e), "data": None}
