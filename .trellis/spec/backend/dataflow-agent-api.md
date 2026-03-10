# Dataflow Agent Architecture & API Specification

> This document details the architecture and API exposure of the external `dataflow-agent` module. 

---

## Architectural Overview

Unlike typical backend microservices (like `dataflow-loopai` or `dataflow-system`) which expose standard RESTful APIs (e.g., via FastAPI or Django), the `dataflow-agent` module is built natively as an **interactive AI Agent platform utilizing Gradio**.

- **Core Framework**: State-driven, modular AI Agent framework for DataFlow.
- **Presentation Layer**: The UI and interaction layer are provided directly by `gradio_app/app.py`.
- **Primary Function**: It orchestrates dataflow and operator tasks including PromptAgent Frontend, Op Assemble Line, Operator QA, Operator Write, Pipeline Rec, and Web Collection.

---

## API Endpoints & Exposure

The `dataflow-agent` **does not** expose standard, decoupled REST API endpoints (like `/v1/task` or `/v1/train`) intended for consumption by an external frontend (like `dataflow-webui`). 

Instead, it relies on the internal API endpoints generated automatically by the **Gradio Server**.

### Gradio API Integration

When `gradio_app/app.py` is launched (default port: `7860`), Gradio automatically creates an internal `/api/` routing schema (such as `/api/predict`) to handle websocket connections and HTTP requests between its frontend interface and the python backend functions.

If another system needs to invoke the agents programmatically, it can do so in two ways:
1. **Python API**: Import the core workflows directly into another Python service (e.g., using `dataflow_agent.workflow.run_workflow`).
2. **Gradio Client**: Use the `gradio_client` Python or JS library to programmatically interact with the exposed Gradio API endpoints.

---

## Toolkits & Utilities

While the core application relies on Gradio, the module contains some standalone API utilities:

### Generic Model Load Balancer
Located at `dataflow_agent/toolkits/model_servers/generic_lb.py`.
It spins up a lightweight `FastAPI` application that acts as a round-robin proxy for multiple backend model servers.
- **Endpoint**: `/{path_name:path}`
- **Methods**: All HTTP methods
- **Functionality**: Forwards requests strictly to the configured `BACKEND_URLS` via `httpx`.