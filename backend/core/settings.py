"""
Django settings for ADP Backend project.
"""

import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'django_celery_beat',
    
    # Local apps
    'core',
    'user',
    'agent',
    'chat',
    'collection',
    'knowledgebase',
    'document',
    'dataset',
    'dataflow',
    'task',
    'template',
    'organization',
    'systemconfig',
    'openapi',
    'customadmin',
    'df_conversation',
    'third_party',
    'llm_chat',
    'train',
    'loopai_proxy',
    'dfagent_proxy',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use PostgreSQL if DATABASE_URL is provided
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'user.User'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_CREDENTIALS = True

# Spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'ADP Backend API',
    'DESCRIPTION': 'API documentation for ADP Backend',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# Celery settings
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# External Agent Services
DATAFLOW_BACKEND_URL = os.environ.get('DATAFLOW_BACKEND_URL', 'http://localhost:8002')
LOOPAI_BACKEND_URL = os.environ.get('LOOPAI_BACKEND_URL', 'http://localhost:8003')
DFAGENT_BACKEND_URL = os.environ.get('DFAGENT_BACKEND_URL', 'http://localhost:7860')
DATAFLOW_OPERATORS_ROOT = os.environ.get(
    'DATAFLOW_OPERATORS_ROOT',
    str(BASE_DIR.parent.parent / 'DataFlow' / 'dataflow' / 'operators'),
)
DATAFLOW_REPO_ROOT = os.environ.get(
    'DATAFLOW_REPO_ROOT',
    str(BASE_DIR.parent.parent / 'DataFlow'),
)
CODE_SERVER_BASE_PORT = int(os.environ.get('CODE_SERVER_BASE_PORT', '18080'))
PACKAGE_EDITOR_PORT = int(os.environ.get('PACKAGE_EDITOR_PORT', '18004'))
PACKAGE_EDITOR_SANDBOX_ROOT = os.environ.get(
    'PACKAGE_EDITOR_SANDBOX_ROOT',
    str(BASE_DIR.parent.parent / 'sandboxes' / 'package-editor'),
)
PROXY_TIMEOUT = int(os.environ.get('PROXY_TIMEOUT', '120'))

LLM_PROVIDER_BASE_URL = os.environ.get('LLM_PROVIDER_BASE_URL', '')
LLM_PROVIDER_API_KEY = os.environ.get('LLM_PROVIDER_API_KEY', '')
LLM_DEFAULT_MODEL = os.environ.get('LLM_DEFAULT_MODEL', 'gpt-4o')
LLM_AVAILABLE_MODELS = [
    model.strip()
    for model in os.environ.get('LLM_AVAILABLE_MODELS', '').split(',')
    if model.strip()
]
LLM_REQUEST_TIMEOUT = int(os.environ.get('LLM_REQUEST_TIMEOUT', '120'))

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Dataflow System Integration
ENABLE_MOCK_DATAFLOW = os.environ.get('ENABLE_MOCK_DATAFLOW', 'False') == 'True'
ENABLE_MOCK_HF_DATASETS = os.environ.get('ENABLE_MOCK_HF_DATASETS', 'False') == 'True'
HF_ENDPOINT = os.environ.get('HF_ENDPOINT', 'https://huggingface.co')
HF_DATASETS_CACHE = os.environ.get('HF_DATASETS_CACHE', None)
DATAFLOW_SERVICE_URL = os.environ.get('DATAFLOW_SERVICE_URL', 'http://localhost:8001')
HF_DATASETS_SERVICE_URL = os.environ.get('HF_DATASETS_SERVICE_URL', 'http://localhost:8002')

