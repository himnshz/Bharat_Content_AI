"""
Celery Tasks for Bulk Operations
Processes CSV files in batches without blocking FastAPI
"""
from celery import Task, group, chord
from app.config.celery_config import celery_app
from app.config.redis_config import get_sync_redis, TaskProgressTracker
from app.schemas.bulk_schemas import (
    ContentGenerationRow,
    TranslationRow,
    SchedulingRow,
    BulkOperationType
)
import pandas as pd
import time
from typing import List, Dict, Any
from pydantic import ValidationError
import traceback


class CallbackTask(Task):
    """Base task with callbacks for progress tracking"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Called when task succeeds"""
        redis_client = get_sync_redis()
        tracker = TaskProgressTracker(redis_client)
        tracker.set_progress(
            task_id=task_id,
            current=retval.get("total", 0),
            total=retval.get("total", 0),
            status="completed",
            message="Bulk operation completed successfully",
            result=retval
        )
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails"""
        redis_client = get_sync_redis()
        tracker = TaskProgressTracker(redis_client)
        tracker.set_progress(
            task_id=task_id,
            current=0,
            total=0,
            status="failed",
            message=f"Task failed: {str(exc)}",
            result={"error": str(exc), "traceback": str(einfo)}
        )


@celery_app.task(bind=True, base=CallbackTask, name="app.tasks.bulk_operations.process_bulk_content")
def process_bulk_content(
    self,
    csv_data: List[Dict[str, Any]],
    operation_type: str,
    user_id: int,
    batch_size: int = 10
) -> Dict[str, Any]:
    """
    Process bulk content generation from CSV data
    
    Args:
        csv_data: List of dictionaries from CSV
        operation_type: Type of operation (content_generation, translation, scheduling)
        user_id: User ID performing the operation
        batch_size: Number of items to process per batch
    
    Returns:
        Dictionary with results and statistics
    """
    redis_client = get_sync_redis()
    tracker = TaskProgressTracker(redis_client)
    
    task_id = self.request.id
    total_rows = len(csv_data)
    successful = 0
    failed = 0
    errors = []
    results = []
    
    start_time = time.time()
    
    try:
        # Update initial progress
        tracker.set_progress(
            task_id=task_id,
            current=0,
            total=total_rows,
            status="processing",
            message=f"Starting {operation_type} for {total_rows} items"
        )
        
        # Validate and process rows based on operation type
        if operation_type == BulkOperationType.CONTENT_GENERATION.value:
            schema_class = ContentGenerationRow
            process_func = process_content_generation_batch
        elif operation_type == BulkOperationType.TRANSLATION.value:
            schema_class = TranslationRow
            process_func = process_translation_batch
        elif operation_type == BulkOperationType.SCHEDULING.value:
            schema_class = SchedulingRow
            process_func = process_scheduling_batch
        else:
            raise ValueError(f"Unknown operation type: {operation_type}")
        
        # Process in batches
        for batch_start in range(0, total_rows, batch_size):
            batch_end = min(batch_start + batch_size, total_rows)
            batch = csv_data[batch_start:batch_end]
            
            # Validate batch
            validated_batch = []
            for idx, row in enumerate(batch):
                row_number = batch_start + idx + 1
                try:
                    validated_row = schema_class(**row)
                    validated_batch.append(validated_row.dict())
                except ValidationError as e:
                    failed += 1
                    errors.append({
                        "row_number": row_number,
                        "error": str(e),
                        "data": row
                    })
            
            # Process validated batch
            if validated_batch:
                batch_results = process_func(validated_batch, user_id)
                
                for result in batch_results:
                    if result.get("success"):
                        successful += 1
                        results.append(result)
                    else:
                        failed += 1
                        errors.append(result)
            
            # Update progress
            current_progress = batch_end
            tracker.set_progress(
                task_id=task_id,
                current=current_progress,
                total=total_rows,
                status="processing",
                message=f"Processed {current_progress}/{total_rows} items"
            )
            
            # Small delay to prevent overwhelming the system
            time.sleep(0.1)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Final result
        final_result = {
            "task_id": task_id,
            "operation_type": operation_type,
            "total": total_rows,
            "successful": successful,
            "failed": failed,
            "errors": errors[:100],  # Limit errors to first 100
            "results": results[:100],  # Limit results to first 100
            "execution_time_seconds": round(execution_time, 2)
        }
        
        # Update final progress
        tracker.set_progress(
            task_id=task_id,
            current=total_rows,
            total=total_rows,
            status="completed",
            message=f"Completed: {successful} successful, {failed} failed",
            result=final_result
        )
        
        return final_result
    
    except Exception as e:
        # Handle unexpected errors
        error_message = f"Bulk operation failed: {str(e)}"
        traceback.print_exc()
        
        tracker.set_progress(
            task_id=task_id,
            current=0,
            total=total_rows,
            status="failed",
            message=error_message,
            result={"error": str(e), "traceback": traceback.format_exc()}
        )
        
        raise


def process_content_generation_batch(batch: List[Dict[str, Any]], user_id: int) -> List[Dict[str, Any]]:
    """
    Process a batch of content generation requests
    
    This function would integrate with your AI service manager
    """
    from app.services.content_generation.ai_service_manager import AIServiceManager
    from app.config.database import SessionLocal
    from app.models.content import Content
    
    results = []
    db = SessionLocal()
    
    try:
        ai_manager = AIServiceManager()
        
        for item in batch:
            try:
                # Generate content using AI service
                generated_content = ai_manager.generate_content(
                    prompt=item["prompt"],
                    language=item["language"],
                    content_type=item["content_type"],
                    tone=item["tone"]
                )
                
                # Save to database
                content = Content(
                    user_id=user_id,
                    original_prompt=item["prompt"],
                    generated_content=generated_content.get("content", ""),
                    language=item["language"],
                    content_type=item["content_type"],
                    tone=item["tone"],
                    model_used=generated_content.get("model", "unknown"),
                    word_count=len(generated_content.get("content", "").split())
                )
                
                db.add(content)
                db.commit()
                db.refresh(content)
                
                results.append({
                    "success": True,
                    "content_id": content.id,
                    "prompt": item["prompt"][:50] + "...",
                    "language": item["language"]
                })
                
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "prompt": item["prompt"][:50] + "..."
                })
    
    finally:
        db.close()
    
    return results


def process_translation_batch(batch: List[Dict[str, Any]], user_id: int) -> List[Dict[str, Any]]:
    """
    Process a batch of translation requests
    
    This function would integrate with your translation service
    """
    from app.services.translation.translator import TranslationService
    from app.config.database import SessionLocal
    from app.models.translation import Translation
    
    results = []
    db = SessionLocal()
    
    try:
        translator = TranslationService()
        
        for item in batch:
            try:
                # Translate text
                translated = translator.translate(
                    text=item["text"],
                    source_language=item["source_language"],
                    target_language=item["target_language"]
                )
                
                # Save to database
                translation = Translation(
                    user_id=user_id,
                    original_text=item["text"],
                    translated_text=translated.get("translated_text", ""),
                    source_language=item["source_language"],
                    target_language=item["target_language"]
                )
                
                db.add(translation)
                db.commit()
                db.refresh(translation)
                
                results.append({
                    "success": True,
                    "translation_id": translation.id,
                    "source": item["source_language"],
                    "target": item["target_language"]
                })
                
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "text": item["text"][:50] + "..."
                })
    
    finally:
        db.close()
    
    return results


def process_scheduling_batch(batch: List[Dict[str, Any]], user_id: int) -> List[Dict[str, Any]]:
    """
    Process a batch of scheduling requests
    
    This function would integrate with your social media scheduler
    """
    from app.services.social_media.scheduler import SocialMediaScheduler
    from app.config.database import SessionLocal
    from app.models.post import Post
    from datetime import datetime
    
    results = []
    db = SessionLocal()
    
    try:
        scheduler = SocialMediaScheduler()
        
        for item in batch:
            try:
                # Schedule post
                post = Post(
                    user_id=user_id,
                    content_id=item["content_id"],
                    platform=item["platform"],
                    scheduled_time=datetime.fromisoformat(item["scheduled_time"].replace('Z', '+00:00')),
                    caption=item.get("caption"),
                    status="scheduled"
                )
                
                db.add(post)
                db.commit()
                db.refresh(post)
                
                results.append({
                    "success": True,
                    "post_id": post.id,
                    "platform": item["platform"],
                    "scheduled_time": item["scheduled_time"]
                })
                
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "content_id": item["content_id"]
                })
    
    finally:
        db.close()
    
    return results


@celery_app.task(name="app.tasks.bulk_operations.cleanup_expired_tasks")
def cleanup_expired_tasks():
    """Periodic task to cleanup expired task progress data"""
    redis_client = get_sync_redis()
    
    # This is handled by Redis TTL, but we can add additional cleanup logic here
    # For example, cleanup old result files, logs, etc.
    
    return {"status": "cleanup_completed", "timestamp": time.time()}
