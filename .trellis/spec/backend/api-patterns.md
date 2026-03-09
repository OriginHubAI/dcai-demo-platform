# API Patterns

> Common patterns and anti-patterns for Django REST Framework (DRF) and backend integration modules.

---

## Common Patterns

### 1. CRUD with Transaction

For creating entities with related data, use `django.db.transaction.atomic`.

```python
# backend/project/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Project, ProjectMember
import logging

logger = logging.getLogger(__name__)

def create_project_with_members(name: str, description: str, member_user_ids: list[int]) -> Project:
    try:
        with transaction.atomic():
            # 1. Create project
            project = Project.objects.create(
                name=name, 
                description=description
            )
            
            # 2. Create members if provided
            if member_user_ids:
                members_to_create = [
                    ProjectMember(project=project, user_id=uid)
                    for uid in member_user_ids
                ]
                ProjectMember.objects.bulk_create(members_to_create)
                
            return project
            
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        # Re-raise or convert to a specific API Exception so the view can handle it
        raise ValidationError("Failed to create project and members.")
```

### 2. Standard DRF ViewSet

Use Generic ViewSets for standard CRUD features with built-in pagination, filtering, and object lookups.

```python
# backend/project/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    queryset = Project.objects.all().order_by('-updated_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter based on current user or query params
        qs = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs
```

### 3. FastAPI Proxy View

For routing requests to internal FastAPI services (e.g., Agents, Tasks), use the standard `FastAPIProxyView`. This handles header forwarding and asynchronous communication.

```python
# backend/fastapi_proxy.py
from fastapi_proxy import FastAPIProxyView

class FastAPIAgentProxyView(FastAPIProxyView):
    """Proxy for Agent endpoints"""
    fastapi_path = 'api/v2/agents'

# urls.py
path('api/v2/agents/', FastAPIAgentProxyView.as_view()),
```

Refer to [fastapi.md](./fastapi.md) for detailed integration guidelines.

---

## Anti-Patterns

### 1. Fat Views without Serializer Validation

```python
# BAD: Manual validation and dict access in Views
class CreateProjectView(APIView):
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({"error": "Name required"}, status=400)
        
        project = Project.objects.create(name=name, status='active')
        return Response({"id": project.id, "name": project.name})

# GOOD: Lean Views with DRF Serializers
class CreateProjectView(APIView):
    def post(self, request):
        serializer = CreateProjectInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Validation passed, use validated_data
        project = Project.objects.create(**serializer.validated_data)
        return Response(ProjectSerializer(project).data)
```

### 2. N+1 Query Problem

Failing to fetch related models in list endpoints.

```python
# BAD: Triggers N additional queries when accessing related field `author`
queryset = Task.objects.all()
# Serializer accessing task.author.name inside a loop

# GOOD: Uses select_related (for ForeignKeys) or prefetch_related (for ManyToMany)
queryset = Task.objects.select_related('author').all()
```

### 3. Catching System Errors Silently in Transactions

```python
# BAD: Transaction continues or commits partial state, hiding the error
@transaction.atomic
def process_data(data):
    try:
        Project.objects.create(**data)
        # ... more db operations
    except Exception:
        pass # Transaction continues or commits in an invalid state

# GOOD: Raise to trigger transaction rollback
@transaction.atomic
def process_data(data):
    try:
        Project.objects.create(**data)
    except IntegrityError:
        # Let it bubble up or raise an API-friendly exception
        raise ValidationError("Invalid data, cannot process.")
```

---

## Upsert Pattern (Django ORM)

Use `update_or_create` for Upsert patterns to avoid race conditions.

```python
# Insert or update based on 'key'
obj, created = SystemSetting.objects.update_or_create(
    key='theme',
    defaults={'value': 'dark', 'updated_at': timezone.now()}
)
```

---

## Soft Delete Pattern

Instead of hard deleting rows, especially for audited tables.

```python
# In models.py
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

# Usage in Services/Views:
def safe_delete_project(project_id: int):
    Project.objects.filter(id=project_id).update(
        is_deleted=True, 
        deleted_at=timezone.now()
    )

# Query active only
active_projects = Project.objects.filter(is_deleted=False)
```

---

## Summary

| Pattern                | Use Case                       | Django/DRF Solution                 |
| ---------------------- | ------------------------------ | ----------------------------------- |
| Multiple DB operations | Ensure atomic consistency      | `@transaction.atomic`               |
| Query optimization     | Avoiding N+1 queries           | `select_related`, `prefetch_related`|
| Pagination             | Standard DRF list endpoints    | DRF Pagination Classes              |
| External API calls     | Calling FastAPI Microservices  | `httpx` asynchronous clients        |
| Upsert                 | Insert or update data          | `update_or_create` ORM method       |
| Soft delete            | Data recovery & audit trails   | Filter `is_deleted=False`           |
