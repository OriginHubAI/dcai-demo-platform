# DCAI Platform

A Hugging Face-style AI community platform built with Vue 3 + Vite (Frontend) and Django + FastAPI (Backend). Browse models, datasets, and apps with search, filtering, sorting, and pagination.

## Table of Contents

- [DCAI Platform](#dcai-platform)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Tech Stack](#tech-stack)
    - [Frontend](#frontend)
    - [Backend](#backend)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Environment Configuration](#environment-configuration)
    - [Frontend Development](#frontend-development)
    - [Backend Development](#backend-development)
      - [Running Backend Tests](#running-backend-tests)
      - [Using API Mode](#using-api-mode)
    - [DataFlow-WebUI Integration (ASGI Mode)](#dataflow-webui-integration-asgi-mode)
  - [Docker Environment](#docker-environment)
  - [API Documentation](#api-documentation)
    - [API Endpoints](#api-endpoints)
  - [Contributing](#contributing)

## Project Overview

DCAI (Data-Centric AI) Platform is a comprehensive AI community hub that provides:

- **Models**: Browse and discover AI models for various tasks
- **Datasets**: Access and share datasets for training and evaluation
- **Apps**: Interactive AI applications powered by open-source models
- **DataFlow**: Visual workflow builder for data processing pipelines
- **Knowledge Bases**: Manage and query knowledge bases with vector search

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework with Composition API
- **Vue Router 4** - Client-side routing
- **Vue I18n** - Internationalization support (English, Chinese, Traditional Chinese)
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Next-generation frontend build tool

### Backend
- **Django** - High-level Python web framework
- **Django REST Framework** - Powerful API toolkit
- **FastAPI** - Modern, fast web framework for APIs (hybrid setup)
- **SQLite/PostgreSQL** - Database (SQLite for dev, PostgreSQL for production)
- **Redis** - Caching and message broker
- **Celery** - Distributed task queue

## Project Structure

```
.
├── frontend/                     # Frontend source code
│   ├── assets/                   # Static assets (CSS, images)
│   ├── components/               # Vue components
│   │   ├── apps/                 # App-related components
│   │   ├── common/               # Common/reusable components
│   │   ├── dataflow/             # DataFlow components
│   │   ├── datasets/             # Dataset components
│   │   ├── home/                 # Home page sections
│   │   ├── knowledgeBase/        # Knowledge base components
│   │   ├── layout/               # Layout components (Header, Footer, Nav)
│   │   └── models/               # Model components
│   ├── composables/              # Vue composition functions
│   ├── config/                   # Configuration files
│   ├── data/                     # Mock data files
│   ├── i18n/                     # Internationalization
│   │   └── locales/              # Translation files
│   ├── router/                   # Vue Router configuration
│   ├── services/                 # API service layer
│   ├── views/                    # Page components
│   ├── App.vue                   # Root component
│   └── main.js                   # Entry point
│
├── backend/                      # Backend source code
│   ├── agent/                    # AI Agent module
│   ├── apps/                     # Apps module (Spaces renamed to Apps)
│   ├── chat/                     # Chat module
│   ├── collection/               # Collections module
│   ├── core/                     # Core settings and config
│   ├── customadmin/              # Custom admin module
│   ├── dataflow/                 # DataFlow module
│   ├── dataset/                  # Dataset module
│   ├── df_conversation/          # DataFlow conversation module
│   ├── document/                 # Document module
│   ├── fastapi_app/              # FastAPI application
│   ├── knowledgebase/            # Knowledge base module
│   ├── llm_chat/                 # LLM chat module
│   ├── openapi/                  # OpenAPI module
│   ├── organization/             # Organization module
│   ├── systemconfig/             # System configuration module
│   ├── task/                     # Task management module
│   ├── template/                 # Template module
│   ├── third_party/              # Third-party integrations
│   ├── train/                    # Training module
│   ├── user/                     # User management module
│   ├── manage.py                 # Django management script
│   └── requirements.txt          # Python dependencies
│
├── public/                       # Public static files
├── index.html                    # HTML entry point
├── package.json                  # Node.js dependencies
├── vite.config.js                # Vite configuration
├── tailwind.config.js            # Tailwind CSS configuration
└── .env.example                  # Environment variables template
```

## Getting Started

### Prerequisites

- **Node.js** v18 or later
- **npm** (comes with Node.js)
- **Python** 3.8 or later
- **pip** (comes with Python)
- **Redis** (optional, for caching and Celery)

### Environment Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Configure the environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_DATA_MODE` | Data source mode: `mock` or `api` | `mock` |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |
| `ENABLE_MOCK_DATAFLOW` | Auto-start mock Dataflow server | `False` |
| `DATAFLOW_MOCK_URL` | Mock Dataflow proxy base URL | `http://localhost:8001` |
| `DATAFLOW_SYSTEM_URL` | Dataflow system URL | `http://127.0.0.1:8001` |
| `ENABLE_MOCK_HF_DATASETS` | Auto-start mock Hugging Face Hub server | `False` |
| `HF_DATASETS_MOCK_URL` | Mock HF server base URL | `http://localhost:8010` |
| `HF_ENDPOINT` | Endpoint for 'datasets' library | `http://localhost:8010` |
| `DATAFLOW_BACKEND_URL` | Dataflow backend service URL | `http://127.0.0.1:8002` |
| `LOOPAI_BACKEND_URL` | LoopAI backend service URL | `http://127.0.0.1:18003` |
| `DFAGENT_BACKEND_URL` | DFAgent backend service URL | `http://127.0.0.1:7860` |
| `DATAFLOW_REPO_ROOT` | Absolute path to DataFlow repository | `/absolute/path/to/DataFlow` |
| `DATAFLOW_OPERATORS_ROOT` | Absolute path to DataFlow operators | `/absolute/path/to/DataFlow/dataflow/operators` |
| `CODE_SERVER_BASE_PORT` | Base port for Code Server instances | `18080` |
| `PACKAGE_EDITOR_PORT` | Port for the Package Editor service | `18004` |
| `PACKAGE_EDITOR_SANDBOX_ROOT` | Directory for Package Editor sandboxes | `/absolute/path/to/sandboxes/package-editor` |
| `PROXY_TIMEOUT` | Proxy request timeout in seconds | `120` |
| `LLM_PROVIDER_BASE_URL` | LLM Provider Base URL | `http://localhost:3000` |
| `LLM_PROVIDER_API_KEY` | LLM Provider API Key | `your-api-key` |
| `LLM_DEFAULT_MODEL` | Default LLM model | `gpt-4o` |
| `LLM_AVAILABLE_MODELS` | Comma-separated list of available models | `gpt-4o,deepseek-chat` |
| `LLM_REQUEST_TIMEOUT` | LLM API request timeout in seconds | `120` |

### Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173).

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend Development

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8000
```

#### Running Backend Tests

The backend uses Django's test runner and includes integration tests for mock systems. 

A 16GB memory limit is automatically enforced when running tests if `TEST_MEMORY_LIMIT_GB=16` is set in your `.env` (configured via `manage.py`).

```bash
cd backend

# Run all tests (memory limit enforced via manage.py)
python manage.py test

# Run specific module tests
python manage.py test dataflow.tests  # Dataflow integration tests
python manage.py test dataset.tests   # Hugging Face mock server tests
python manage.py test user.tests      # User and Auth tests
```

> **Note**: Integration tests for `dataflow` and `dataset` automatically start their respective mock FastAPI servers if they are not already running. Ensure `ENABLE_MOCK_DATAFLOW=True` or `ENABLE_MOCK_HF_DATASETS=True` in your `.env` is NOT required for running tests specifically, as the test runner handles server lifecycle, but it IS required for these systems to work during regular `runserver` development.

#### Using API Mode

To use the real backend API instead of mock data:

1. Update your `.env` file:
   ```env
   VITE_DATA_MODE=api
   VITE_API_BASE_URL=http://localhost:8000
   ```

2. Start both frontend and backend servers

3. Restart the frontend to apply new environment variables

## DataFlow-WebUI Integration (ASGI Mode)

DataFlow-WebUI is embedded directly into dcai-platform via a single-process ASGI dispatcher — no separate DataFlow-WebUI service is needed.

**Route ownership (handled by `backend/core/asgi.py`):**

| Path | Handler |
|------|---------|
| `/embedded/dataflow-webui/*` | DataFlow-WebUI React frontend (FastAPI static files) |
| `/api/v1/*` | DataFlow-WebUI backend API (FastAPI, in-iframe calls) |
| `/api/v2/dataflow/pipelines/*` … | DataFlow-WebUI compat (path rewritten to `/api/v1/`) |
| `/api/hf/*` | dcai-platform HF datasets service (Django) |
| everything else | Django |

### Step 1 — Build DataFlow-WebUI frontend (one-time)

```bash
cd ../DCAI-DataFlow-WebUI/frontend
npx vite build --mode embedded
# Output: DCAI-DataFlow-WebUI/frontend/dist/  (served by FastAPI)
```

### Step 2 — Start the ASGI server

```bash
cd backend

# Install dependencies (first time)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start unified ASGI server (Django + DataFlow-WebUI FastAPI in one process)
uvicorn core.asgi:application --host 0.0.0.0 --port 18000
```

> **Note**: The default `EXTERNAL_HF_API_URL` is `http://localhost:18000/api/hf`.
> If you run on a different port, set this env var to match:
> ```bash
> EXTERNAL_HF_API_URL=http://localhost:8000/api/hf uvicorn core.asgi:application --port 8000
> ```

### Step 3 — Start dcai-platform frontend (dev mode)

```bash
# from project root
npm run dev
# Vite dev server proxies /api and /embedded/* to http://127.0.0.1:18000
```

### DataFlow-WebUI location

The ASGI dispatcher resolves DataFlow-WebUI's backend via the `DATAFLOW_WEBUI_BACKEND_DIR` env var.
Default: `<dcai-platform>/../DCAI-DataFlow-WebUI/backend`.
Override if your directory layout differs:

```bash
DATAFLOW_WEBUI_BACKEND_DIR=/path/to/DCAI-DataFlow-WebUI/backend uvicorn core.asgi:application ...
```

If the directory is not found, the server starts normally with DataFlow-WebUI disabled (pure Django ASGI).

---

## Docker Environment

### Building the Image

From the project root, run:

```bash
docker build -t dcai-sandbox -f sandbox/Dockerfile .
```

The image includes:
- Python 3.12
- Node.js 22
- Gemini CLI (`@google/gemini-cli`)
- Project backend dependencies

### Direct Docker Access

For direct interactive access to the sandbox environment with host network and 24GB memory, add this function to your `~/.bashrc` or `~/.bash_aliases`:

```bash
function dcai_docker() {
    local mem="16g"
    # 在宿主机层面预先格式化好欢迎行，避免在 docker 命令内部嵌套过于复杂的转义
    local info="   User: $USER | Mem: ${mem^^} | Net: Host"

    docker run -it --rm \
        --network host \
        --add-host=host.docker.internal:127.0.0.1 \
        -v /etc/passwd:/etc/passwd:ro \
        -v /etc/group:/etc/group:ro \
        -v "$HOME":"$HOME" \
        -u $(id -u):$(id -g) \
        -w "$(pwd)" \
        -e HOME="$HOME" \
        -e TERM=xterm-256color \
        -e COLORTERM=truecolor \
        -e LANG=C.UTF-8 \
        -e LC_ALL=C.UTF-8 \
        -e HTTPS_PROXY="$HTTPS_PROXY" \
        -e HTTP_PROXY="$HTTP_PROXY" \
        --memory="$mem" \
        dcai-sandbox /bin/bash -c "
            L='------------------------------------------------------------'
            printf '\e[1;36m%s\e[0m\n' \"\$L\"
            printf '\e[1;32m   🚀 Welcome to DCAI Docker Sandbox\e[0m\n'
            printf '\e[1;34m%s\e[0m\n' \"$info\"
            printf '\e[1;36m%s\e[0m\n' \"\$L\"
            exec /bin/bash
        "
}
```

## API Documentation

When the backend is running, API documentation is available at:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/` | API v1 endpoints |
| `/api/v2/` | API v2 endpoints |
| `/api/v2/apps` | Apps listing |
| `/api/v2/datasets` | Datasets listing |
| `/api/v2/tasks` | Tasks management |
| `/admin/` | Django admin interface |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
