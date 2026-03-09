# Type Safety Guidelines

> Type safety patterns for Python 3.9+ using explicit typing and Mypy.

---

## Why Type Hints?

While Python is dynamically typed, type hinting drastically improves code navigation, helps developers catch bugs early (via `mypy` or LSP tools), and auto-documents code.

```python
# WRONG
def process_task(task_id, payload):
    # Hard to tell what types these are without reading internal method logic
    return db_save(task_id, payload)

# CORRECT
from uuid import UUID

def process_task(task_id: UUID, payload: dict) -> bool:
    # Explicit types. IDE will warn if you pass a string instead of UUID
    return db_save(task_id, payload)
```

---

## Handling Optionals

If a function can return `None`, you must signify it.

```python
from typing import Optional
from .models import User

# CORRECT
def get_user_by_email(email: str) -> Optional[User]:
    return User.objects.filter(email=email).first()

client = get_user_by_email("test@example.com")
if client:
    print(client.id) # Safe
```

---

## Advanced Typing (dataclasses / Pydantic)

For complex data structures (especially those coming from or going to Proxied FastAPI services), use standard library `dataclasses` or `pydantic`.

```python
from pydantic import BaseModel
from typing import List

class AgentToolParams(BaseModel):
    name: str
    openapi_url: str

class AgentConfig(BaseModel):
    title: str
    tools: List[AgentToolParams]

# Utilizing it in a Service
def deploy_agent(config_data: dict) -> bool:
    # This automatically validates and provides dot-notation autocomplete!
    config = AgentConfig(**config_data)
    print(config.tools[0].name)
    return True
```

---

## Type Hints in Django Views vs Services

Usually, DRF Serializers handle the "typing" at the View layer. It is most crucial to strictly type the `services.py` layer.

```python
# backend/project/services.py
from django.db.models import QuerySet
from .models import Project

def get_active_projects() -> QuerySet[Project]:
    return Project.objects.filter(status='active')
```

*(Note for `QuerySet`: using `django-stubs` provides support for generically typing QuerySets like `QuerySet[Project]`)*.

---

## Avoiding `Any`

Using `Any` defeats the purpose of the type checker. Try to use built-in collection types (`dict`, `list`, `set`) or specify `unknown` patterns via generic type parameters if absolutely necessary.

```python
from typing import Any

# WRONG
def raw_sql_execute(query: str) -> Any: ...

# BETTER
def raw_sql_execute(query: str) -> list[dict]: ...
```

---

## Summary

| Rule                        | Reason                 |
| --------------------------- | ---------------------- |
| Type hint all service funcs | Self-documenting code  |
| Understand `Optional[T]`    | Prevents `AttributeError: NoneType` |
| Use `pydantic` or `dataclass`| Strong validation for internal payloads |
| Explicit return types       | Mypy can infer better  |
| Avoid `Any` when possible   | Type safety            |
