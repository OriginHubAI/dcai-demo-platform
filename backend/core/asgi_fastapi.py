"""
ASGI Configuration with FastAPI mounted alongside Django
This allows running Django and FastAPI on the same port
"""
import os
import django
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.asgi import get_asgi_application

# Create FastAPI application
fastapi_app = FastAPI(
    title="FastAPI Backend",
    description="FastAPI implementation for specific endpoints",
    version="2.0.0",
)

# Add CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Example FastAPI endpoints - migrate your logic here
@fastapi_app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fastapi"}


@fastapi_app.get("/agents")
async def list_agents():
    """List agents - example endpoint"""
    # Import Django models here after django.setup()
    from agent.models import Agent
    agents = Agent.objects.all()
    return [{"id": a.id, "name": a.name} for a in agents]


# Get Django ASGI application
django_app = get_asgi_application()

# Combine both applications using Starlette
# Routes starting with /api/v2/fastapi go to FastAPI
# All other routes go to Django
application = Starlette(routes=[
    Mount("/api/v2/fastapi", app=fastapi_app),
    Mount("/", app=django_app),
])
