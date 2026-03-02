from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base

class ContentType(str, enum.Enum):
    SOCIAL_POST = "social_post"
    BLOG = "blog"
    ARTICLE = "article"
    CAPTION = "caption"
    SCRIPT = "script"
    EMAIL = "email"
    AD_COPY = "ad_copy"

class ContentStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    EDITED = "edited"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class ToneType(str, enum.Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"

class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Content details
    title = Column(String(500))
    original_prompt = Column(Text, nullable=False)
    generated_content = Column(Text, nullable=False)
    edited_content = Column(Text)  # User can edit generated content
    
    # Content metadata
    content_type = Column(SQLEnum(ContentType), default=ContentType.SOCIAL_POST)
    status = Column(SQLEnum(ContentStatus), default=ContentStatus.GENERATED)
    language = Column(String(50), nullable=False, index=True)
    tone = Column(SQLEnum(ToneType), default=ToneType.CASUAL)
    
    # AI model information
    model_used = Column(String(100))  # e.g., "bedrock-claude-v2", "bedrock-llama-2"
    model_version = Column(String(50))
    generation_time_ms = Column(Integer)  # Time taken to generate
    
    # AWS Bedrock specific
    bedrock_model_id = Column(String(255))  # e.g., "anthropic.claude-v2"
    bedrock_request_id = Column(String(255))
    
    # Content analysis
    word_count = Column(Integer)
    character_count = Column(Integer)
    estimated_reading_time = Column(Integer)  # in seconds
    
    # SEO and keywords
    keywords = Column(JSONB)  # List of extracted keywords - PostgreSQL JSONB for better performance
    hashtags = Column(JSONB)  # Suggested hashtags
    
    # Quality metrics
    quality_score = Column(Float)  # AI-generated quality score (0-100)
    sentiment_score = Column(Float)  # Sentiment analysis (-1 to 1)
    
    # Engagement prediction (ML-based)
    predicted_engagement_score = Column(Float)
    
    # Version control
    version = Column(Integer, default=1)
    parent_content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="contents")
    posts = relationship("Post", back_populates="content")
    translations = relationship("Translation", back_populates="content", cascade="all, delete-orphan")
    
    # PostgreSQL-specific indexes for performance
    __table_args__ = (
        Index('idx_content_user_status', 'user_id', 'status'),
        Index('idx_content_language_type', 'language', 'content_type'),
        Index('idx_content_created_at', 'created_at'),
        Index('idx_content_keywords_gin', 'keywords', postgresql_using='gin'),  # GIN index for JSONB
        Index('idx_content_hashtags_gin', 'hashtags', postgresql_using='gin'),  # GIN index for JSONB
    )
    
    def __repr__(self):
        return f"<Content {self.id} - {self.language} - {self.content_type}>"
