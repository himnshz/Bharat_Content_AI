from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.config.database import Base

class UserRole(str, enum.Enum):
    STUDENT = "student"
    YOUTUBER = "youtuber"
    BUSINESS = "business"
    TEACHER = "teacher"
    STARTUP = "startup"

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    
    # User profile
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, index=True)
    subscription_tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, index=True)
    preferred_language = Column(String(50), default="hindi")
    
    # Account status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Usage tracking
    content_generated_count = Column(Integer, default=0)
    translations_count = Column(Integer, default=0)
    posts_scheduled_count = Column(Integer, default=0)
    
    # AWS Cognito integration (optional)
    cognito_user_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Relationships
    contents = relationship("Content", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    social_accounts = relationship("SocialAccount", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("Analytics", back_populates="user", cascade="all, delete-orphan")
    owned_teams = relationship("Team", back_populates="owner", foreign_keys="Team.owner_id")
    team_memberships = relationship("TeamMember", back_populates="user")

    # PostgreSQL-specific indexes for performance
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_role_tier', 'role', 'subscription_tier'),
        Index('idx_user_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"
