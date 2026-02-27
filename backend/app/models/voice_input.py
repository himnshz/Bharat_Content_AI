from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base

class VoiceInputStatus(str, enum.Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class VoiceInput(Base):
    __tablename__ = "voice_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Audio file details
    audio_file_url = Column(String(1000), nullable=False)  # S3 URL
    audio_file_key = Column(String(500))  # S3 key
    audio_duration_seconds = Column(Float)
    audio_format = Column(String(50))  # mp3, wav, etc.
    audio_size_bytes = Column(Integer)
    
    # Transcription details
    transcribed_text = Column(Text)
    language_detected = Column(String(50))
    language_specified = Column(String(50))  # User-specified language
    
    # AWS Transcribe specific
    transcribe_job_name = Column(String(255))
    transcribe_job_status = Column(String(50))
    
    # Processing status
    status = Column(SQLEnum(VoiceInputStatus), default=VoiceInputStatus.PROCESSING, index=True)
    
    # Quality metrics
    confidence_score = Column(Float)  # Average confidence of transcription
    word_count = Column(Integer)
    
    # Speaker identification (if multiple speakers)
    speaker_count = Column(Integer, default=1)
    speaker_labels = Column(Text)  # JSON string with speaker segments
    
    # Processing time
    processing_time_ms = Column(Integer)
    
    # Error handling
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<VoiceInput {self.id} - {self.language_detected} - {self.status}>"
