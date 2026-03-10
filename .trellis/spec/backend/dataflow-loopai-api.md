# Dataflow LoopAI API Specification

> This document details the required backend API endpoints, payload structures, and configuration used by the `dataflow-loopai` module. This module provides LLM remote training (via LLaMA Factory) and orchestrates LoopAI agent tasks.

---

## Service Overview

The Dataflow LoopAI backend is a FastAPI application integrating LangGraph for agent orchestration and `subprocess` based execution for LLaMA Factory model training tasks. It connects to a SQLite database (`db/db.sqlite3`) using Tortoise ORM.

### Authentication
Currently, the LoopAI backend operates as an internal microservice and uses a basic CORS configuration without strict token-based authentication (relying on `allow_origins=["*"]`). It is intended to be called by the `dataflow-webui` or proxy services.

---

## API Endpoints by Module

### 1. Training & Execution (`/train`)
Responsible for submitting and managing LLaMA Factory and vERL training tasks remotely.

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `POST` | `/train/` | Start a training task via JSON | `{ config, task_name, framework, config_path }` |
| `POST` | `/train/upload` | Start training via YAML upload | `file` (form-data), `task_name` |
| `GET`  | `/train/status/{task_id}` | Check real-time task status | None |
| `GET`  | `/train/logs/{task_id}` | Fetch training logs | `?max_lines={int}` |
| `GET`  | `/train/tasks` | Get all training tasks | None |
| `DELETE`| `/train/tasks/{task_id}` | Cancel/delete training task | None |
| `GET`  | `/train/swanlab-logs/{task_id}` | Get specific SwanLab log path | None |
| `GET`  | `/train/swanlab-logs` | Get all SwanLab logs | None |
| `GET`  | `/train/metrics/{task_id}` | Get training metrics | `?count={int}` |
| `GET`  | `/train/metrics/{task_id}/file`| Get metrics JSON file | None |
| `DELETE`| `/train/metrics/{task_id}` | Cleanup task metrics | None |

### 2. Starter / Agent Orchestration (`/starter`)
Manages the LangGraph agent state machines and agent memory/events.

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `POST` | `/starter/agent/start` | Start the agent for a task | `?task_id={str}` |
| `POST` | `/starter/agent/input` | Send input to agent | `?text={str}` |
| `POST` | `/starter/agent/stop` | Stop the running agent | None |
| `GET`  | `/starter/agent/status` | Get current agent status | None |
| `GET`  | `/starter/agent/messages` | Get agent message history | None |
| `GET`  | `/starter/agent/message/stream`| Stream agent messages (SSE) | None |

### 3. Task Management (`/task`)
Maintains metadata regarding AI workflows and LoopAI tasks.

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/task/list_tasks` | List all tasks | `?search, offset, limit` |
| `GET`  | `/task/task/{task_id}` | Get task by ID | None |
| `POST` | `/task/task` | Create a new task | `{ name, config, state }` |
| `PUT`  | `/task/task` | Update task details | `{ id, name, config }` |
| `DELETE`| `/task/task/{id}` | Delete task by ID | None |

### 4. Configuration (`/config`)
Manages the `StarterConfig` and file system directory validation.

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/config/config` | Get Starter/system config | None |
| `POST` | `/config/config` | Update config | `{ id, config }` |
| `GET`  | `/config/state_schema` | Get LangGraph state schema | None |
| `GET`  | `/config/list_dir` | Browse directories | `?path={str}` |

### 5. Resources (`/resource`)
Handles dataset and text resources indexing.

| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/resource/resource` | Get resource list | `?search, offset, limit` |
| `GET`  | `/resource/resource/count` | Get resource count | `?search` |
| `POST` | `/resource/resource` | Create resource | `?name, description, path, res_type` |
| `PUT`  | `/resource/resource/{resource_id}`| Update resource | `{ name, path, status, file_type, res_type }` |
| `DELETE`| `/resource/resource/{resource_id}`| Delete resource | None |
| `POST` | `/resource/resource/preview` | Preview content (JSONL/CSV/TXT)| `?resource_id={str}, offset, limit` |

### 6. System
| Method | Endpoint | Description | Payload |
|--------|----------|-------------|---------|
| `GET`  | `/health` | Health check & directory status | None |

---

## Technical Considerations

1. **Background Processes**: The `/train` API spins up completely detached `subprocess.Popen` threads to run the LLaMA Factory CLI. Processes are automatically killed (`os.killpg`) upon FastAPI shutdown.
2. **Stream Events**: The `/starter/agent/message/stream` endpoint returns a Server-Sent Events (SSE) stream (`text/event-stream`), utilized for real-time agent monitoring.
3. **Database**: Relies on `sqlite` using Tortoise ORM with automatic schema generation (`generate_schemas=True`) upon boot.
