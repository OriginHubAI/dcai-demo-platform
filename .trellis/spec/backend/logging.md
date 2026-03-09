# Logging Guidelines

> Guidelines for logging in Python and Django.

---

## Logging Guidelines

### Use Python Standard `logging`

Never use `print()` for backend logic, since it won't be collected by centralized monitoring tools (like ELK/CloudWatch) and lacks severity context.

```python
# CORRECT
import logging

logger = logging.getLogger(__name__)

def create_project(data):
    logger.info("Project creation started", extra={"project_name": data.get("name")})
    try:
        # DB Logic
        pass
    except Exception as e:
        # Use logger.exception to automatically attach the stack trace
        logger.exception("Failed to create project")

# WRONG
print("Project created: " + project.id)
```

### Django `LOGGING` Configuration

Logging is configured centrally in `core/settings.py`.

```python
# backend/core/settings.py
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if os.environ.get('DEBUG') == 'True' else 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        # Catch our application logs
        'agent': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        }
    },
}
```

### Log Levels

| Level       | Use Case            | Action Required |
| ----------- | ------------------- | --------------- |
| `EXCEPTION` | Includes stack trace| Immediate bug investigation |
| `ERROR`     | Unexpected failures | High priority investigation |
| `WARNING`   | Recoverable issues  | Low priority, monitor |
| `INFO`      | Important events    | Passive monitoring |
| `DEBUG`     | Development details | Ignore in production |

---

## Handling Celery Task Logging

When running background tasks using Celery, you should obtain a logger specific to Celery so the logs correctly pipe to the worker output stream.

```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery_app.task
def process_data(data_id):
    logger.info(f"Starting async processing for Data ID: {data_id}")
    ...
```

---

## Summary

| Rule                             | Reason                     |
| -------------------------------- | -------------------------- |
| Use `logging.getLogger(__name__)`| Module identification out of the box      |
| Avoid `print()` statements       | Lacks structure and won't go to file handlers |
| Use `logger.exception()` in `except` blocks | Collects the full stack trace |
| Configure central formatters     | Consistency across all modules |
