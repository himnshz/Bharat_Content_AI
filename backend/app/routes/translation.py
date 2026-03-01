from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.config.database import get_db
from app.models import Translation, TranslationMethod, Content, User

router = APIRouter()

# Request/Response Schemas
class TranslationRequest(BaseModel):
    content_id: int = Field(..., description="Content ID to translate")
    target_language: str = Field(..., description="Target language code (e.g., 'hindi', 'tamil', 'bengali')")
    source_language: Optional[str] = Field(None, description="Source language (auto-detected if not provided)")
    maintain_tone: bool = Field(default=True, description="Whether to maintain the original tone")
    cultural_adaptation: bool = Field(default=False, description="Adapt content for cultural context")

class DirectTranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    source_language: str = Field(..., description="Source language")
    target_language: str = Field(..., description="Target language")
    tone: Optional[str] = Field(default="neutral", description="Desired tone")
    user_id: int = Field(..., description="User ID")

class TranslationResponse(BaseModel):
    id: int
    content_id: int
    source_language: str
    target_language: str
    original_text: str
    translated_text: str
    method: TranslationMethod
    quality_score: Optional[float]
    translation_time_ms: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TranslationListResponse(BaseModel):
    total: int
    items: List[TranslationResponse]


# Supported Indian languages
SUPPORTED_LANGUAGES = {
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "bengali": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "kannada": "kn",
    "malayalam": "ml",
    "punjabi": "pa",
    "odia": "or",
    "english": "en"
}


@router.post("/translate", response_model=TranslationResponse, status_code=status.HTTP_201_CREATED)
async def translate_content(request: TranslationRequest, db: Session = Depends(get_db)):
    """
    Translate existing content to a target Indian language using IndicTrans.
    """
    try:
        # Verify content exists
        content = db.query(Content).filter(Content.id == request.content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Validate target language
        if request.target_language.lower() not in SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language. Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            )
        
        # Get source text
        source_text = content.edited_content or content.generated_content
        source_lang = request.source_language or content.language
        
        # Check if translation already exists
        existing = db.query(Translation).filter(
            Translation.content_id == request.content_id,
            Translation.target_language == request.target_language
        ).first()
        
        if existing:
            return existing
        
        # TODO: Integrate with IndicTrans model
        # For now, mock translation
        start_time = datetime.utcnow()
        
        # Simulate translation
        translated_text = f"[Translated to {request.target_language}] {source_text}"
        
        if request.cultural_adaptation:
            translated_text += f"\n[Culturally adapted for {request.target_language} audience]"
        
        end_time = datetime.utcnow()
        translation_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Create translation record
        translation = Translation(
            content_id=request.content_id,
            source_language=source_lang,
            target_language=request.target_language,
            source_text=source_text,
            translated_text=translated_text,
            method=TranslationMethod.INDIC_TRANS,
            quality_score=92.5,  # Mock quality score
            translation_time_ms=translation_time,
            model_version="indictrans-v2"
        )
        
        db.add(translation)
        db.commit()
        db.refresh(translation)
        
        # Update user translation count
        user = db.query(User).filter(User.id == content.user_id).first()
        if user:
            user.translations_count += 1
            db.commit()
        
        return translation
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.post("/translate/direct", response_model=TranslationResponse, status_code=status.HTTP_201_CREATED)
async def translate_text_direct(request: DirectTranslationRequest, db: Session = Depends(get_db)):
    """
    Translate text directly without creating content first.
    Useful for quick translations.
    """
    try:
        # Verify user exists
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate languages
        if request.source_language.lower() not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported source language")
        if request.target_language.lower() not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported target language")
        
        # TODO: Integrate with IndicTrans
        start_time = datetime.utcnow()
        translated_text = f"[{request.target_language}] {request.text}"
        end_time = datetime.utcnow()
        translation_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Create a temporary content record for the translation
        from app.models import ContentType, ContentStatus, ToneType
        
        temp_content = Content(
            user_id=request.user_id,
            original_prompt="Direct translation",
            generated_content=request.text,
            content_type=ContentType.SOCIAL_POST,
            status=ContentStatus.GENERATED,
            language=request.source_language,
            tone=ToneType.CASUAL
        )
        
        db.add(temp_content)
        db.flush()
        
        # Create translation record
        translation = Translation(
            content_id=temp_content.id,
            source_language=request.source_language,
            target_language=request.target_language,
            source_text=request.text,
            translated_text=translated_text,
            method=TranslationMethod.INDIC_TRANS,
            quality_score=90.0,
            translation_time_ms=translation_time
        )
        
        db.add(translation)
        db.commit()
        db.refresh(translation)
        
        # Update user stats
        user.translations_count += 1
        db.commit()
        
        return translation
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Direct translation failed: {str(e)}")


