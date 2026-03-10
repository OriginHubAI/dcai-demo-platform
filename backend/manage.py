#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def enforce_memory_limit():
    """Enforce virtual memory limit if TEST_MEMORY_LIMIT_GB is set."""
    # Temporarily disabled
    return


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    # Load .env from project root
    BASE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = BASE_DIR.parent
    load_dotenv(PROJECT_ROOT / '.env')
    
    # Apply memory limit if applicable
    enforce_memory_limit()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
