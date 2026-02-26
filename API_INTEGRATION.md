# Frontend-Backend API Integration Guide

This document describes how the frontend and backend API integration works, including how to switch between mock data and real API.

## Architecture

### Overview

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Vue Pages     │──────│   API Service   │──────│  Data Source    │
│                 │      │   Layer         │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │                         │
                                │    ┌──────────────┐    │
                                ├───▶│ Config: mock │    │
                                │    └──────────────┘    │
                                │                         │
                                ▼                         ▼
                         ┌─────────────┐          ┌─────────────┐
                         │  Mock Data  │          │ Django API  │
                         │  (local JS) │          │  (backend)  │
                         └─────────────┘          └─────────────┘
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Data Mode Configuration
# Options: 'mock' | 'api'
VITE_DATA_MODE=mock

# Backend API Base URL
VITE_API_BASE_URL=http://localhost:8000
```

### Switching Data Mode

#### Method 1: Environment Variable (Recommended for build)

Set `VITE_DATA_MODE` in your `.env` file:
- `VITE_DATA_MODE=mock` - Use local mock data
- `VITE_DATA_MODE=api` - Use backend Django API

#### Method 2: Runtime Switch (Development)

```javascript
import { setDataMode } from '@/config'

// Switch to API mode
setDataMode('api')

// Switch back to mock mode
setDataMode('mock')
```

## API Service Layer

### Usage in Components

```javascript
import { taskApi, datasetApi } from '@/services/api.js'

// In your component
onMounted(async () => {
  // This automatically uses mock or API based on config
  const tasks = await taskApi.getTasks()
  console.log(tasks)
})
```

### Available APIs

| API | Methods |
|-----|---------|
| `taskApi` | `getTasks()`, `getTaskById(id)`, `getTaskStatus(id)` |
| `datasetApi` | `getDatasets()`, `getDatasetById(id)` |
| `dataflowApi` | `getPackages()`, `getPackageById(id)`, `getPipeline(taskId)`, `getExecutionResult(taskId)` |
| `knowledgeBaseApi` | `getKnowledgeBases()` |
| `modelApi` | `getModels()` |
| `spaceApi` | `getSpaces()` |

## Backend API Endpoints

### Implemented Sample Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v2/tasks` | GET | List all tasks |
| `/api/v2/tasks/<id>` | GET | Get task detail |
| `/api/v2/datasets` | GET | List all datasets |
| `/api/v2/datasets/<id>` | GET | Get dataset detail |
| `/api/v2/dataflow/packages` | GET | List DataFlow packages |
| `/api/v2/dataflow/packages/<id>` | GET | Get package detail |
| `/api/v2/knowledgebase` | GET | List knowledge bases |
| `/api/v2/knowledgebase/<id>` | GET | Get knowledge base detail |

## Development Workflow

### 1. Start with Mock Data (Default)

```bash
# No configuration needed - mock mode is default
npm run dev
```

### 2. Switch to API Mode

```bash
# Create .env file
echo "VITE_DATA_MODE=api" > .env

# Or use the example
cp .env.example .env

# Start dev server
npm run dev
```

### 3. Start Django Backend

```bash
cd backend
python manage.py runserver
```

## Adding New API Endpoints

### Frontend

1. Add method to appropriate service in `src/services/api.js`:

```javascript
export const myApi = {
  async getData() {
    if (isMockMode()) {
      const { myData } = await import('@/data/myData.js')
      return myData
    }
    
    const url = getApiUrl('/my-endpoint')
    const response = await fetchWithAuth(url)
    return response.data
  }
}
```

### Backend

1. Create or update `urls.py` in appropriate app
2. Add sample data and view functions
3. Register URL in `backend/core/urls.py`

## CORS Configuration

The backend is configured to allow all origins in DEBUG mode. For production:

```python
# backend/core/settings.py
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    # Add your production domain
]
```

## Authentication

Currently, API endpoints use `@permission_classes([AllowAny])` for demo purposes.

For production, change to:

```python
@permission_classes([IsAuthenticated])
```

And ensure the frontend sends the JWT token in the Authorization header.

## Troubleshooting

### API requests failing

1. Check if backend is running: `http://localhost:8000/health/`
2. Verify CORS settings in backend
3. Check browser console for error messages

### Mock data not loading

1. Verify `VITE_DATA_MODE=mock` in `.env`
2. Check that mock data files exist in `src/data/`

### Switch not working

1. Restart the dev server after changing `.env`
2. Check `src/config/index.js` for correct mode detection
