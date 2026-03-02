from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Boolean, Text, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base

class Platform(str, enum.Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=True)
    
    # Post details
    title = Column(String(500))
    text_content = Column(Text, nullable=False)
    
    # Platform specific
    platform = Column(SQLEnum(Platform), nullable=False, index=True)
    status = Column(SQLEnum(PostStatus), default=PostStatus.DRAFT, index=True)
    
    # Media attachments
    media_urls = Column(JSON)  # List of image/video URLs
    media_type = Column(String(50))  # image, video, carousel, etc.
    
    # Scheduling
    scheduled_time = Column(DateTime, index=True)
    published_time = Column(DateTime)
    
    # Platform-specific data
    platform_post_id = Column(String(255))  # ID from the social platform
    platform_url = Column(String(1000))  # Direct link to the post
    
    # Engagement metrics (updated periodically)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    # Engagement rate calculation
    engagement_rate = Column(Integer, default=0)  # Percentage
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    # AWS EventBridge integration
    eventbridge_rule_name = Column(String(255))  # For scheduled posts
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_synced_at = Column(DateTime)  # Last time metrics were synced
    
    # Relationships
    user = relationship("User", back_populates="posts")
    content = relationship("Content", back_populates="posts")
    
    # Performance indexes for common queries
    __table_args__ = (
        Index('idx_post_user_schedule', 'user_id', 'scheduled_time'),
        Index('idx_post_user_platform_status', 'user_id', 'platform', 'status'),
        Index('idx_post_scheduled_status', 'scheduled_time', 'status'),
    )
    
    def __repr__(self):
        return f"<Post {self.id} - {self.platform} - {self.status}>"
