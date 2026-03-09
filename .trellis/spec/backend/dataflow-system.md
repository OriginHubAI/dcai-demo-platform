# Dataflow System Backend Specification

> **Module Location**: `dataflow-system/`
> **Technology Stack**: FastAPI, Prefect, Ray, PostgreSQL, S3.

## 1. Architectural Overview

The Dataflow System is a distributed computation engine designed for data processing pipelines (DAGs) and long-running AI serving tasks.

### Core Components
- **FastAPI Layer**: Provides the external REST API for pipeline management and operator discovery.
- **Prefect Orchestrator**: Manages the lifecycle of pipelines (Flows), including scheduling, retries, and state tracking.
- **Ray Execution Engine**: Handles the distributed execution of individual operators (Tasks).
- **Storage**: Uses S3-compatible storage for intermediate and final data artifacts.

## 2. Core Entities

### 2.1 Pipeline
A set of processing steps organized as a Directed Acyclic Graph (DAG).
- **Nodes**: Individual execution units (Operators).
- **Edges**: Data dependencies between operators.

### 2.2 Operator
A reusable component that performs a specific data transformation or AI task.
- **Internal Operators**: Built-in logic (e.g., embedding, parsing).
- **External Operators**: User-defined or project-specific logic.

## 3. API Endpoints

All endpoints use a standard response envelope:
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 3.1 Pipelines (`/api/v1/pipelines`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/create` | Submit a new pipeline configuration for execution. |
| GET | `/{id}/status` | Query the current execution state (Pending, Running, Completed). |
| GET | `/{id}/info` | Retrieve detailed metadata about the pipeline. |
| POST | `/{id}/cancel` | Stop an ongoing pipeline execution. |
| GET | `/{id}/results` | Retrieve S3 paths for output artifacts. |

### 3.2 Operators (`/api/v1/operators`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | List all registered operators and their configuration requirements. |

## 4. Pydantic Schemas (Reference)

### PipelineRequest
```python
class PipelineRequest(BaseModel):
    pipeline_key_in_backend: UUID
    priority: int
    pipeline_config: PipelineConfig
    datasets_config: List[DatasetConfig]
    output_storage_config: OutputStorageConfig
```

### OperatorInfo
```python
class OperatorInfo(BaseModel):
    id: str
    name: str
    type: str
    description: str
    parameters: Dict[str, Any]
```

## 5. Integration Patterns

Main backend (Django) interacts with the Dataflow System by:
1. Validating user-defined graph layouts.
2. Generating a unique `pipeline_key_in_backend`.
3. Posting the `PipelineRequest` to the Dataflow API.
4. Polling or receiving callbacks for status updates.
5. Fetching final data from the provided S3 paths.
