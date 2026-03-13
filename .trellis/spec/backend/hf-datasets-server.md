# HF Datasets Server (LocalFS)

The `dcai-platform` provides a local filesystem-based implementation of the Hugging Face Hub and Datasets Server (Viewer) APIs. This allows both the frontend and Python libraries like `datasets` to interact with local data as if it were hosted on Hugging Face.

## Architecture

- **Service**: `backend/dataset/services.py` containing `LocalFSDatasetsServer`.
- **Storage Root**: `backend/fastapi_app/sample_data/`.
- **API Namespace**: `/api/hf/`.

## Features

### 1. Hub API Compatibility
Supports core repository management and file resolution:
- `GET /api/hf/api/datasets`: List all local datasets.
- `GET /api/hf/api/datasets/{repo_id}`: Metadata including file siblings.
- `GET /api/hf/datasets/{repo_id}/resolve/{rev}/{path}`: Download/stream files.
- `POST /api/hf/api/repos/create`: Create new dataset repositories.
- `DELETE /api/hf/api/datasets/{repo_id}`: Delete repositories.
- `POST /api/hf/api/datasets/{repo_id}/upload/{rev}/{path}`: Upload files.

### 2. Viewer API Compatibility
Implements the HF Datasets Server protocol for data inspection:
- `GET /api/hf/is-valid?dataset={id}`: Capability check.
- `GET /api/hf/splits?dataset={id}`: List available splits (train, test, etc.).
- `GET /api/hf/rows?dataset={id}&split={s}&offset={o}&length={l}`: Paginated data rows.
- `GET /api/hf/info?dataset={id}`: Dataset metadata and schema inference.

## Implementation Details

### Dataset Identification
A directory is recognized as a dataset repo if:
1. It contains a `resolve/` directory.
2. It contains a `{repo_name}.py` loader script.
3. It contains common data files (`.jsonl`, `.csv`, `.parquet`) at the root.

### Schema Inference
The server dynamically infers dtypes by inspecting the first few rows of a dataset if an `info.json` is not provided. Supported types: `string`, `int64`, `float64`, `bool`.

### Compatibility Patterns
- **Paths-info**: Handles both JSON and Form-data based path probes from `huggingface_hub`.
- **Git Tree**: Simulates `/tree/` and OIDs for frontend components that expect a Git-like structure.
- **Request Dispatching**: `hf_dataset_metadata` handles greedy path matching and dispatches `DELETE` and Git-subpath requests to appropriate handlers.

## Testing
Comprehensive tests are located in `backend/dataset/tests.py`. They use `StaticLiveServerTestCase` and patch the `datasets` library's `HF_ENDPOINT` to point to the local test server.
