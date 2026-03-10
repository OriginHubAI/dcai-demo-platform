# Dataflow Agent Architecture & API Specification

> This document details the architecture and programmatic interfaces of the external `dataflow-agent` module. 

---

## Architectural Overview

Through deep code inspection, it's confirmed that `dataflow-agent` **does not expose a standard RESTful API** (e.g., using FastAPI, Django, or Flask) for its core agent functionalities. Instead, it is an SDK-first Python library wrapped with a native **Gradio Web UI**.

- **Core Framework**: Built on `LangChain`/`LangGraph`, providing a state-driven Multi-Agent system (e.g., PromptAgent, Pipeline Rec, Operator QA).
- **Presentation Layer**: Provided directly by `gradio_app/app.py`.
- **API Paradigm**: Programmatic integration is achieved via **Python SDK imports** or the implicit **Gradio Client API**, rather than decoupled HTTP microservices.

---

## Programmatic Integration (Python SDK)

The most robust way to interact with `dataflow-agent` from other backend services (like `dataflow-system`) is by importing it directly as a Python library.

### Workflow Execution API

All core agent processes are defined as "Workflows" registered via decorators and managed by the `RuntimeRegistry`.

**Endpoint / Function Call:**
```python
import asyncio
from dataflow_agent.workflow import run_workflow
from dataflow_agent.state import MainState

async def execute_agent():
    # 1. Initialize the required state
    state = MainState()
    
    # 2. Call the workflow by its registered name
    # Available workflows include: "operator_qa", "pipeline_recommend", etc.
    out_state = await run_workflow("operator_qa", state)
    
    return out_state
```

**Key Interfaces:**
- `dataflow_agent.workflow.list_workflows()`: Returns a list of all currently registered agent workflows.
- `dataflow_agent.workflow.get_workflow(name)`: Retrieves the graph factory for a specific workflow.
- `dataflow_agent.state.DFState` / `MainState`: The dataclass structures required as input payloads for these workflows.

---

## Gradio API Integration

When the Gradio app (`gradio_app/app.py`) is running (default port: `7860`), it implicitly exposes WebSocket and HTTP endpoints.

However, because specific `api_name` parameters are **not defined** on the Gradio components in the codebase, the endpoints are dynamically generated (e.g., `/api/predict_1`, `/api/predict_2`). 

*Note: It is highly recommended to use the Python SDK (`run_workflow`) instead of HTTP requests to the Gradio server for backend-to-backend integrations due to the fragility of anonymous Gradio endpoints.*

---

## Standalone Utilities (FastAPI)

The module does contain one standalone FastAPI microservice used exclusively as a utility, not for agent logic:

### Generic Model Load Balancer
Located at `dataflow_agent/toolkits/model_servers/generic_lb.py`.
- **Purpose**: A round-robin proxy for multiple backend LLM endpoints.
- **Route**: `/{path_name:path}` (Accepts all methods).
- **Execution**: `python generic_lb.py --backends http://llm1 http://llm2 --port 8000`