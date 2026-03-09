# Database Guidelines (Django ORM + PostgreSQL)

> Guidelines for Django ORM and Database migrations development.

---

## Database Configuration

The DCAI Platform uses **PostgreSQL** for primary transactional data and **MyScale** for vector embeddings and OLAP queries. Dev environments can optionally use SQLite.

```python
# backend/core/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dcai_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Schema Definition (Models)

Use Django's built-in Model classes to define your schema.

```python
# backend/project/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Project(models.Model):
    # UUIDs are better for distributed systems and hard-to-guess IDs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # TextChoices for Enums
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'
        DRAFT = 'draft', 'Draft'
        
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.ACTIVE
    )
    
    # Automatically managed timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Default order
        ordering = ['-updated_at']
        # Add constraints and indexes as needed
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return self.name

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## Query Patterns

### ORM Basics

```python
# Single result (Raises Task.DoesNotExist if not found, Task.MultipleObjectsReturned if > 1)
task = Task.objects.get(id=task_id)

# Single result, returning None if not found
task = Task.objects.filter(id=task_id).first()

# Multiple results
all_tasks = Task.objects.all()
active_projects = Project.objects.filter(status='active')

# Insert with return
project = Project.objects.create(name='New Project')

# Relational queries (Reverse Relationship using `related_name`)
project_tasks = project.tasks.all()
```

### Avoiding N+1 Queries

Always fetch related data efficiently if you plan to serialize or iterate through it.

```python
# Use select_related when fetching a Foreign Key (1-to-1 or N-to-1)
tasks = Task.objects.select_related('project').all()
for task in tasks:
    print(task.project.name) # Does NOT trigger a new database hit

# Use prefetch_related when fetching Many-to-Many or Reverse Foreign Keys (1-to-N)
projects = Project.objects.prefetch_related('tasks').all()
for project in projects:
    print(project.tasks.count()) # Does NOT trigger a new database hit per project if loaded appropriately
```

### Batch Operations

```python
# Bulk Create
Project.objects.bulk_create([
    Project(name='Project 1'),
    Project(name='Project 2'),
])

# Bulk Update
Task.objects.filter(completed=False).update(completed=True)
```

### IN clauses

```python
# Finding items matching a list of IDs
project_ids = [1, 2, 3]
projects = Project.objects.filter(id__in=project_ids)
```

---

## Migrations

Django handles schema changes automatically via makemigrations.

```bash
# 1. After making a change to models.py, generate the migration file
python manage.py makemigrations project

# 2. Apply the migration to the database
python manage.py migrate
```

**Rule of Thumb:**
- Never edit an applied migration file.
- If you mess up locally, reverse the migration (`python manage.py migrate project {prev_migration_num}`), delete the bad migration file, and recreate it.
- In production, migrations should always be run sequentially during the deployment process.

---

## Advanced: Querying External/Vector Databases

The platform uses MyScale for vector search. This is typically managed via a client library, rather than the Django ORM, though the results might be mapped back to Django ORM Models.

```python
import clickhouse_connect

def search_embeddings(embedding_vector, limit=10):
    client = clickhouse_connect.get_client(...)
    # Native MyScale Query
    result = client.command(f"""
        SELECT id, distance(vector, {embedding_vector}) as dist 
        FROM dataset_vectors
        ORDER BY dist ASC LIMIT {limit}
    """)
    return result
```

---

## Quick Reference

| Operation             | Method                                   |
| --------------------- | ---------------------------------------- |
| Fetch One             | `.get()` or `.first()`                   |
| Fetch Many            | `.filter()` or `.all()`                  |
| Insert                | `.create()` or `.bulk_create()`          |
| Relational (FK)       | `.select_related('fk_field')`            |
| Relational (M2M)      | `.prefetch_related('m2m_field')`         |
| Match array           | `filter(field__in=list)`                 |
| Contains String       | `filter(field__icontains="text")`        |

| Rule                             | Reason                                  |
| -------------------------------- | --------------------------------------- |
| Use `select_related/prefetch`    | Maximize performance (avoid N+1)        |
| Use transactions                 | Atomic operations                       |
| Generate Migrations (`makemigrations`) | Keep schema tightly coupled to code |
