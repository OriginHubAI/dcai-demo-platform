# Environment Configuration

> Guidelines for managing configurations across different environments (Development vs Production) in Django.

---

## The `.env` Approach

Configuration should never be hardcoded into `settings.py`. We use `django-environ` to read values from a `.env` file or from system environment variables.

### The Problem

- Secrets committed to Git.
- Hardcoded database credentials resulting in production breakages.
- Overriding complex dictionaries based on environments.

### The Solution

```python
# backend/core/settings.py
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Reading .env file.
# We usually read it from the level above `backend/` where the Dockerfile might be invoked,
# or cleanly inside the `backend/` folder.
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))

# Usage:
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DEBUG')
DATABASE_URL = env('DATABASE_URL', default='postgres://user:pass@localhost:5432/dcai_db')

DATABASES = {
    'default': env.db('DATABASE_URL')
}
```

---

## Expected `.env` Variables

A `.env.example` file should exist in the repository root and look something like this:

```ini
# Core Django
DJANGO_SECRET_KEY=yoursecretkey
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,dcai-platform.com

# Database (PostgreSQL)
DATABASE_URL=postgres://postgres:password@localhost:5432/dcai_db
# Redis
REDIS_URL=redis://localhost:6379/1

# Proxied FastAPI Endpoints
FASTAPI_BASE_URL=http://localhost:8002
```

---

## Local Development vs Production settings

Instead of maintaining multiple settings files (e.g., `settings_dev.py`, `settings_prod.py`), try to toggle settings dynamically based on the `DEBUG` flag.

```python
if DEBUG:
    # Use simpler setups, print emails to console.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # Optional SQLite override for light local dev
    # DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / "db.sqlite3"}
else:
    # Use real email service, restrict CORS completely, secure session cookies
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

---

## Summary

| Rule                                  | Reason                                                |
| ------------------------------------- | ----------------------------------------------------- |
| Never hardcode secrets in `settings.py`| Prevents credential leaks                             |
| Copy `.env.example` to `.env`         | Ensures devs know what vars are needed                |
| Base settings on `DEBUG`              | Maintains a single source of truth for app config     |
| Use `django-environ`                  | Safely parses casting types (e.g. converting "True" to Python boolean `True`) |
