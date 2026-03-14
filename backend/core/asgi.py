"""
ASGI application for dcai-platform.

DataFlow-WebUI's FastAPI app is mounted in-process alongside Django.

Route ownership:
  /embedded/dataflow-webui/*     → FastAPI / (serve DataFlow-WebUI React frontend)
  /embedded/dataflow-backend/*   → FastAPI / (strip prefix; frontend API calls via dcaiApiBase)
  /api/v1/operators/*            → Django df app → httpx → DATAFLOW_BACKEND_URL
  /api/v1/tasks/*                → Django df app → httpx → DATAFLOW_BACKEND_URL
  /api/v1/pipelines/*            → Django df app → httpx → DATAFLOW_BACKEND_URL
  /api/v1/* (datasets/serving/prompts/…) → FastAPI /api/v1/* (in-iframe calls, passthrough)
  /api/v2/dataflow/datasets/*    → FastAPI /api/v1/datasets/*
  /api/v2/dataflow/serving/*     → FastAPI /api/v1/serving/*
  /api/v2/dataflow/prompts/*     → FastAPI /api/v1/prompts/*
  /api/v2/dataflow/preferences/* → FastAPI /api/v1/preferences/*
  /api/v2/dataflow/text2sql_database/* → FastAPI /api/v1/text2sql_database/*
  /api/v2/dataflow/text2sql_database_manager/* → FastAPI /api/v1/text2sql_database_manager/*
  /api/hf/*                      → Django HF datasets service
  /api/v2/dataflow/packages/*    → Django
  /api/v2/dataflow/operators     → Django OperatorListView (exact)
  /api/v2/dataflow/operators/*   → Django df app → httpx → DATAFLOW_BACKEND_URL
  /api/v2/dataflow/pipelines/*   → Django df app → httpx → DATAFLOW_BACKEND_URL
  /api/v2/dataflow/tasks/*       → Django df app → httpx → DATAFLOW_BACKEND_URL
  everything else                → Django
"""

import logging
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# ---------------------------------------------------------------------------
# Django must be set up before any Django imports
# ---------------------------------------------------------------------------
import django  # noqa: E402

django.setup()

from django.core.asgi import get_asgi_application  # noqa: E402

django_app = get_asgi_application()

# ---------------------------------------------------------------------------
# DataFlow-WebUI FastAPI app (optional — falls back to Django-only if missing)
# ---------------------------------------------------------------------------

_dataflow_app = None

_backend_dir = os.environ.get(
    "DATAFLOW_WEBUI_BACKEND_DIR",
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "DCAI-DataFlow-WebUI", "backend")
    ),
)

if os.path.isdir(_backend_dir):
    if _backend_dir not in sys.path:
        sys.path.insert(0, _backend_dir)

    # Configure DataFlow-WebUI to use dcai-platform's HF datasets service.
    # These must be set BEFORE importing app.main (pydantic_settings reads env at import).
    # ENABLE_DATASETS_API must stay true — the DataFlow local dataset registry
    # (/api/v1/datasets/*) is needed for pipeline dataset management. Only ENABLE_HF_API
    # is disabled because dcai-platform provides its own HF hub at /api/hf/*.
    os.environ.setdefault("ENABLE_DATASETS_API", "true")
    os.environ.setdefault("ENABLE_HF_API", "false")
    # DataFlow-WebUI delegates HF hub API calls to dcai-platform's HF datasets service.
    os.environ.setdefault("EXTERNAL_HF_API_URL", "http://localhost:18000/api/hf")

    try:
        from app.main import app as _dataflow_app  # type: ignore[import]

        logging.getLogger(__name__).info("DataFlow-WebUI FastAPI app loaded successfully.")
    except Exception as exc:  # pragma: no cover
        logging.getLogger(__name__).warning(
            "DataFlow-WebUI not available — falling back to Django-only: %s", exc
        )
else:
    logging.getLogger(__name__).warning(
        "DATAFLOW_WEBUI_BACKEND_DIR not found (%s) — DataFlow-WebUI disabled.", _backend_dir
    )


# ---------------------------------------------------------------------------
# ASGI dispatcher
# ---------------------------------------------------------------------------

# Subpaths that the in-iframe DataFlow-WebUI frontend calls directly via /api/v1/*.
# operators/, tasks/, pipelines/ MUST stay here so that the self-referential httpx
# call from Django proxy_views (DATAFLOW_BACKEND_URL → this ASGI server) is caught
# by Rule 2 and forwarded to in-process FastAPI — preventing an infinite loop.
_V1_PASSTHROUGH_SUBPATHS = (
    "operators/", "tasks/", "pipelines/",
    "datasets/", "serving/", "prompts/", "preferences/",
    "text2sql_database/", "text2sql_database_manager/",
)

# Subpaths under /api/v2/dataflow/ that are rewritten and proxied to FastAPI.
# tasks/, pipelines/, operators/ are intentionally excluded here — they are
# now intercepted by Django df app views (proxy_views.py) before reaching ASGI.
_COMPAT_SUBPATHS = ("datasets/", "serving/", "prompts/", "preferences/", "text2sql_database/", "text2sql_database_manager/")
_COMPAT_PREFIX = "/api/v2/dataflow/"
_FASTAPI_V1_PREFIX = "/api/v1/"

# Prefixes whose requests are served by the DataFlow-WebUI React frontend.
_FRONTEND_PREFIXES = ("/embedded/dataflow-webui/", "/embedded/dataflow-backend/")


def _rewrite(path: str):
    """
    Return the FastAPI-internal path for the given incoming path, or None if
    the request should fall through to Django.
    """
    if _dataflow_app is None:
        return None

    # 1. DataFlow-WebUI React frontend (iframe entry + static assets)
    #    /embedded/dataflow-webui/foo  →  /foo
    #    /embedded/dataflow-backend/foo  →  /foo
    for prefix in _FRONTEND_PREFIXES:
        if path.startswith(prefix):
            return path[len(prefix) - 1:]  # keep leading "/"

    # 2. DataFlow-WebUI API calls made directly by the in-iframe frontend
    #    /api/v1/operators/  /api/v1/tasks/  /api/v1/pipelines/ etc.  →  FastAPI passthrough
    #    (Django also serves /api/v1/chat/stream — only route known DataFlow subpaths)
    if path.startswith(_FASTAPI_V1_PREFIX):
        suffix = path[len(_FASTAPI_V1_PREFIX):]
        if any(suffix.startswith(sub) for sub in _V1_PASSTHROUGH_SUBPATHS):
            return path

    # 3. dcai-platform compat paths (path rewrite)
    #    /api/v2/dataflow/datasets/foo  →  /api/v1/datasets/foo
    #    (tasks/pipelines/operators are handled by Django df app before reaching here)
    if path.startswith(_COMPAT_PREFIX):
        suffix = path[len(_COMPAT_PREFIX):]
        if any(suffix.startswith(sub) for sub in _COMPAT_SUBPATHS):
            return _FASTAPI_V1_PREFIX + suffix

    return None


async def application(scope, receive, send):
    if scope["type"] in ("http", "websocket"):
        rewritten = _rewrite(scope.get("path", ""))
        if rewritten is not None:
            scope = dict(scope)
            scope["path"] = rewritten
            await _dataflow_app(scope, receive, send)
            return
    await django_app(scope, receive, send)