@router.get("/list/{content_id}", response_model=TranslationListResponse)
async def list_translations(content_id: int, db: Session = Depends(get_db)):
    """
    List all translations for a specific content.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    translations = db.query(Translation).filter(
        Translation.content_id == content_id
    ).order_by(Translation.created_at.desc()).all()
    
    return TranslationListResponse(
        total=len(translations),
        items=translations
    )


@router.get("/{translation_id}", response_model=TranslationResponse)
async def get_translation(translation_id: int, db: Session = Depends(get_db)):
    """
    Get a specific translation by ID.
    """
    translation = db.query(Translation).filter(Translation.id == translation_id).first()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation


class BatchTranslateRequest(BaseModel):
    content_id: int = Field(..., description="Content ID to translate")
    target_languages: List[str] = Field(..., min_items=1, description="List of target languages")

@router.post("/batch", response_model=List[TranslationResponse], status_code=status.HTTP_201_CREATED)
async def batch_translate(
    request: BatchTranslateRequest,
    db: Session = Depends(get_db)
):
    """
    Translate content to multiple languages at once.
    """
    content_id = request.content_id
    target_languages = request.target_languages
    try:
        content = db.query(Content).filter(Content.id == content_id).first()
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        # Validate all languages
        for lang in target_languages:
            if lang.lower() not in SUPPORTED_LANGUAGES:
                raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")
        
        translations = []
        source_text = content.edited_content or content.generated_content
        
        for target_lang in target_languages:
            # Check if translation exists
            existing = db.query(Translation).filter(
                Translation.content_id == content_id,
                Translation.target_language == target_lang
            ).first()
            
            if existing:
                translations.append(existing)
                continue
            
            # Create new translation
            translated_text = f"[Translated to {target_lang}] {source_text}"
            
            translation = Translation(
                content_id=content_id,
                source_language=content.language,
                target_language=target_lang,
                source_text=source_text,
                translated_text=translated_text,
                method=TranslationMethod.INDIC_TRANS,
                quality_score=90.0,
                translation_time_ms=500
            )
            
            db.add(translation)
            translations.append(translation)
        
        db.commit()
        
        # Refresh all translations
        for translation in translations:
            db.refresh(translation)
        
        # Update user stats
        user = db.query(User).filter(User.id == content.user_id).first()
        if user:
            user.translations_count += len([t for t in translations if t.id])
            db.commit()
        
        return translations
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Batch translation failed: {str(e)}")


@router.get("/languages/supported")
async def get_supported_languages():
    """
    Get list of all supported languages for translation.
    """
    return {
        "languages": [
            {"name": lang, "code": code}
            for lang, code in SUPPORTED_LANGUAGES.items()
        ],
        "total": len(SUPPORTED_LANGUAGES)
    }


@router.delete("/{translation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_translation(translation_id: int, db: Session = Depends(get_db)):
    """
    Delete a translation record.
    """
    translation = db.query(Translation).filter(Translation.id == translation_id).first()
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    db.delete(translation)
    db.commit()
    
    return None
