from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum, Float
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
    keywords = Column(JSON)  # List of extracted keywords
    hashtags = Column(JSON)  # Suggested hashtags
    
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
    
    def __repr__(self):
        return f"<Content {self.id} - {self.language} - {self.content_type}>"
