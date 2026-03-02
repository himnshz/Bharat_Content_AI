"""
Content Generation Tasks with Progress Tracking
"""
from app.config.celery_config import celery_app
from app.config.redis_config import get_sync_redis, TaskProgressTracker
from app.config.database import SessionLocal
from app.models import Content, ContentType, ContentStatus, ToneType, User
from app.services.content_generation.ai_service_manager import get_ai_service_manager
import bleach
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.content_tasks.generate_content_async")
def generate_content_async(
    self,
    user_id: int,
    prompt: str,
    language: str = "hindi",
    tone: str = "casual",
    content_type: str = "social_post"
):
    """
    Generate AI content asynchronously with progress tracking.
    
    Args:
        self: Celery task instance
        user_id: User ID requesting content
        prompt: Content generation prompt
        language: Target language
        tone: Content tone
        content_type: Type of content
    
    Returns:
        dict: Generated content details
    """
    redis = get_sync_redis()
    tracker = TaskProgressTracker(redis)
    db = SessionLocal()
    
    try:
        # Update progress: Starting
        tracker.set_progress(
            self.request.id,
            0, 100,
            "processing",
            "Initializing content generation..."
        )
        
        # Get AI service manager
        tracker.set_progress(
            self.request.id,
            10, 100,
            "processing",
            "Connecting to AI service..."
        )
        
        ai_manager = get_ai_service_manager()
        
        if not ai_manager.get_available_services():
            tracker.set_progress(
                self.request.id,
                0, 100,
                "failed",
                "No AI services available"
            )
            raise Exception("AI service temporarily unavailable")
        
        # Generate content
        tracker.set_progress(
            self.request.id,
            30, 100,
            "processing",
            "Generating content with AI..."
        )
        
        start_time = datetime.utcnow()
        result = ai_manager.generate_content(
            prompt=prompt,
            language=language,
            tone=tone,
            content_type=content_type
        )
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        # Sanitize content
        tracker.set_progress(
            self.request.id,
            70, 100,
            "processing",
            "Sanitizing and processing content..."
        )
        
        generated_text = bleach.clean(result['content'], tags=[], strip=True)
        
        # Calculate metrics
        word_count = len(generated_text.split())
        char_count = len(generated_text)
        keywords = [w.strip('.,!?') for w in generated_text.split() if len(w) > 5][:10]
        hashtags = [w for w in generated_text.split() if w.startswith('#')]
        
        # Save to database
        tracker.set_progress(
            self.request.id,
            90, 100,
            "processing",
            "Saving content to database..."
        )
        
        content = Content(
            user_id=user_id,
            original_prompt=prompt,
            generated_content=generated_text,
            content_type=ContentType[content_type.upper()],
            status=ContentStatus.GENERATED,
            language=language,
            tone=ToneType[tone.upper()],
            model_used=result.get('model_used'),
            generation_time_ms=generation_time,
            word_count=word_count,
            character_count=char_count,
            keywords=keywords,
            hashtags=hashtags,
            quality_score=85.0,
            estimated_reading_time=word_count // 3
        )
        
        db.add(content)
        
        # Update user stats
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.content_generated_count += 1
        
        db.commit()
        db.refresh(content)
        
        # Complete
        result_data = {
            "id": content.id,
            "generated_content": generated_text,
            "word_count": word_count,
            "model_used": result.get('model_used'),
            "generation_time_ms": generation_time
        }
        
        tracker.set_progress(
            self.request.id,
            100, 100,
            "completed",
            "Content generated successfully!",
            result_data
        )
        
        logger.info(f"Content generated async for user {user_id}, content_id={content.id}")
        return result_data
        
    except Exception as e:
        logger.error(f"Async content generation failed: {str(e)}", exc_info=True)
        tracker.set_progress(
            self.request.id,
            0, 100,
            "failed",
            f"Generation failed: {str(e)}"
        )
        raise
    finally:
        db.close()


@celery_app.task(name="app.tasks.content_tasks.generate_single_content")
def generate_single_content(prompt: str, **kwargs):
    """Generate single content task (legacy)"""
    return {"status": "completed", "prompt": prompt}

