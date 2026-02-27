from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Enum as SQLEnum
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

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Platform details
    platform = Column(SQLEnum(Platform), nullable=False, index=True)
    platform_user_id = Column(String(255), nullable=False)
    platform_username = Column(String(255))
    
    # Authentication
    access_token = Column(String(1000))  # Encrypted in production
    refresh_token = Column(String(1000))  # Encrypted in production
    token_expires_at = Column(DateTime)
    
    # Account information
    account_name = Column(String(255))
    profile_picture_url = Column(String(1000))
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Permissions
    permissions = Column(JSON)  # List of granted permissions
    
    # AWS Secrets Manager integration
    secret_arn = Column(String(500))  # ARN for stored credentials in AWS Secrets Manager
    
    # Rate limiting
    daily_post_limit = Column(Integer, default=10)
    posts_today = Column(Integer, default=0)
    last_post_date = Column(DateTime)
    
    # Timestamps
    connected_at = Column(DateTime, default=datetime.utcnow)
    last_synced_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="social_accounts")
    
    def __repr__(self):
        return f"<SocialAccount {self.platform} - {self.platform_username}>"
