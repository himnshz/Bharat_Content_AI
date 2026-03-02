"""
Pydantic Schemas for Bulk Operations
Validates CSV data and API requests
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BulkOperationType(str, Enum):
    """Types of bulk operations"""
    CONTENT_GENERATION = "content_generation"
    TRANSLATION = "translation"
    SCHEDULING = "scheduling"
    MIXED = "mixed"


class ContentGenerationRow(BaseModel):
    """Schema for bulk content generation CSV row"""
    prompt: str = Field(..., min_length=10, max_length=5000, description="Content generation prompt")
    language: str = Field(default="hindi", description="Target language")
    content_type: str = Field(default="social_post", description="Type of content")
    tone: str = Field(default="casual", description="Content tone")
    platform: Optional[str] = Field(None, description="Target platform")
    keywords: Optional[str] = Field(None, description="Comma-separated keywords")
    
    @validator("language")
    def validate_language(cls, v):
        valid_languages = ["hindi", "english", "tamil", "telugu", "bengali", "marathi", "gujarati", "kannada"]
        if v.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v.lower()
    
    @validator("content_type")
    def validate_content_type(cls, v):
        valid_types = ["social_post", "blog", "article", "caption", "script", "email", "ad_copy"]
        if v.lower() not in valid_types:
            raise ValueError(f"Content type must be one of: {', '.join(valid_types)}")
        return v.lower()
    
    @validator("tone")
    def validate_tone(cls, v):
        valid_tones = ["casual", "formal", "professional", "friendly", "humorous", "inspirational", "educational"]
        if v.lower() not in valid_tones:
            raise ValueError(f"Tone must be one of: {', '.join(valid_tones)}")
        return v.lower()


class TranslationRow(BaseModel):
    """Schema for bulk translation CSV row"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    source_language: str = Field(..., description="Source language")
    target_language: str = Field(..., description="Target language")
    preserve_formatting: bool = Field(default=True, description="Preserve text formatting")
    
    @validator("source_language", "target_language")
    def validate_language(cls, v):
        valid_languages = ["hindi", "english", "tamil", "telugu", "bengali", "marathi", "gujarati", "kannada"]
        if v.lower() not in valid_languages:
            raise ValueError(f"Language must be one of: {', '.join(valid_languages)}")
        return v.lower()


class SchedulingRow(BaseModel):
    """Schema for bulk scheduling CSV row"""
    content_id: int = Field(..., description="ID of content to schedule")
    platform: str = Field(..., description="Social media platform")
    scheduled_time: str = Field(..., description="Schedule time (ISO format)")
    caption: Optional[str] = Field(None, max_length=2000, description="Post caption")
    hashtags: Optional[str] = Field(None, description="Comma-separated hashtags")
    
    @validator("platform")
    def validate_platform(cls, v):
        valid_platforms = ["facebook", "instagram", "twitter", "linkedin", "youtube", "pinterest", "tiktok"]
        if v.lower() not in valid_platforms:
            raise ValueError(f"Platform must be one of: {', '.join(valid_platforms)}")
        return v.lower()
    
    @validator("scheduled_time")
    def validate_scheduled_time(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("scheduled_time must be in ISO format (e.g., 2024-01-01T12:00:00Z)")
        return v


class BulkOperationRequest(BaseModel):
    """Request schema for bulk operation"""
    operation_type: BulkOperationType
    user_id: int
    batch_size: int = Field(default=10, ge=1, le=100, description="Number of items to process per batch")
    priority: int = Field(default=5, ge=1, le=10, description="Task priority (1=low, 10=high)")


class BulkOperationResponse(BaseModel):
    """Response schema for bulk operation"""
    task_id: str
    operation_type: str
    total_rows: int
    status: str
    message: str
    progress_url: str
    estimated_time_seconds: Optional[int] = None


class TaskProgress(BaseModel):
    """Task progress schema"""
    task_id: str
    current: int
    total: int
    percentage: float
    status: str
    message: str
    result: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict[str, Any]]] = None


class BulkOperationResult(BaseModel):
    """Final result of bulk operation"""
    task_id: str
    operation_type: str
    total_rows: int
    successful: int
    failed: int
    errors: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    execution_time_seconds: float
    completed_at: datetime


class CSVValidationError(BaseModel):
    """CSV validation error"""
    row_number: int
    field: str
    error: str
    value: Any


class CSVValidationResult(BaseModel):
    """CSV validation result"""
    valid: bool
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: List[CSVValidationError]
    sample_data: Optional[List[Dict[str, Any]]] = None
