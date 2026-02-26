# Sci-DCAI Platform

A Hugging Face-style AI community platform built with Vue 3 + Vite (Frontend) and Django + FastAPI (Backend). Browse models, datasets, and apps with search, filtering, sorting, and pagination.

## Table of Contents

- [Sci-DCAI Platform](#sci-dcai-platform)
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
      - [Using API Mode](#using-api-mode)
  - [API Documentation](#api-documentation)
    - [API Endpoints](#api-endpoints)
  - [Contributing](#contributing)

## Project Overview

Sci-DCAI (Scientific Data-Centric AI) Platform is a comprehensive AI community hub that provides:

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

#### Using API Mode

To use the real backend API instead of mock data:

1. Update your `.env` file:
   ```env
   VITE_DATA_MODE=api
   VITE_API_BASE_URL=http://localhost:8000
   ```

2. Start both frontend and backend servers

3. Restart the frontend to apply new environment variables

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
