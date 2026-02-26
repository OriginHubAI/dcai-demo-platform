# DCAI Platform Frontend

A Hugging Face-style AI community hub built with Vue 3, Vite, and Tailwind CSS. Browse models, datasets, and spaces with search, filtering, sorting, and pagination.

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)
- npm (comes with Node.js)
- Python 3.8+ (for backend)
- pip (comes with Python)

## Environment Configuration

This project uses a `.env` file for configuration. Before running the application:

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Configure the environment variables in `.env`:

| Variable | Description | Options |
|----------|-------------|---------|
| `VITE_DATA_MODE` | Data source mode | `mock` - Use local mock data (default) <br> `api` - Use backend Django API |
| `VITE_API_BASE_URL` | Backend API base URL | Default: `http://localhost:8000` |

### Example `.env` file

```env
# Data Mode Configuration
VITE_DATA_MODE=mock

# Backend API Base URL
VITE_API_BASE_URL=http://localhost:8000
```

## Getting Started

### Frontend Development

#### Install dependencies

```bash
npm install
```

#### Run the development server

```bash
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173) (default Vite port).

### Build for production

```bash
npm run build
```

Output is written to the `dist/` directory.

### Preview the production build

```bash
npm run preview
```

## Backend Development

The backend is built with Django and FastAPI. Navigate to the `backend` directory to set up and run the backend server.

### Backend Prerequisites

- Python 3.8 or later
- pip
- Virtual environment (recommended)

### Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Running Backend with Frontend (API Mode)

To use the real backend API instead of mock data:

1. Update your `.env` file to use API mode:
   ```env
   VITE_DATA_MODE=api
   VITE_API_BASE_URL=http://localhost:8000
   ```

2. Start the Django backend server:
   ```bash
   cd backend
   python manage.py runserver 0.0.0.0:8000
   ```

3. Restart the frontend development server to apply the new environment variables.

### Database Migrations

If you're setting up the backend for the first time or after model changes:

```bash
cd backend
python manage.py migrate
```

## Tech Stack

- **Vue 3** (Composition API with `<script setup>`)
- **Vue Router 4** for client-side routing
- **Tailwind CSS** for utility-first styling
- **Vite** for development and bundling
