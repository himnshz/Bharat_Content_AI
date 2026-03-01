from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.config.database import get_db
from app.models import Content, ContentType, ContentStatus, ToneType, User
from app.services.content_generation.ai_service_manager import get_ai_service_manager, get_service_info

router = APIRouter()

# Request/Response Schemas
class ContentGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=5000, description="Content generation prompt")
    language: str = Field(default="hindi", description="Target language for content")
    tone: ToneType = Field(default=ToneType.CASUAL, description="Tone of the content")
    content_type: ContentType = Field(default=ContentType.SOCIAL_POST, description="Type of content to generate")
    user_id: int = Field(..., description="User ID")

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
async def generate_content(request: ContentGenerateRequest, db: Session = Depends(get_db)):
    """
    Generate AI content using any available AI service (Gemini, Bedrock, OpenAI, etc.).
    Automatically selects the best available service based on configured API keys.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get AI service manager
        ai_manager = get_ai_service_manager()
        
        # Check if any services are available
        if not ai_manager.get_available_services():
            raise HTTPException(
                status_code=503,
                detail="No AI services available. Please configure at least one API key (GEMINI_API_KEY, AWS credentials, OPENAI_API_KEY, etc.)"
            )
        
        # Generate content using best available service
        result = ai_manager.generate_content(
            prompt=request.prompt,
            language=request.language,
            tone=request.tone.value,
            content_type=request.content_type.value
        )
        
        # Calculate metrics
        generated_text = result['content']
        word_count = len(generated_text.split())
        char_count = len(generated_text)
        
        # Extract keywords and hashtags (simple implementation)
        words = generated_text.split()
        keywords = [w.strip('.,!?') for w in words if len(w) > 5][:10]
        hashtags = [w for w in words if w.startswith('#')]
        
        # Create content record
        content = Content(
            user_id=request.user_id,
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
            quality_score=85.0,  # Placeholder - can be enhanced with quality analysis
            estimated_reading_time=word_count // 3  # ~180 words per minute
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        # Update user stats
        user.content_generated_count += 1
        db.commit()
        
        return content
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")


@router.get("/list", response_model=ContentListResponse)
async def list_content(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    content_type: Optional[ContentType] = None,
    language: Optional[str] = None,
    status: Optional[ContentStatus] = None,
    db: Session = Depends(get_db)
):
    """
    List all content for a user with optional filters.
    """
    query = db.query(Content).filter(Content.user_id == user_id)
    
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
async def get_content(content_id: int, db: Session = Depends(get_db)):
    """
    Get a specific content by ID.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
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
async def delete_content(content_id: int, db: Session = Depends(get_db)):
    """
    Delete a content record.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
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
