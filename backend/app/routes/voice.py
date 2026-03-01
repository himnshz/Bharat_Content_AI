from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import os

from app.config.database import get_db
from app.models import VoiceInput, VoiceInputStatus, User

router = APIRouter()

# Response Schemas
class VoiceInputResponse(BaseModel):
    id: int
    user_id: int
    audio_file_url: str
    audio_duration_seconds: Optional[float]
    audio_format: Optional[str]
    transcribed_text: Optional[str]
    language_detected: Optional[str]
    language_specified: Optional[str]
    status: VoiceInputStatus
    confidence_score: Optional[float]
    word_count: Optional[int]
    processing_time_ms: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class VoiceInputListResponse(BaseModel):
    total: int
    items: List[VoiceInputResponse]

class TranscriptionRequest(BaseModel):
    voice_input_id: int = Field(..., description="Voice input ID to transcribe")
    language: Optional[str] = Field(None, description="Expected language (for better accuracy)")


@router.post("/upload", response_model=VoiceInputResponse, status_code=status.HTTP_201_CREATED)
async def upload_voice_input(
    user_id: int,
    audio_file: UploadFile = File(...),
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Upload an audio file for voice-to-text transcription.
    Supports MP3, WAV, M4A, and other common audio formats.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate file type
        allowed_formats = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-m4a', 'audio/ogg']
        if audio_file.content_type not in allowed_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Allowed: {', '.join(allowed_formats)}"
            )
        
        # Read file content
        file_content = await audio_file.read()
        file_size = len(file_content)
        
        # Validate file size (max 25MB)
        max_size = 25 * 1024 * 1024  # 25MB
        if file_size > max_size:
            raise HTTPException(status_code=400, detail="File size exceeds 25MB limit")
        
        # TODO: Upload to AWS S3
        # For now, create a mock S3 URL
        timestamp = int(datetime.utcnow().timestamp())
        file_key = f"voice-inputs/{user_id}/{timestamp}_{audio_file.filename}"
        audio_url = f"https://bharat-content-ai.s3.amazonaws.com/{file_key}"
        
        # Extract audio format
        audio_format = audio_file.filename.split('.')[-1] if '.' in audio_file.filename else 'unknown'
        
        # Create voice input record
        voice_input = VoiceInput(
            user_id=user_id,
            audio_file_url=audio_url,
            audio_file_key=file_key,
            audio_format=audio_format,
            audio_size_bytes=file_size,
            language_specified=language,
            status=VoiceInputStatus.PROCESSING
        )
        
        db.add(voice_input)
        db.commit()
        db.refresh(voice_input)
        
        # TODO: Trigger AWS Transcribe job asynchronously
        # transcribe_audio_async(voice_input.id, audio_url, language)
        
        return voice_input
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload audio: {str(e)}")


@router.post("/transcribe", response_model=VoiceInputResponse)
async def transcribe_audio(request: TranscriptionRequest, db: Session = Depends(get_db)):
    """
    Manually trigger transcription for an uploaded audio file.
    In production, this would be called automatically after upload.
    """
    try:
        voice_input = db.query(VoiceInput).filter(VoiceInput.id == request.voice_input_id).first()
        if not voice_input:
            raise HTTPException(status_code=404, detail="Voice input not found")
        
        if voice_input.status == VoiceInputStatus.COMPLETED:
            return voice_input
        
        # TODO: Integrate with AWS Transcribe
        # For now, mock transcription
        start_time = datetime.utcnow()
        
        # Simulate transcription
        mock_transcription = "This is a mock transcription of the audio file. In production, this would be the actual transcribed text from AWS Transcribe."
        detected_language = request.language or voice_input.language_specified or "hindi"
        
        voice_input.transcribed_text = mock_transcription
        voice_input.language_detected = detected_language
        voice_input.status = VoiceInputStatus.COMPLETED
        voice_input.confidence_score = 95.5
        voice_input.word_count = len(mock_transcription.split())
        voice_input.audio_duration_seconds = 45.0
        voice_input.completed_at = datetime.utcnow()
        
        end_time = datetime.utcnow()
        voice_input.processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
        
        db.commit()
        db.refresh(voice_input)
        
        return voice_input
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        voice_input.status = VoiceInputStatus.FAILED
        voice_input.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.get("/list", response_model=VoiceInputListResponse)
async def list_voice_inputs(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    status: Optional[VoiceInputStatus] = None,
    db: Session = Depends(get_db)
):
    """
    List all voice inputs for a user.
    """
    query = db.query(VoiceInput).filter(VoiceInput.user_id == user_id)
    
    if status:
        query = query.filter(VoiceInput.status == status)
    
    total = query.count()
    items = query.order_by(VoiceInput.created_at.desc()).offset(skip).limit(limit).all()
    
    return VoiceInputListResponse(total=total, items=items)


@router.get("/{voice_input_id}", response_model=VoiceInputResponse)
async def get_voice_input(voice_input_id: int, db: Session = Depends(get_db)):
    """
    Get a specific voice input by ID.
    """
    voice_input = db.query(VoiceInput).filter(VoiceInput.id == voice_input_id).first()
    if not voice_input:
        raise HTTPException(status_code=404, detail="Voice input not found")
    return voice_input


@router.post("/{voice_input_id}/to-content")
async def convert_voice_to_content(voice_input_id: int, db: Session = Depends(get_db)):
    """
    Convert transcribed voice input directly to content generation using any available AI service.
    """
    from app.models import Content, ContentType, ContentStatus, ToneType
    from app.services.content_generation.ai_service_manager import get_ai_service_manager
    
    voice_input = db.query(VoiceInput).filter(VoiceInput.id == voice_input_id).first()
    if not voice_input:
        raise HTTPException(status_code=404, detail="Voice input not found")
    
    if voice_input.status != VoiceInputStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Voice input not yet transcribed")
    
    if not voice_input.transcribed_text:
        raise HTTPException(status_code=400, detail="No transcribed text available")
    
    try:
        # Use AI service manager
        ai_manager = get_ai_service_manager()
        
        result = ai_manager.generate_content(
            prompt=voice_input.transcribed_text,
            language=voice_input.language_detected or "hindi",
            tone="casual",
            content_type="social_post"
        )
        
        # Create content record
        content = Content(
            user_id=voice_input.user_id,
            original_prompt=f"Voice input: {voice_input.transcribed_text}",
            generated_content=result['content'],
            content_type=ContentType.SOCIAL_POST,
            status=ContentStatus.GENERATED,
            language=voice_input.language_detected or "hindi",
            tone=ToneType.CASUAL,
            model_used=result.get('model_used'),
            generation_time_ms=result.get('generation_time_ms'),
            word_count=len(result['content'].split())
        )
        
        db.add(content)
        db.commit()
        db.refresh(content)
        
        return {
            "status": "success",
            "voice_input_id": voice_input_id,
            "content_id": content.id,
            "generated_content": content.generated_content,
            "ai_service_used": result.get('service_used')
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to convert voice to content: {str(e)}")


@router.delete("/{voice_input_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voice_input(voice_input_id: int, db: Session = Depends(get_db)):
    """
    Delete a voice input record.
    """
    voice_input = db.query(VoiceInput).filter(VoiceInput.id == voice_input_id).first()
    if not voice_input:
        raise HTTPException(status_code=404, detail="Voice input not found")
    
    # TODO: Delete audio file from S3
    # delete_from_s3(voice_input.audio_file_key)
    
    db.delete(voice_input)
    db.commit()
    
    return None
