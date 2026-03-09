# API Module Organization

> Domain-driven API module layout using Django, Django REST Framework (DRF), and Python type hints.

---

## Core Principles

1. **Domain-driven structure** - Each major business domain gets its own Django app (e.g., `apps.dataset`, `user`, `chat`).
2. **Fat Models, Thin Views, Service Layer** - Keep HTTP logic in Views/ViewSets, state in Models, and complex business logic in `services.py` or selectors.
3. **Serialization** - Use DRF Serializers for validation and data transformation.
4. **Code reuse** - Shared utilities extracted to a common `core/` or `utils/` app.
5. **Clear separation of concerns** - URL routing -> Views -> Serializers/Services -> Models.

---

## Django App Structure

A typical modern Django app in DCAI Platform should look like this:

```
backend/{app_name}/
├── apps.py               # Django AppConfig
├── models.py             # Database models (PostgreSQL)
├── urls.py               # App-specific URL routing
├── views.py              # DRF Views & ViewSets
├── serializers.py        # Request/Response validation and transformation
├── services.py           # Complex business logic and external API calls (e.g. FastAPI proxying)
├── selectors.py          # (Optional) Complex read queries
└── tests/                # Unit and integration tests
```

---

## File Responsibilities

### `models.py` - Database Schema

**Purpose**: Define the database tables, relationships, and basic data integrity rules using the Django ORM.

```python
# backend/project/models.py
from django.db import models

class ProjectStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    ARCHIVED = 'archived', 'Archived'
    DRAFT = 'draft', 'Draft'

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name
```

---

### `serializers.py` - Validation & Data Formatting

**Purpose**: Validate incoming data (from `request.data` or `request.query_params`) and serialize outgoing model instances to JSON.

```python
# backend/project/serializers.py
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CreateProjectInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
```

---

### `views.py` / `viewset/` - HTTP Endpoint Handlers

**Purpose**: Handle HTTP requests, parse inputs using serializers, call services/ORM layer, and return HTTP responses.

```python
# backend/project/views.py
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, CreateProjectInputSerializer
from .services import create_project

class ProjectViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        # 1. Validate Input
        serializer = CreateProjectInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. Call Service or ORM
        project = create_project(**serializer.validated_data)
        
        # 3. Serialize Output
        output_serializer = ProjectSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
```

---

### `services.py` - Business Logic & Proxies

**Purpose**: Host reusable logic that involves multiple models, external API calls (e.g., to DataFlow-System FastAPI), or complex transaction blocks.

```python
# backend/project/services.py
from django.db import transaction
from .models import Project

@transaction.atomic
def create_project(name: str, description: str = "") -> Project:
    """
    Creates a new project. Raises exceptions on failure.
    """
    project = Project.objects.create(
        name=name,
        description=description,
        status='active'
    )
    # Could involve other models or external API calls here
    return project
```

---

## URL Routing Integration

URL configs map incoming requests to the ViewSets or Views.

```python
# backend/project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
```

---

## Best Practices

### DO

- **Always validate inputs with DRF Serializers**: `serializer.is_valid(raise_exception=True)` automatically returns HTTP 400 with the error details.
- **Use `select_related` and `prefetch_related`** in your Views' `queryset` to avoid N+1 queries.
- **Keep Views thin**: Move complex business rules to `services.py` or model methods.
- **Return consistent DRF Responses**: Let the content negotiation handle JSON rendering.

### DON'T

- **Don't skip validation**: Never trust `request.data` blindly. E.g., `Project.objects.create(**request.data)` is dangerous.
- **Don't put complex business logic in Serializers**: Serializers are for data transformation and validation. If creating an object requires hitting an external API, put that in a `service`.
- **Don't expose internal stack traces**: Let DRF's exception handler convert custom Exceptions into appropriate HTTP responses.

---

## Quick Start Checklist

When creating a new Django app (module):

- [ ] Run `python manage.py startapp {app_name}`
- [ ] Add the app to `INSTALLED_APPS` in `core/settings.py`
- [ ] Create `models.py` and run `makemigrations`
- [ ] Add `serializers.py` with validation rules
- [ ] Create `views.py` (prefer ViewSets for CRUD)
- [ ] Add `urls.py` and register it in the main `backend/core/urls.py`
- [ ] Add `services.py` if complex business logic or proxying to FastAPI is required
