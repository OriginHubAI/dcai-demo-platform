# Implement Mock Datasets Server

## Goal
Implement a mock server for Hugging Face Datasets to facilitate internal testing and DataFlow integration. The server should serve sample dataset files from local storage and support key Hugging Face Hub APIs.

## Requirements
1.  **FastAPI Mock Server**: Create `backend/fastapi_app/mock_hf.py` based on `hf-datasets-api.md`.
2.  **Local Storage**: Store sample dataset files in a local directory (e.g., `backend/fastapi_app/sample_data/`).
3.  **Supported APIs**:
    *   `GET /api/datasets/{repo_id}`: Hub metadata.
    *   `GET /datasets/{repo_id}/resolve/{revision}/{path}`: File download (redirect to local file).
    *   `GET /parquet?dataset={dataset_name}`: Parquet export list.
    *   `GET /info?dataset={dataset_name}`: Dataset info.
4.  **Auto-start**: Implement auto-start logic in `backend/dataset/apps.py` (similar to `dataflow`).
5.  **Environment Configuration**: Add `ENABLE_MOCK_HF`, `HF_ENDPOINT`, and `HF_DATASETS_CACHE` support.
6.  **Integration Tests**: Add tests in `backend/dataset/tests.py` using `datasets` library to verify the mock server.

## Acceptance Criteria
- [ ] Mock server starts automatically when `ENABLE_MOCK_HF=True`.
- [ ] `datasets.load_dataset()` can successfully load a dataset from the mock server.
- [ ] Local sample files are served correctly via the mock server.
- [ ] Integration tests pass.

## Technical Notes
- Use `hf-datasets-api.md` as the primary reference for API signatures and expected responses.
- Follow the auto-start pattern from `backend/dataflow/apps.py`.
- Handle the `datasets-server` subdomain or path mapping if necessary (as noted in `hf-datasets-api.md`).
