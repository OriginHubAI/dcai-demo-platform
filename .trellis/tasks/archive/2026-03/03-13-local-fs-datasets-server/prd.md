# LocalFSDatasetsServer Implementation

## Goal
Replace the existing simplistic HF mock server and Django views with a robust, feature-complete `LocalFSDatasetsServer` that supports both Hub (management) and Viewer (data inspection) APIs, ensuring full compatibility with the `huggingface_hub` and `datasets` Python libraries as well as the platform's frontend.

## Requirements

### Hub API (Dataset Management)
- [ ] **List Datasets** (`/api/datasets`): Support filtering, search, and return real metadata (num_samples, file_size).
- [ ] **Dataset Metadata** (`/api/datasets/{repo_id}`): Return detailed repository info, including siblings (file list).
- [ ] **Resolve/Download** (`/datasets/{repo_id}/resolve/{rev}/{path}`): Stream actual file content from local storage.
- [ ] **Create Repository** (`/api/repos/create`): Support creating new dataset directories.
- [ ] **Delete Repository** (`/api/repos/delete`): Support removing dataset directories.
- [ ] **Upload File** (`/api/datasets/{repo_id}/upload/{rev}/{path}`): Support uploading and persisting files.
- [ ] **Git Tree APIs**: Support `/tree/`, `/paths-info/`, and `/commits/` for frontend compatibility.

### Viewer API (Data Inspection)
- [ ] **Capabilities** (`/is-valid`, `/splits`): Identify available splits (e.g., `train`, `test`).
- [ ] **Dataset Info** (`/info`): Dynamically infer schemas (dtypes) and descriptions from local files.
- [ ] **Data Rows** (`/rows`, `/first-rows`): Implement real row-level reading and pagination for JSONL, JSON, CSV, and Parquet.

### Technical Integrity
- [ ] Implement a `DatasetRegistry` to manage local storage paths and metadata.
- [ ] Use `fastapi_app/sample_data` as the primary local storage root.
- [ ] Ensure all responses are in standard HF formats (no ADP middleware wrapping).
- [ ] Comprehensive test suite in `backend/dataset/tests.py` covering both Hub and Viewer functionalities.

## Acceptance Criteria
- [ ] `datasets.load_dataset` can successfully load, stream, and inspect local datasets.
- [ ] Frontend data studio can list, navigate, and preview (with pagination) local datasets.
- [ ] Write operations (create, upload, delete) work and persist to the filesystem.
- [ ] All unit tests pass.
