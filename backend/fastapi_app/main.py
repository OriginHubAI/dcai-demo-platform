"""
Standalone FastAPI Application
Run with: uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload
"""
import os
import sys

# Add parent directory to path to import Django models
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import Django models after setup
from agent.models import Agent
from task.models import Task

app = FastAPI(
    title="FastAPI Backend",
    description="High-performance API endpoints migrated from Django",
    version="2.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Pydantic Schemas ==============

class AgentSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: int
    title: str
    status: str
    
    class Config:
        from_attributes = True


# ============== Agent Endpoints ==============

@app.get("/api/v2/agents", response_model=List[AgentSchema])
async def list_agents():
    """List all agents"""
    agents = Agent.objects.all()
    return list(agents)


@app.get("/api/v2/agents/{agent_id}", response_model=AgentSchema)
async def get_agent(agent_id: int):
    """Get a specific agent"""
    try:
        agent = Agent.objects.get(id=agent_id)
        return agent
    except Agent.DoesNotExist:
        raise HTTPException(status_code=404, detail="Agent not found")


# ============== Task Endpoints ==============

@app.get("/api/v2/tasks", response_model=List[TaskSchema])
async def list_tasks():
    """List all tasks"""
    tasks = Task.objects.all()
    return list(tasks)


@app.get("/api/v2/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: int):
    """Get a specific task"""
    try:
        task = Task.objects.get(id=task_id)
        return task
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")


# ============== Health Check ==============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fastapi", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
