"""
Celery Configuration for Async Task Queue
Handles bulk operations without blocking FastAPI event loop
"""
from celery import Celery
from kombu import Exchange, Queue
import os
from dotenv import load_dotenv

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)

# Create Celery app
celery_app = Celery(
    "bharat_content_ai",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.bulk_operations",
        "app.tasks.content_tasks",
        "app.tasks.translation_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
    task_soft_time_limit=3300,  # 55 minutes soft limit
    task_acks_late=True,  # Acknowledge after task completion
    task_reject_on_worker_lost=True,
    
    # Result backend
    result_expires=86400,  # Results expire after 24 hours
    result_extended=True,  # Store additional task metadata
    
    # Worker settings
    worker_prefetch_multiplier=4,  # Number of tasks to prefetch
    worker_max_tasks_per_child=1000,  # Restart worker after 1000 tasks
    worker_disable_rate_limits=False,
    
    # Retry settings
    task_default_retry_delay=60,  # 1 minute
    task_max_retries=3,
    
    # Queue configuration
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    
    # Task routes
    task_routes={
        "app.tasks.bulk_operations.*": {"queue": "bulk"},
        "app.tasks.content_tasks.*": {"queue": "content"},
        "app.tasks.translation_tasks.*": {"queue": "translation"},
    },
    
    # Beat schedule (for periodic tasks)
    beat_schedule={
        "cleanup-expired-tasks": {
            "task": "app.tasks.bulk_operations.cleanup_expired_tasks",
            "schedule": 3600.0,  # Every hour
        },
    },
)

# Define queues
celery_app.conf.task_queues = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("bulk", Exchange("bulk"), routing_key="bulk", priority=5),
    Queue("content", Exchange("content"), routing_key="content", priority=7),
    Queue("translation", Exchange("translation"), routing_key="translation", priority=7),
)

# Task annotations for rate limiting
celery_app.conf.task_annotations = {
    "app.tasks.bulk_operations.process_bulk_content": {
        "rate_limit": "10/m",  # 10 bulk operations per minute
    },
    "app.tasks.content_tasks.generate_single_content": {
        "rate_limit": "100/m",  # 100 content generations per minute
    },
}


# Celery signals for monitoring
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery setup"""
    print(f"Request: {self.request!r}")
    return {"status": "success", "message": "Celery is working!"}
