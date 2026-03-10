# Backend Development Guidelines Index

> **Tech Stack**: Django + Django REST Framework + PostgreSQL (MyScale) + Redis. Secondary services loosely coupled via FastAPI proxying.

---

## Documentation Files

| File                                               | Description                                       | When to Read                       |
| -------------------------------------------------- | ------------------------------------------------- | ---------------------------------- |
| [directory-structure.md](./directory-structure.md) | Django App structure and domain organization      | Starting a new feature/app             |
| [api-module.md](./api-module.md)                   | Model-View-Serializer pattern (types, procedures) | Creating/modifying API Modules |
| [api-patterns.md](./api-patterns.md)               | Common Django API patterns & Proxy patterns      | Implementing CRUD, Proxying External Apps |
| [error-handling.md](./error-handling.md)           | Exception handling in Django and DRF Transactions | Designing service logic robustness |
| [database.md](./database.md)                       | Django ORM, schema, performance (select_related)  | Database operations & Query optimization |
| [environment.md](./environment.md)                 | Environment setup & Configuration properties       | Handling Deployment Environments |
| [logging.md](./logging.md)                         | Python `logging` module and structlog integration | Debugging in Cloud architectures   |
| [pagination.md](./pagination.md)                   | DRF Pagination Classes (`PageNumber`, `Cursor`)   | Implementing large list APIs       |
| [quality.md](./quality.md)                         | Python linting, `pytest`, imports, code quality   | Formatting code and writing tests |
| [type-safety.md](./type-safety.md)                 | Python Type Hinting guidelines (`mypy`)          | Writing robust Python methods        |
| [fastapi.md](./fastapi.md)                         | FastAPI microservice & data plane development     | Building FastAPI Type-B services   |
| [authentication.md](./authentication.md)             | Token based Auth across microservices             | Dealing with Auth / Permissions   |
| [hf-datasets-api.md](./hf-datasets-api.md)         | Hugging Face Datasets 核心接口与使用文档          | Implementing Dataset integrations |
| [dataflow-webui-api.md](./dataflow-webui-api.md)   | Dataflow WebUI Backend API Specification         | Implementing backend for Dataflow WebUI |

---

## Core Rules Summary

| Rule                                                           | Reference                                      |
| -------------------------------------------------------------- | ---------------------------------------------- |
| **All views map to apps. Include App urls to core/urls**             | [directory-structure.md](./directory-structure.md)             |
| **Never use raw strings in settings, use django-environ(.env)**  | [environment.md](./environment.md)             |
| **Never skip DRF Serializer validation**                       | [api-module.md](./api-module.md)               |
| **Keep Views thin, handle complex biz logic in services.py**     | [api-module.md](./api-module.md)               |
| **If proxying another local port, use async httpx**              | [api-patterns.md](./api-patterns.md)       |
| **Catch and raise APIException for logic failure**               | [error-handling.md](./error-handling.md)       |
| **PostgreSQL is source of truth, but Vectors go to MyScale**     | [database.md](./database.md)                   |
| **Use CursorPagination for infinite scrolling Lists**            | [pagination.md](./pagination.md)               |
| **Use Type Annotations on all new Python methods**               | [type-safety.md](./type-safety.md)             |
| **Format with Black, lint with Ruff/Flake8**                   | [quality.md](./quality.md)                   |
| **Pass JWT properly via headers to Sub-Agents and Apps**| [authentication.md](./authentication.md) |
| **Use Pydantic schemas for FastAPI validation**                | [fastapi.md](./fastapi.md)                     |

---

**Language**: All documentation must be written in **English**.
