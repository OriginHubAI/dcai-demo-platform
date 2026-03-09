# Code Quality & Import Guidelines

> Quality standards for Python, Django, and the broader DCAI backend.

---

## Import Path Rules

### Absolute Imports

Always use absolute imports based on the Django project root.

```python
# CORRECT - src/backend/project/services.py
from project.models import Project
from core.exceptions import CustomAPIException

# WRONG - Relative imports make refactoring harder and can cause circular dependency issues
from .models import Project
from ..core.exceptions import CustomAPIException
```

### Import Ordering (isort)

Imports should be grouped in the following order:
1. Standard library imports (e.g. `import os`, `import sys`)
2. Related third party imports (e.g. `import django`, `import rest_framework`)
3. Local application/library specific imports

Using `isort` will automatically organize this for you.

---

## Quality Guidelines

### Style and Formatting

We follow **PEP 8** standards.

- **Formatter**: `Black` (line length of 88 or 100).
- **Linter**: `Flake8` or `Ruff`.
- **Type Checker**: `mypy`.

Before committing, ensure your code passes styling checks. Let CI/CD or your pre-commit hooks handle formatting seamlessly.

### Forbidden Patterns

| Pattern                        | Reason                | Alternative                   |
| ------------------------------ | --------------------- | ----------------------------- |
| `except Exception:` blindly    | Swallows tracebacks   | `logger.exception()` or specific errors  |
| Raw strings for settings       | Security/Rigidity     | `django.conf.settings` or `.env`    |
| `import *`                     | Namespace pollution   | Explicitly name your imports  |
| Business logic in views        | Hard to test          | Move to `services.py`         |
| Unpaginated `Model.objects.all()` | Memory crash          | Use standard ViewSet or limit |

---

## Testing Guidelines (Pytest)

We use `pytest` combined with `pytest-django`.

### Test Coverage Requirements

| Layer        | Target Coverage | Description                    |
| ------------ | --------------- | ------------------------------ |
| Services     | > 90%           | Core business rules / Proxies  |
| Views/Routes | > 80%           | HTTP contract testing          |
| Models       | > 80%           | Custom model methods / constraints |
| Serializers  | Tested via Views| Covered implicitly if Views pass |

### Running Tests

```bash
# Run all tests
pytest

# Run tests in a specific app
pytest project/tests/

# Run with coverage report
pytest --cov=.
```

### Test File Template

```python
# backend/project/tests/test_services.py
import pytest
from project.models import Project
from project.services import create_project

@pytest.mark.django_db
class TestProjectServices:

    def test_create_project_success(self):
        # Arrange
        name = "Test Project"
        
        # Act
        project = create_project(name=name)
        
        # Assert
        assert project.id is not None
        assert project.name == "Test Project"
        assert project.status == "active"
        
    def test_create_project_validation(self):
        # Arrange
        name = "" # invalid
        
        # Act & Assert
        with pytest.raises(ValueError):
            create_project(name=name)
```

### Test Scenario Categories

| Category            | What to Test            | Example                        |
| ------------------- | ----------------------- | ------------------------------ |
| Input Validation    | Required fields, format | Missing name, invalid UUID     |
| Normal Operations   | Happy path              | Create entity successfully     |
| Error Handling      | Exceptions, proxy fails | Verify HTTPErrors are raised/caught |
| Database Integrity  | Constraints             | Duplicate unique names         |

---

## Summary

| Rule                         | Reason              |
| ---------------------------- | ------------------- |
| Absolute imports             | Codebase clarity    |
| Use `Black` and `Ruff`       | Uniform formatting without arguments |
| Never rely on `import *`     | Explicit is better than implicit |
| 90% coverage for services    | Isolate logic from Web logic  |
| Use `@pytest.mark.django_db` | Give tests DB access securely |
