# Directory Structure

> Domain-driven directory layout for the Django Backend Server.

---

## Backend Application Structure

The DCAI Backend is built around Django but incorporates modern microservice and API gateway concepts.

```
backend/
├── manage.py             # Django entry point
├── requirements.txt      # Python dependencies
├── core/                 # Core settings, URL routing, and global configs (Main Django Box)
│   ├── settings.py       # Global Django settings
│   ├── urls.py           # Root URL dispatcher
│   ├── asgi.py           # ASGI config (for WebSockets / async apps)
│   └── wsgi.py           # WSGI config for sync deployment
├── agent/                # Domain App: Agent routing & management
├── apps/                 # Domain App: Type A Spaces/Apps
├── chat/                 # Domain App: Chat history, conversations, sharing
├── collection/           # Domain App: User Collections
├── customadmin/          # Domain App: Custom Django admin interface overrides
├── dataflow/             # Domain App: Proxies DataFlow-System endpoints
├── dataset/              # Domain App: High-performance metadata and MyScale linkage
├── document/             # Domain App: Document chunking and management
├── knowledgebase/        # Domain App: Knowledge bases UI logic
├── llm_chat/             # Domain App: Large Language Model proxying
├── organization/         # Domain App: RBAC, Teams, and Orgs
├── user/                 # Domain App: Custom User models, Auth, JWT, GitHub/WeChat OAuth
└── third_party/          # Integrations: AliYun Bailian, LangChain wrappers, etc.
```

---

## Inside a Domain App Folder

A standard App generally follows the MVC/MTV structure enhanced with Service layers for logic:

```
backend/{domain}/
├── __init__.py           
├── apps.py               # App configuration
├── models.py             # Database models (Data Layer)
├── urls.py               # Route dispatcher for this domain
├── views.py              # HTTP Endpoints (View Layer)
├── serializers.py        # Request validation and serialization formatting
├── services.py           # Business Rules / Cross-model operations / API Proxy calls
├── permissions.py        # Optional: Custom DRF permission classes
├── tasks.py              # Optional: Celery async tasks (e.g., background document processing)
└── tests/                # Testing directory
    ├── conftest.py       # Pytest fixtures
    ├── test_models.py
    ├── test_views.py
    └── test_services.py
```

---

## Domain Examples & Responsibilities

| Domain          | Description                                         | Example Responsibilities                            |
| --------------- | --------------------------------------------------- | --------------------------------------------------- |
| `user`          | User identity & Authentication                      | Login, Register, Refresh Token, WeChat/GitHub OAuth |
| `agent`         | Tool and Agent configuration                        | Agent creation, Tool URLs, routing via SubAgents    |
| `dataflow`      | Interactions with the DataFlow-System FastAPI Server| Operator retrieval, Code-Server lifecycle proxying  |
| `dataset`       | Linking S3/LakeFS with structured Metadata          | Listing datasets, interacting with LakeFS API       |
| `chat`          | User conversations via DataMaster                   | Conversation history, stream responses              |

---

## Test Directory Structure (Pytest)

Maintain tests near the code they are testing within the App's `tests/` directory. Use Pytest + `pytest-django`.

```
backend/{domain}/tests/
├── factories/            # Factory Boy factories (Optional)
│   ├── __init__.py
│   └── user_factory.py
├── test_models.py        # ORM / Constraint testing
├── test_views.py         # Testing ViewSets and API Endpoints (Integration style) 
├── test_services.py      # Testing isolated business logic (Unit style)
└── test_serializers.py   # Explicit validation tests
```

---

## Test File Naming Convention

| Type                | Location                      | Naming                          |
| ------------------- | ----------------------------- | ------------------------------- |
| Models test         | `backend/{domain}/tests/`     | `test_models.py`                |
| Views test          | `backend/{domain}/tests/`     | `test_views.py`                 |
| Services test       | `backend/{domain}/tests/`     | `test_services.py`              |
| Celery Tasks test   | `backend/{domain}/tests/`     | `test_tasks.py`                 |

---

## Key Principles

1. **One folder per domain** - Each business domain is encapsulated in an installed Django app.
2. **urls.py registers app routes** - The `core/urls.py` simply `includes` the domain `urls.py`.
3. **Views contain no business logic** - Keep Views light. Extract logic into `services.py`.
4. **Celery tasks go in tasks.py** - Django automatically discovers celery background workers by inspecting `tasks.py`.
5. **Serializers do validation** - All input checking happens there.

---

## When to Create a New Domain App

Create a new domain app (`python manage.py startapp {domain}`) when:
- You have a fundamentally new business concept (e.g., launching a "billing" service).
- The models and views naturally bundle together and shouldn't bloat an existing module.

Do NOT create a new domain for:
- Scripts or common utilities. Put these in a generic `core/` or `utils/` app instead.
