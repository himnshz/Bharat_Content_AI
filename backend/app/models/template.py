from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base


class TemplateCategory(str, enum.Enum):
    SOCIAL_MEDIA = "social_media"
    BLOG = "blog"
    EMAIL = "email"
    MARKETING = "marketing"
    ANNOUNCEMENT = "announcement"
    PRODUCT = "product"
    EVENT = "event"
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    NEWS = "news"


class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)  # Null for system templates
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(TemplateCategory), nullable=False, index=True)
    content = Column(Text, nullable=False)
    
    # Template metadata
    language = Column(String, default="english", index=True)
    tone = Column(String, default="professional")
    platform = Column(String, nullable=True, index=True)  # facebook, instagram, twitter, etc.
    
    # Template settings
    is_public = Column(Boolean, default=False, index=True)  # Can other users see this?
    is_system = Column(Boolean, default=False, index=True)  # System-provided template
    is_favorite = Column(Boolean, default=False)
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_template_category_public', 'category', 'is_public'),
        Index('idx_template_user_category', 'user_id', 'category'),
        Index('idx_template_platform_language', 'platform', 'language'),
    )
    
    def __repr__(self):
        return f"<Template {self.name}>"
