#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    django.setup()

    try:
        # Test database connection
        from django.db import connection

        connection.ensure_connection()

        # Test Redis connection
        import redis

        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()

        # Test MongoDB connection
        from tasks.utils import get_mongodb_connection

        db = get_mongodb_connection()
        db.list_collection_names()

        print("✅ All services are healthy!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        sys.exit(1)
