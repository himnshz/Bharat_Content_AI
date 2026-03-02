from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import bleach
import logging

from app.config.database import get_db
from app.models import Content, ContentType, ContentStatus, ToneType, User
from app.services.content_generation.ai_service_manager import get_ai_service_manager, get_service_info
from app.auth.dependencies import get_current_user, enforce_quota
from app.tasks.content_tasks import generate_content_async
from celery.result import AsyncResult
from app.config.redis_config import get_async_redis, AsyncTaskProgressTracker

router = APIRouter()
logger = logging.getLogger(__name__)

# Request/Response Schemas
class ContentGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000, description="Content generation prompt")
    language: str = Field(default="hindi", description="Target language for content")
    tone: ToneType = Field(default=ToneType.CASUAL, description="Tone of the content")
    content_type: ContentType = Field(default=ContentType.SOCIAL_POST, description="Type of content to generate")
    
    @validator('prompt')
    def validate_prompt(cls, v):
        """Validate and sanitize prompt"""
        # Check for prompt injection patterns
        forbidden_patterns = [
            'ignore previous', 'ignore all previous', 'system:', 'admin:', 
            '<script>', 'javascript:', 'onerror=', 'onclick='
        ]
        v_lower = v.lower()
        for pattern in forbidden_patterns:
            if pattern in v_lower:
                raise ValueError(f'Invalid prompt content detected')
        
        # Sanitize HTML
        v = bleach.clean(v, tags=[], strip=True)
        return v.strip()

class ContentEditRequest(BaseModel):
    edited_content: str = Field(..., min_length=1, description="Edited content text")

class ContentSummarizeRequest(BaseModel):
    content_id: int = Field(..., description="Content ID to summarize")
    target_length: Optional[int] = Field(default=100, description="Target word count for summary")

class ContentResponse(BaseModel):
    id: int
    original_prompt: str
    generated_content: str
    edited_content: Optional[str]
    content_type: ContentType
    status: ContentStatus
    language: str
    tone: ToneType
    model_used: Optional[str]
    generation_time_ms: Optional[int]
    word_count: Optional[int]
    quality_score: Optional[float]
    keywords: Optional[List[str]]
    hashtags: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ContentListResponse(BaseModel):
    total: int
    items: List[ContentResponse]


