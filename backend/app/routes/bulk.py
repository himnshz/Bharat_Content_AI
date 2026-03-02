"""
Bulk Operations API Routes
Handles CSV upload, validation, and task management with SSE progress tracking
"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.config.redis_config import get_async_redis, AsyncTaskProgressTracker
from app.schemas.bulk_schemas import (
    BulkOperationRequest,
    BulkOperationResponse,
    TaskProgress,
    BulkOperationResult,
    CSVValidationResult,
    CSVValidationError,
    BulkOperationType
)
from app.tasks.bulk_operations import process_bulk_content
from app.models.user import User
from app.auth.dependencies import get_current_user
import pandas as pd
import io
import json
from typing import Optional
import asyncio
from celery.result import AsyncResult
from app.config.celery_config import celery_app
import aiofiles
import os
from datetime import datetime

router = APIRouter()

# Temporary upload directory
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/validate-csv", response_model=CSVValidationResult)
async def validate_csv(
    file: UploadFile = File(...),
    operation_type: BulkOperationType = BulkOperationType.CONTENT_GENERATION
):
    """
    Validate CSV file before processing
    
    Returns validation results with errors and sample data
    """
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        total_rows = len(df)
        errors = []
        valid_rows = 0
        
        # Validate based on operation type
        if operation_type == BulkOperationType.CONTENT_GENERATION:
            required_columns = ["prompt", "language", "content_type", "tone"]
        elif operation_type == BulkOperationType.TRANSLATION:
            required_columns = ["text", "source_language", "target_language"]
        elif operation_type == BulkOperationType.SCHEDULING:
            required_columns = ["content_id", "platform", "scheduled_time"]
        else:
            raise HTTPException(status_code=400, detail="Invalid operation type")
        
        # Check required columns
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Validate each row
        for idx, row in df.iterrows():
            row_number = idx + 1
            row_valid = True
            
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    errors.append(CSVValidationError(
                        row_number=row_number,
                        field=col,
                        error="Field is required",
                        value=row[col]
                    ))
                    row_valid = False
            
            if row_valid:
                valid_rows += 1
        
        # Get sample data (first 5 rows)
        sample_data = df.head(5).to_dict('records')
        
        return CSVValidationResult(
            valid=len(errors) == 0,
            total_rows=total_rows,
            valid_rows=valid_rows,
            invalid_rows=total_rows - valid_rows,
            errors=errors[:100],  # Limit to first 100 errors
            sample_data=sample_data
        )
    
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.post("/upload", response_model=BulkOperationResponse)
async def upload_bulk_csv(
    file: UploadFile = File(...),
    operation_type: BulkOperationType = BulkOperationType.CONTENT_GENERATION,
    current_user: User = Depends(get_current_user),
    batch_size: int = 10,
    priority: int = 5,
    db: Session = Depends(get_db)
):
    """
    Upload CSV file and start bulk operation
    
    Returns task ID and progress URL for tracking
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Read and parse CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        if len(df) > 10000:
            raise HTTPException(
                status_code=400,
                detail="CSV file too large. Maximum 10,000 rows allowed"
            )
        
        # Convert to list of dictionaries
        csv_data = df.to_dict('records')
        
        # Estimate processing time (rough estimate: 2 seconds per item)
        estimated_time = len(csv_data) * 2
        
        # Submit task to Celery
        task = process_bulk_content.apply_async(
            args=[csv_data, operation_type.value, current_user.id, batch_size],
            priority=priority
        )
        
        return BulkOperationResponse(
            task_id=task.id,
            operation_type=operation_type.value,
            total_rows=len(csv_data),
            status="queued",
            message=f"Bulk operation queued successfully. Processing {len(csv_data)} items.",
            progress_url=f"/api/bulk/progress/{task.id}",
            estimated_time_seconds=estimated_time
        )
    
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@router.get("/progress/{task_id}")
async def get_task_progress(task_id: str):
    """
    Get current progress of a bulk operation task
    
    Returns progress information including percentage, status, and results
    """
    try:
        redis_client = await get_async_redis()
        tracker = AsyncTaskProgressTracker(redis_client)
        
        # Get progress from Redis
        progress = await tracker.get_progress(task_id)
        
        if not progress:
            # Check Celery task status
            task_result = AsyncResult(task_id, app=celery_app)
            
            if task_result.state == "PENDING":
                return {
                    "task_id": task_id,
                    "status": "queued",
                    "message": "Task is queued and waiting to be processed"
                }
            elif task_result.state == "STARTED":
                return {
                    "task_id": task_id,
                    "status": "processing",
                    "message": "Task has started processing"
                }
            elif task_result.state == "SUCCESS":
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "message": "Task completed successfully",
                    "result": task_result.result
                }
            elif task_result.state == "FAILURE":
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "message": "Task failed",
                    "error": str(task_result.info)
                }
            else:
                return {
                    "task_id": task_id,
                    "status": task_result.state.lower(),
                    "message": f"Task state: {task_result.state}"
                }
        
        return progress
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress: {str(e)}")


