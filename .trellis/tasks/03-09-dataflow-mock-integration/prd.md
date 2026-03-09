# Integrate mock Dataflow System with auto-start

## Goal
Automate the lifecycle of the mock Dataflow System server during backend development and integrate the Django backend with its API.

## Requirements

### 1. Environment Configuration
- [x] Add `ENABLE_MOCK_DATAFLOW` (default: `False`) to `.env.example`.
- [x] Add `DATAFLOW_SERVICE_URL` (default: `http://localhost:8001`) to `.env.example`.
- [x] Update `backend/core/settings.py` to expose these settings.

### 2. Auto-start Mock Server
- [x] Implement logic in `backend/dataflow/apps.py` (using `ready()` method) to start the mock FastAPI server if `ENABLE_MOCK_DATAFLOW` is `True`.
- [x] Ensure the mock server runs in a separate process and is managed gracefully.
- [x] Handle the case where the port is already in use.

### 3. Dataflow System Client
- [x] Create `backend/dataflow/client.py` to handle communication with the Dataflow System (mock or real).
- [x] Implement methods for:
    - `list_operators()`
    - `create_pipeline(request_data)`
    - `get_pipeline_status(pipeline_id)`
- [x] Use `httpx` or `requests` for API calls.

### 4. Integration & Testing
- [x] Create a sample view in `backend/dataflow/views.py` that utilizes the client.
- [x] Add integration tests in `backend/dataflow/tests.py` to verify:
    - Client correctly communicates with the mock server.
    - Mock server starts/responds correctly when enabled.

## Acceptance Criteria
- [x] Mock server starts automatically when `python manage.py runserver` is used (if enabled).
- [x] Django backend can fetch operators from the mock server.
- [x] Environment variables are documented in `.env.example`.
- [x] Integration tests pass.

## Technical Notes
- Project uses `httpx` for async FastAPI proxying; consider using it for the client as well.
- The mock server path is `backend/fastapi_app/mock_dataflow.py`.