@router.post("/generate", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_content(
    request: ContentGenerateRequest,
    current_user: User = Depends(enforce_quota("content_generation")),
    db: Session = Depends(get_db)
):
    """
    Generate AI content using any available AI service (Gemini, Bedrock, OpenAI, etc.).
    
    SECURITY:
    - Requires authentication
    - Enforces quota limits based on subscription tier
    - Validates and sanitizes input
    - Sanitizes AI output
    """
    try:
        # Get AI service manager
        ai_manager = get_ai_service_manager()
        
        # Check if any services are available
        if not ai_manager.get_available_services():
            logger.error("No AI services available")
            raise HTTPException(
                status_code=503,
                detail="AI service temporarily unavailable. Please try again later."
            )
        
        # Generate content using best available service
        result = ai_manager.generate_content(
            prompt=request.prompt,
            language=request.language,
            tone=request.tone.value,
            content_type=request.content_type.value
        )
        
        # Sanitize AI-generated content
        generated_text = bleach.clean(result['content'], tags=[], strip=True)
        
        # Calculate metrics
        word_count = len(generated_text.split())
        char_count = len(generated_text)
        
        # Extract keywords and hashtags (simple implementation)
        words = generated_text.split()
        keywords = [w.strip('.,!?') for w in words if len(w) > 5][:10]
        hashtags = [w for w in words if w.startswith('#')]
        
        # Create content record
        content = Content(
            user_id=current_user.id,  # SECURITY: Use authenticated user ID
            original_prompt=request.prompt,
            generated_content=generated_text,
            content_type=request.content_type,
            status=ContentStatus.GENERATED,
            language=request.language,
            tone=request.tone,
            model_used=result.get('model_used'),
            generation_time_ms=result.get('generation_time_ms'),
            word_count=word_count,
            character_count=char_count,
            keywords=keywords,
            hashtags=hashtags,
            quality_score=85.0,
            estimated_reading_time=word_count // 3
        )
        
        db.add(content)
        
        # Update user stats
        current_user.content_generated_count += 1
        
        db.commit()
        db.refresh(content)
        
        logger.info(f"Content generated for user {current_user.id}, content_id={content.id}")
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Content generation failed for user {current_user.id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating content. Please try again."
        )


@router.post("/generate/async", status_code=status.HTTP_202_ACCEPTED)
async def generate_content_async_endpoint(
    request: ContentGenerateRequest,
    current_user: User = Depends(enforce_quota("content_generation")),
    db: Session = Depends(get_db)
):
    """
    Generate AI content asynchronously (non-blocking).
    Returns immediately with task ID for progress tracking.
    
    PERFORMANCE:
    - Non-blocking: Returns in <100ms
    - Background processing: AI generation happens in Celery worker
    - Progress tracking: Use /generate/status/{task_id} to check progress
    
    SECURITY:
    - Requires authentication
    - Enforces quota limits
    """
    try:
        # Start background task
        task = generate_content_async.delay(
            user_id=current_user.id,
            prompt=request.prompt,
            language=request.language,
            tone=request.tone.value,
            content_type=request.content_type.value
        )
        
        logger.info(f"Async content generation started for user {current_user.id}, task_id={task.id}")
        
        return {
            "task_id": task.id,
            "status": "processing",
            "message": "Content generation started. Use /generate/status/{task_id} to check progress.",
            "estimated_time_seconds": 10
        }
        
    except Exception as e:
        logger.error(f"Failed to start async content generation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to start content generation. Please try again."
        )


@router.get("/generate/status/{task_id}")
async def get_generation_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get status of async content generation task.
    
    Returns:
    - status: processing, completed, failed
    - progress: 0-100
    - message: Current status message
    - result: Generated content (when completed)
    """
    try:
        # Check Celery task status
        task = AsyncResult(task_id)
        
        # Get detailed progress from Redis
        redis = await get_async_redis()
        tracker = AsyncTaskProgressTracker(redis)
        progress_data = await tracker.get_progress(task_id)
        
        if progress_data:
            return progress_data
        
        # Fallback to Celery task state
        if task.ready():
            if task.successful():
                return {
                    "task_id": task_id,
                    "status": "completed",
                    "progress": 100,
                    "message": "Content generated successfully",
                    "result": task.result
                }
            else:
                return {
                    "task_id": task_id,
                    "status": "failed",
                    "progress": 0,
                    "message": str(task.info) if task.info else "Task failed"
                }
        else:
            return {
                "task_id": task_id,
                "status": "processing",
                "progress": 50,
                "message": "Generating content..."
            }
            
    except Exception as e:
        logger.error(f"Failed to get task status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve task status"
        )


@router.get("/list", response_model=ContentListResponse)
async def list_content(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
    content_type: Optional[ContentType] = None,
    language: Optional[str] = None,
    status: Optional[ContentStatus] = None,
    db: Session = Depends(get_db)
):
    """
    List all content for authenticated user with optional filters.
    
    SECURITY:
    - User can only see their own content
    - No IDOR vulnerability
    """
    query = db.query(Content).filter(Content.user_id == current_user.id)
    
    if content_type:
        query = query.filter(Content.content_type == content_type)
    if language:
        query = query.filter(Content.language == language)
    if status:
        query = query.filter(Content.status == status)
    
    total = query.count()
    items = query.order_by(Content.created_at.desc()).offset(skip).limit(limit).all()
    
    return ContentListResponse(total=total, items=items)


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific content by ID.
    
    SECURITY:
    - User can only access their own content
    """
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id  # SECURITY: Prevent IDOR
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content


@router.put("/{content_id}/edit", response_model=ContentResponse)
async def edit_content(content_id: int, request: ContentEditRequest, db: Session = Depends(get_db)):
    """
    Edit generated content manually.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.edited_content = request.edited_content
    content.status = ContentStatus.EDITED
    content.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(content)
    
    return content


@router.post("/summarize", response_model=ContentResponse)
async def summarize_content(request: ContentSummarizeRequest, db: Session = Depends(get_db)):
    """
    Generate a summarized version of existing content using any available AI service.
    """
    content = db.query(Content).filter(Content.id == request.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    try:
        # Use AI service manager to summarize
        ai_manager = get_ai_service_manager()
        
        text_to_summarize = content.edited_content or content.generated_content
        
        result = ai_manager.summarize_content(
            text=text_to_summarize,
            target_length=request.target_length,
            language=content.language
        )
        
        # Create new content record for summary
        summary_content = Content(
            user_id=content.user_id,
            original_prompt=f"Summary of content #{content.id}",
            generated_content=result['content'],
            content_type=ContentType.CAPTION,
            status=ContentStatus.GENERATED,
            language=content.language,
            tone=ToneType.PROFESSIONAL,
            model_used=result.get('model_used'),
            generation_time_ms=result.get('generation_time_ms'),
            word_count=len(result['content'].split()),
            parent_content_id=content.id
        )
        
        db.add(summary_content)
        db.commit()
        db.refresh(summary_content)
        
        return summary_content
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a content record.
    
    SECURITY:
    - User can only delete their own content
    """
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.id  # SECURITY: Prevent IDOR
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(content)
    db.commit()
    
    return None


@router.get("/ai-services/status")
async def get_ai_services_status():
    """
    Get information about available AI services and which one is currently being used.
    Useful for debugging and monitoring.
    """
    try:
        service_info = get_service_info()
        return {
            "status": "operational" if service_info["total_available"] > 0 else "no_services",
            **service_info,
            "supported_providers": [
                "gemini", "bedrock", "openai", "anthropic", 
                "cohere", "huggingface", "groq", "together"
            ],
            "configuration_help": {
                "gemini": "Set GEMINI_API_KEY environment variable",
                "bedrock": "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY or AWS_BEARER_TOKEN_BEDROCK",
                "openai": "Set OPENAI_API_KEY environment variable",
                "anthropic": "Set ANTHROPIC_API_KEY environment variable",
                "cohere": "Set COHERE_API_KEY environment variable",
                "huggingface": "Set HUGGINGFACE_API_KEY environment variable",
                "groq": "Set GROQ_API_KEY environment variable",
                "together": "Set TOGETHER_API_KEY environment variable"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get service status: {str(e)}")
