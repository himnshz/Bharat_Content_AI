from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Date tracking
    date = Column(Date, nullable=False, index=True)
    
    # Content metrics
    content_generated = Column(Integer, default=0)
    translations_made = Column(Integer, default=0)
    posts_scheduled = Column(Integer, default=0)
    posts_published = Column(Integer, default=0)
    
    # Engagement metrics (aggregated from all posts)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_reach = Column(Integer, default=0)
    total_impressions = Column(Integer, default=0)
    
    # Average engagement rate
    avg_engagement_rate = Column(Float, default=0.0)
    
    # Language breakdown
    language_usage = Column(JSON)  # {"hindi": 10, "tamil": 5, ...}
    
    # Platform breakdown
    platform_usage = Column(JSON)  # {"facebook": 5, "instagram": 8, ...}
    
    # Content type breakdown
    content_type_usage = Column(JSON)  # {"social_post": 10, "blog": 2, ...}
    
    # Best performing content
    top_post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    top_post_engagement = Column(Integer, default=0)
    
    # AI usage metrics
    total_tokens_used = Column(Integer, default=0)  # For LLM tracking
    total_api_calls = Column(Integer, default=0)
    avg_generation_time_ms = Column(Integer, default=0)
    
    # AWS cost tracking (optional)
    estimated_cost_usd = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analytics")
    
    def __repr__(self):
        return f"<Analytics {self.user_id} - {self.date}>"


class ContentPerformance(Base):
    """Detailed performance tracking for individual content pieces"""
    __tablename__ = "content_performance"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True, index=True)
    
    # Time-series metrics
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Snapshot metrics
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    # Calculated metrics
    engagement_rate = Column(Float, default=0.0)
    virality_score = Column(Float, default=0.0)
    
    # Audience demographics (from platform APIs)
    audience_demographics = Column(JSON)
    
    # Geographic data
    top_countries = Column(JSON)
    top_cities = Column(JSON)
    
    # Device breakdown
    device_breakdown = Column(JSON)  # {"mobile": 70, "desktop": 30}
    
    def __repr__(self):
        return f"<ContentPerformance {self.content_id} - {self.timestamp}>"
