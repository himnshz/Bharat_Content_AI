from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base

class CampaignStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CampaignType(str, enum.Enum):
    INFLUENCER = "influencer"
    BRAND = "brand"
    PRODUCT_LAUNCH = "product_launch"
    AWARENESS = "awareness"
    ENGAGEMENT = "engagement"
    CONVERSION = "conversion"

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Campaign details
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    campaign_type = Column(SQLEnum(CampaignType), default=CampaignType.AWARENESS)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT, index=True)
    
    # Campaign objectives
    objectives = Column(JSONB)  # List of campaign objectives - PostgreSQL JSONB
    target_audience = Column(JSONB)  # Demographics, interests, etc.
    
    # Budget and timeline
    budget = Column(Float)  # Total campaign budget
    currency = Column(String(10), default="USD")
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    
    # Platform targeting
    platforms = Column(JSONB)  # List of platforms (facebook, instagram, etc.)
    
    # Content requirements
    content_guidelines = Column(Text)  # Brand guidelines, dos and don'ts
    hashtags = Column(JSONB)  # Required hashtags
    mentions = Column(JSONB)  # Required mentions
    
    # Creators/Influencers
    creator_ids = Column(JSONB)  # List of creator/influencer IDs
    min_followers = Column(Integer)  # Minimum follower requirement
    max_creators = Column(Integer)  # Maximum number of creators
    
    # Performance metrics
    target_reach = Column(Integer)
    target_impressions = Column(Integer)
    target_engagement_rate = Column(Float)
    target_conversions = Column(Integer)
    
    # Actual metrics (updated as campaign runs)
    actual_reach = Column(Integer, default=0)
    actual_impressions = Column(Integer, default=0)
    actual_engagement_rate = Column(Float, default=0.0)
    actual_conversions = Column(Integer, default=0)
    
    # ROI tracking
    total_spent = Column(Float, default=0.0)
    revenue_generated = Column(Float, default=0.0)
    roi = Column(Float, default=0.0)  # Return on Investment percentage
    
    # Approval workflow
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime)
    
    # Campaign assets
    brand_assets = Column(JSONB)  # URLs to logos, images, videos
    landing_page_url = Column(String(1000))
    tracking_links = Column(JSONB)  # UTM links for tracking
    
    # Collaboration
    team_members = Column(JSONB)  # List of user IDs with access
    notes = Column(Text)  # Internal notes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="campaigns")
    approver = relationship("User", foreign_keys=[approved_by])
    
    # PostgreSQL-specific indexes for performance
    __table_args__ = (
        Index('idx_campaign_user_status', 'user_id', 'status'),
        Index('idx_campaign_dates', 'start_date', 'end_date'),
        Index('idx_campaign_type_status', 'campaign_type', 'status'),
        Index('idx_campaign_platforms_gin', 'platforms', postgresql_using='gin'),
        Index('idx_campaign_creator_ids_gin', 'creator_ids', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<Campaign {self.id} - {self.name} - {self.status}>"
    
    @property
    def is_active(self):
        """Check if campaign is currently active"""
        if self.status != CampaignStatus.ACTIVE:
            return False
        now = datetime.utcnow()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        return True
    
    @property
    def days_remaining(self):
        """Calculate days remaining in campaign"""
        if not self.end_date:
            return None
        now = datetime.utcnow()
        if now > self.end_date:
            return 0
        return (self.end_date - now).days
    
    @property
    def budget_spent_percentage(self):
        """Calculate percentage of budget spent"""
        if not self.budget or self.budget == 0:
            return 0
        return (self.total_spent / self.budget) * 100