@router.get("/progress-stream/{task_id}")
async def stream_task_progress(task_id: str):
    """
    Server-Sent Events (SSE) endpoint for real-time progress updates
    
    Streams progress updates to the client as they happen
    """
    async def event_generator():
        """Generate SSE events for task progress"""
        redis_client = await get_async_redis()
        tracker = AsyncTaskProgressTracker(redis_client)
        
        # Subscribe to progress updates
        pubsub = await tracker.subscribe_to_progress(task_id)
        
        try:
            # Send initial connection message
            yield f"data: {json.dumps({'status': 'connected', 'task_id': task_id})}\n\n"
            
            # Listen for updates
            timeout_counter = 0
            max_timeout = 3600  # 1 hour maximum
            
            while timeout_counter < max_timeout:
                try:
                    # Wait for message with timeout
                    message = await asyncio.wait_for(
                        pubsub.get_message(ignore_subscribe_messages=True),
                        timeout=1.0
                    )
                    
                    if message and message['type'] == 'message':
                        # Send progress update
                        data = message['data']
                        yield f"data: {data}\n\n"
                        
                        # Check if task is complete
                        progress_data = json.loads(data)
                        if progress_data.get('status') in ['completed', 'failed']:
                            break
                    
                    timeout_counter += 1
                
                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    yield f": heartbeat\n\n"
                    timeout_counter += 1
                    continue
        
        finally:
            await pubsub.unsubscribe(f"task_progress_channel:{task_id}")
            await pubsub.close()
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.get("/result/{task_id}", response_model=BulkOperationResult)
async def get_task_result(task_id: str):
    """
    Get final result of a completed bulk operation
    
    Returns detailed results including successes, failures, and errors
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == "PENDING":
            raise HTTPException(status_code=404, detail="Task not found or still queued")
        elif task_result.state == "STARTED":
            raise HTTPException(status_code=400, detail="Task is still processing")
        elif task_result.state == "FAILURE":
            raise HTTPException(
                status_code=500,
                detail=f"Task failed: {str(task_result.info)}"
            )
        elif task_result.state == "SUCCESS":
            result = task_result.result
            return BulkOperationResult(
                task_id=task_id,
                operation_type=result.get("operation_type", "unknown"),
                total_rows=result.get("total", 0),
                successful=result.get("successful", 0),
                failed=result.get("failed", 0),
                errors=result.get("errors", []),
                results=result.get("results", []),
                execution_time_seconds=result.get("execution_time_seconds", 0),
                completed_at=datetime.utcnow()
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown task state: {task_result.state}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching result: {str(e)}")


@router.delete("/cancel/{task_id}")
async def cancel_task(task_id: str):
    """
    Cancel a running bulk operation task
    
    Attempts to revoke the task if it's still queued or processing
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state in ["PENDING", "STARTED"]:
            # Revoke the task
            celery_app.control.revoke(task_id, terminate=True)
            
            # Update progress in Redis
            redis_client = await get_async_redis()
            tracker = AsyncTaskProgressTracker(redis_client)
            
            # Note: We need to use sync Redis for this
            from app.config.redis_config import get_sync_redis, TaskProgressTracker
            sync_redis = get_sync_redis()
            sync_tracker = TaskProgressTracker(sync_redis)
            sync_tracker.set_progress(
                task_id=task_id,
                current=0,
                total=0,
                status="cancelled",
                message="Task cancelled by user"
            )
            
            return {
                "task_id": task_id,
                "status": "cancelled",
                "message": "Task cancellation requested"
            }
        elif task_result.state == "SUCCESS":
            return {
                "task_id": task_id,
                "status": "completed",
                "message": "Task already completed, cannot cancel"
            }
        else:
            return {
                "task_id": task_id,
                "status": task_result.state.lower(),
                "message": f"Task in state {task_result.state}, cancellation may not be possible"
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling task: {str(e)}")


@router.get("/templates/content-generation")
async def get_content_generation_template():
    """
    Download CSV template for bulk content generation
    
    Returns a sample CSV file with correct headers
    """
    template_data = {
        "prompt": [
            "Write a social media post about sustainable living",
            "Create a blog introduction about AI in education"
        ],
        "language": ["hindi", "english"],
        "content_type": ["social_post", "blog"],
        "tone": ["casual", "professional"],
        "platform": ["instagram", "linkedin"],
        "keywords": ["sustainability,eco-friendly", "AI,education,technology"]
    }
    
    df = pd.DataFrame(template_data)
    
    # Convert to CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=content_generation_template.csv"}
    )


@router.get("/templates/translation")
async def get_translation_template():
    """Download CSV template for bulk translation"""
    template_data = {
        "text": [
            "Hello, how are you?",
            "Welcome to our platform"
        ],
        "source_language": ["english", "english"],
        "target_language": ["hindi", "tamil"],
        "preserve_formatting": [True, True]
    }
    
    df = pd.DataFrame(template_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=translation_template.csv"}
    )


@router.get("/templates/scheduling")
async def get_scheduling_template():
    """Download CSV template for bulk scheduling"""
    template_data = {
        "content_id": [1, 2],
        "platform": ["facebook", "instagram"],
        "scheduled_time": ["2024-12-01T10:00:00Z", "2024-12-01T14:00:00Z"],
        "caption": ["Check out our latest post!", "New content alert!"],
        "hashtags": ["#content,#social", "#instagram,#post"]
    }
    
    df = pd.DataFrame(template_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=scheduling_template.csv"}
    )
