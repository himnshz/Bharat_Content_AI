"""
Translation Tasks
"""
from app.config.celery_config import celery_app


@celery_app.task(name="app.tasks.translation_tasks.translate_single_text")
def translate_single_text(text: str, **kwargs):
    """Translate single text task"""
    return {"status": "completed", "text": text}
