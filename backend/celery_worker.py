"""
Celery Worker Startup Script
Run this to start the Celery worker for processing bulk operations
"""
from app.config.celery_config import celery_app

if __name__ == "__main__":
    # Start Celery worker
    celery_app.start()
