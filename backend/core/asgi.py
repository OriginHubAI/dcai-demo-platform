"""
ASGI application for dcai-platform.

DataFlow-WebUI's FastAPI app is mounted in-process alongside Django.

Route ownership:
  /embedded/dataflow-webui/*     → FastAPI / (serve DataFlow-WebUI React frontend)
  /embedded/dataflow-backend/*   → FastAPI / (strip prefix; frontend API calls via dcaiApiBase)
  /api/v1/*                      → FastAPI /api/v1/* (DataFlow-WebUI frontend in-iframe API calls)
  /api/v2/dataflow/pipelines/*   → FastAPI /api/v1/pipelines/* (dcai-platform compat, path rewrite)
  /api/v2/dataflow/operators/*   → FastAPI /api/v1/operators/*
  /api/v2/dataflow/tasks/*       → FastAPI /api/v1/tasks/*
  /api/v2/dataflow/datasets/*    → FastAPI /api/v1/datasets/*
  /api/v2/dataflow/serving/*     → FastAPI /api/v1/serving/*
  /api/v2/dataflow/prompts/*     → FastAPI /api/v1/prompts/*
  /api/v2/dataflow/preferences/* → FastAPI /api/v1/preferences/*
  /api/v2/dataflow/text2sql_database/* → FastAPI /api/v1/text2sql_database/*
  /api/v2/dataflow/text2sql_database_manager/* → FastAPI /api/v1/text2sql_database_manager/*
  /api/hf/*                      → Django HF datasets service
  /api/v2/dataflow/packages/*    → Django
  /api/v2/dataflow/operators     → Django OperatorListView (exact)
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

    # Configure DataFlow-WebUI to use dcai-platform's datasets service.
    # These must be set BEFORE importing app.main (pydantic_settings reads env at import).
    os.environ.setdefault("ENABLE_DATASETS_API", "false")
    os.environ.setdefault("ENABLE_HF_API", "false")
    # DataFlow-WebUI delegates all dataset API calls to dcai-platform's HF datasets service.
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

# Subpaths under /api/v2/dataflow/ that are proxied to FastAPI (with rewrite).
_COMPAT_SUBPATHS = ("pipelines/", "operators/", "tasks/", "datasets/", "serving/", "prompts/", "preferences/", "text2sql_database/", "text2sql_database_manager/")
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
    #    Only route the same subpaths that the compat layer covers — not all /api/v1/*
    #    (Django also serves endpoints under /api/v1/, e.g. /api/v1/chat/stream)
    #    /api/v1/pipelines/foo  →  /api/v1/pipelines/foo  (passthrough)
    if path.startswith(_FASTAPI_V1_PREFIX):
        suffix = path[len(_FASTAPI_V1_PREFIX):]
        if any(suffix.startswith(sub) for sub in _COMPAT_SUBPATHS):
            return path

    # 3. dcai-platform compat paths (path rewrite)
    #    /api/v2/dataflow/pipelines/foo  →  /api/v1/pipelines/foo
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
