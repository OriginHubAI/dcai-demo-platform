# Generate Dataflow System backend spec and mock server

## Goal
Establish the backend development specifications for the `dataflow-system` module and provide a mock FastAPI server for integration testing and development.

## Requirements

### 1. Backend Development Specification
- Create `.trellis/spec/backend/dataflow-system.md` containing:
    - Core architectural overview (FastAPI + Prefect + Ray).
    - API endpoint definitions based on `dataflow-system/app/api/`.
    - Data models and Pydantic schemas based on `dataflow-system/app/schemas/`.
    - Interaction flow between Django (main backend) and Dataflow System (low-level module).

### 2. Mock FastAPI Server
- Implement `backend/fastapi_app/mock_dataflow.py` (or similar path) that:
    - Implements all endpoints identified in `dataflow-system/app/api/`.
    - Uses the same Pydantic schemas for request validation.
    - Provides mock responses for:
        - `POST /api/v1/pipelines/create`
        - `GET /api/v1/pipelines/{pipeline_id}/status`
        - `GET /api/v1/operators`
    - Simulates pipeline state transitions (Pending -> Running -> Completed).

### 3. Integration Consistency
- Ensure the mock server follows the same response envelope (`code`, `message`, `data`).
- Match the naming conventions and UUID-based identifiers used in the original module.

## Acceptance Criteria
- [ ] `.trellis/spec/backend/dataflow-system.md` exists and accurately describes the module.
- [ ] `backend/fastapi_app/mock_dataflow.py` is implemented and runnable.
- [ ] Mock server endpoints return the expected structure.
- [ ] Documentation updated in `backend/FASTAPI_INTEGRATION.md` if necessary.

## Technical Notes
- `dataflow-system` uses a custom `DataflowSystemResponse` envelope.
- Pipelines are represented as DAGs with nodes and edges.
- Storage is handled via S3 configurations.
