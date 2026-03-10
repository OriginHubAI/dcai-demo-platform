# Dataflow WebUI API Specification

> This document details the required backend API endpoints, payload structures, and authentication mechanisms needed to support the `dataflow-webui` external frontend module.

---

## Authentication Mechanism

The frontend uses token-based authentication (JWT or similar). 

- **Headers**:
  - `Authorization`: `Bearer <token>` or `<token>` (retrieved from `localStorage.getItem('access_token')` or `sessionStorage`).
  - `X-INVITE-CODE`: Optional, used during registration or special API calls.
- **Handling Errors**:
  - `401 Unauthorized`: Triggers frontend to clear tokens and redirect to `/login`.
  - `403 Forbidden`: Triggers a redirect jump.
  - Business errors are expected to return `{ code: != 0, message: "Error message" }`.

---

## API Endpoints by Module

The frontend expects the API to be prefixed with `/api` or directly accessed via the `VITE_APP_BASE_API` environment variable. Most endpoints are under the `/v1/` or `/v2/` namespace.

### Auth & User (`/v1/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `POST` | `/v1/login/phone` | Phone login | `{ phone, code }` |
| `POST` | `/v1/login` | Username/Password login | `{ username, password, uid }` |
| `POST` | `/v1/register` | User registration | `{ username, email, password, code, invite_code }` |
| `POST` | `/v1/logout` | User logout | None |
| `GET`  | `/v1/users/info` | Get user info | None |
| `PUT`  | `/v1/users/sync` | Sync user info | `{ id, registerSource, photo }` |
| `POST` | `/v1/email/code` | Send email verification code | `{ email, scene }` |
| `POST` | `/v1/login/sms/code`| Send SMS verification code | `{ phone }` |
| `POST` | `/v1/password/reset`| Reset password | `{ email, code, newPassword }` |
| `POST` | `/v1/user/password`| Update password | `{ newPassword, oldPassword? }` |

### Tasks & Pipelines (`/v1/` & `/v2/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/v1/task` | Fetch real task list | `?page_size, page_num, keyword, status, dataset_id` |
| `POST` | `/v1/task` | Create a task | `{ name, description, task_type, dataset_ids, template_id, pipeline_config, schedule_config, notification, extend_rules }` |
| `GET`  | `/v1/task/{taskId}` | Get real task details | None |
| `DELETE`| `/v1/task/{taskId}` | Delete task | None |
| `POST` | `/v1/task/{taskId}/start` | Start task | `pipelineData` |
| `POST` | `/v1/task/{taskId}/stop` | Stop task | None |
| `POST` | `/v1/task/{taskId}/resume`| Resume task | `pipelineData` |
| `POST` | `/v1/task/{taskId}/restart`| Restart pipeline | None |
| `POST` | `/v1/task/{taskId}/priority`| Update pipeline priority | `{ priority }` |
| `GET`  | `/v1/task/{taskId}/newly` | Poll real-time updates | `?t={time}` |
| `POST` | `/v2/task/create_and_play` | Save and immediately play task | Task config object |
| `GET`  | `/v2/task/record/{recordId}/play` | Force play task record | None |
| `GET`  | `/v2/task/record/{recordId}/retry`| Retry task record | None |
| `GET`  | `/v2/task/record_detail_simple` | Task progress detail | `?task_id, page_num, page_size, status` |
| `POST` | `/v2/pipelines/results/query`| Query operator results | `{ pipeline_id, stage, page, page_size, parent_pipeline_id? }` |
| `GET`  | `/v1/pipelines/{parentId}/subtasks/{pipelineId}`| Get sub-task detail | None |
| `POST` | `/v1/pipelines/{pipelineId}/result/download`| Download pipeline result | `{ stage }` |

### Datasets (`/v1/dataset` & `/v1/third-party/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/v1/dataset` | List datasets | Pagination params |
| `POST` | `/v1/dataset` | Create dataset | Dataset metadata |
| `GET`  | `/v1/dataset/{id}` | Get dataset details | None |
| `PUT`  | `/v1/dataset/{id}` | Update dataset | `{ name, description }` |
| `DELETE`| `/v1/dataset/{id}`| Delete dataset | None |
| `GET`  | `/v1/dataset/{id}/files`| Get dataset files | `?page_size, page_num, list_type=all` |
| `POST` | `/v1/dataset/{id}/files`| Add dataset file(s) | `{ files: [{ name, description, path, mime_type, size, file_metadata }] }` |
| `DELETE`| `/v1/dataset/{id}/files/{fileId}`| Delete dataset file | None |
| `GET`  | `/v1/dataset/file/url` | Get file download URL | `?object_path` |
| `POST` | `/v1/presigned-url`| Get S3/OSS presigned URL | Upload params |
| `POST` | `/v1/third-party/list`| List third-party datasets | `{ pageNo, pageSize, keywords }` |
| `GET`  | `/v1/third-party/detail/{id}`| Get third-party dataset details | None |
| `GET`  | `/v1/third-party/files/{id}`| Get third-party dataset files | `?prefix, limit` |
| `POST` | `/v1/third-party/kps/query-dataset`| Query KPS dataset | Query params |

### Operators (`/v2/operators/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/v2/operators/` | Fetch operators | `?page=1&page_size=1000` |

### Agents / Topics (`/v1/agents/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/v1/agents` | Get topics list | Pagination |
| `POST` | `/v1/agents` | Create topic | Metadata |
| `GET`  | `/v1/agents/{id}` | Topic details | `?source=share` |
| `PUT`  | `/v1/agents/{id}` | Update topic | Metadata |
| `DELETE`| `/v1/agents/{id}`| Delete topic | None |
| `GET`  | `/v1/agents/hot` | Hot topics list | None |
| `POST` | `/v1/agents/{id}/subscribe/{action}`| Subscribe to topic | `action: 1 | 0` |

### Knowledge Bases (`/v1/knowledge-base/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/v1/knowledge-base` | Get my knowledge base list | Pagination |
| `POST` | `/v1/knowledge-base/search`| Search knowledge base | Search queries |
| `POST` | `/v1/knowledge-base` | Create knowledge base | Params |
| `GET`  | `/v1/knowledge-base/{id}`| Get KB detail | None |
| `PUT`  | `/v1/knowledge-base/{id}`| Update KB | `{ title, description }` |
| `DELETE`| `/v1/knowledge-base/{id}`| Delete KB | None |
| `GET`  | `/v1/knowledge-base/{id}/documents`| Get KB documents | Pagination |
| `POST` | `/v1/knowledge-base/{id}/files`| Add files to KB | `{ files }` |

### Dataflow Conversation (`/v1/df-conversation/`)

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `POST` | `/v1/df-conversation/create`| Create agent conversation | `{ user_id, conversion_id, title, content }` |
| `GET`  | `/v1/df-conversation/list`| Get agent conversation list | `?page, page_size` |
| `GET`  | `/v1/df-conversation/{id}`| Get conversation details | None |
| `DELETE`| `/v1/df-conversation/{id}`| Delete conversation | None |

---

## Default Response Format

All successful responses are expected to follow a generic envelope structure:

```json
{
  "code": 0,
  "msg": "success",
  "message": "success", // fallback
  "data": {} // The actual payload (Array, Object, or Primitive)
}
```

Errors usually return `code != 0`, and UI displays the `message` field natively. Specific codes like `100002` trigger auto-redirects.

## Download File Parsing
The frontend supports standard Blob download via Axios. It checks if the `responseType` is `blob` or `arraybuffer`. If the backend returns a JSON error instead of a blob, the frontend attempts to read it using `await data.text()` and handles the JSON error message appropriately.
