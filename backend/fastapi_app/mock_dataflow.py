import uuid
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Dict, List, Optional
from uuid import UUID

from fastapi import FastAPI, APIRouter, HTTPException, Path, Query, Body
from pydantic import BaseModel, Field

app = FastAPI(title="Mock Dataflow System", version="0.1.0")
router = APIRouter(prefix="/api/v1")

# --- Schemas (Mirrored from dataflow-system) ---

class ResponseCode(int, Enum):
    SUCCESS = 0
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

class DataflowSystemResponse(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Optional[Any] = None, message: str = "success") -> "DataflowSystemResponse":
        return cls(code=ResponseCode.SUCCESS, message=message, data=data)

class S3StorageOptions(BaseModel):
    class S3ClientKwargs(BaseModel):
        endpoint_url: str
        region_name: str = ""
    key: str
    secret: str
    client_kwargs: S3ClientKwargs

class DatasetConfig(BaseModel):
    dataset_id: UUID
    bucket_name: str
    storage_options: S3StorageOptions
    s3_files: Optional[List[str]] = None
    s3_directory: Optional[List[str]] = None

class OutputStorageConfig(BaseModel):
    bucket_name: str
    storage_options: S3StorageOptions
    s3_result_directory: str

class Node(BaseModel):
    class NodeConfig(BaseModel):
        run: Dict[str, Any]
        init: Dict[str, Any]
    id: UUID
    task_idx: int
    operator_name: str
    operator_type: str
    config: NodeConfig

class Edge(BaseModel):
    source: UUID
    target: UUID
    source_port: str
    target_port: str

class PipelineConfig(BaseModel):
    name: str
    task_type: str
    nodes: List[Node]
    edges: List[Edge]

class PipelineRequest(BaseModel):
    pipeline_key_in_backend: UUID
    priority: Annotated[int, Field(ge=0, le=100)]
    pipeline_config: PipelineConfig
    datasets_config: List[DatasetConfig]
    output_storage_config: OutputStorageConfig

class OperatorInfo(BaseModel):
    id: str
    name: str
    type: str
    description: str
    parameters: Dict[str, Any]

# --- Mock Data ---

MOCK_OPERATORS = [
    OperatorInfo(
        id="op_llm_extract",
        name="LLM Information Extraction",
        type="TRANSFORM",
        description="Extract structured information from unstructured text using LLM.",
        parameters={"model": "gpt-4", "prompt_template": "string"}
    ),
    OperatorInfo(
        id="op_embedding",
        name="Text Embedding",
        type="TRANSFORM",
        description="Generate vector embeddings for text chunks.",
        parameters={"model": "text-embedding-3-small"}
    ),
    OperatorInfo(
        id="op_myscale_insert",
        name="MyScale Vector Insert",
        type="SINK",
        description="Insert embeddings and metadata into MyScale database.",
        parameters={"table_name": "string"}
    )
]

# In-memory store for pipelines
pipelines_db = {}

# --- Routes ---

@router.get("/operators", response_model=List[OperatorInfo])
async def list_operators():
    return MOCK_OPERATORS

@router.post("/pipelines/create", response_model=DataflowSystemResponse)
async def create_pipeline(request: PipelineRequest):
    pipeline_id = uuid.uuid4()
    pipelines_db[pipeline_id] = {
        "status": "RUNNING",
        "created_at": datetime.now(),
        "request": request.model_dump()
    }
    return DataflowSystemResponse.success(data={
        "pipeline_key_in_backend": request.pipeline_key_in_backend,
        "pipeline_id": pipeline_id
    })

@router.get("/pipelines/{pipeline_id}/status", response_model=DataflowSystemResponse)
async def get_pipeline_status(pipeline_id: UUID = Path(...)):
    if pipeline_id not in pipelines_db:
        return DataflowSystemResponse(code=404, message="Pipeline not found")
    
    # Simple logic to simulate completion
    pipeline = pipelines_db[pipeline_id]
    if (datetime.now() - pipeline["created_at"]).total_seconds() > 30:
        pipeline["status"] = "COMPLETED"
        
    return DataflowSystemResponse.success(data={
        "pipeline_id": pipeline_id,
        "status": pipeline["status"]
    })

@router.get("/pipelines/{pipeline_id}/results", response_model=DataflowSystemResponse)
async def get_pipeline_results(pipeline_id: UUID = Path(...)):
    if pipeline_id not in pipelines_db:
        return DataflowSystemResponse(code=404, message="Pipeline not found")
    
    return DataflowSystemResponse.success(data={
        "s3_files": ["s3://mock-bucket/results/task_1.jsonl"],
        "storage_options": {
            "key": "mock-key",
            "secret": "mock-secret",
            "client_kwargs": {"endpoint_url": "http://localhost:9000"}
        }
    })

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    import os
    from urllib.parse import urlparse
    
    url = os.environ.get("DATAFLOW_SYSTEM_URL", "http://127.0.0.1:8001")
    parsed = urlparse(url)
    port = parsed.port or 8001
    host = parsed.hostname or "0.0.0.0"
    
    uvicorn.run(app, host=host, port=port)
