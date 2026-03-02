from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.config.database import Base


class TeamRole(str, enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class InviteStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="owned_teams", foreign_keys=[owner_id])
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    invites = relationship("TeamInvite", back_populates="team", cascade="all, delete-orphan")
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_team_owner_created', 'owner_id', 'created_at'),
    )


class TeamMember(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(SQLEnum(TeamRole), default=TeamRole.VIEWER, index=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_team_member_unique', 'team_id', 'user_id', unique=True),
        Index('idx_team_member_role', 'team_id', 'role'),
    )


class TeamInvite(Base):
    __tablename__ = "team_invites"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    role = Column(SQLEnum(TeamRole), default=TeamRole.VIEWER)
    status = Column(SQLEnum(InviteStatus), default=InviteStatus.PENDING, index=True)
    invited_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    invited_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, index=True)
    accepted_at = Column(DateTime, nullable=True)
    
    # Relationships
    team = relationship("Team", back_populates="invites")
    inviter = relationship("User", foreign_keys=[invited_by])
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_invite_email_status', 'email', 'status'),
        Index('idx_invite_team_status', 'team_id', 'status'),
    )


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    content = relationship("Content", foreign_keys=[content_id])
    post = relationship("Post", foreign_keys=[post_id])
    campaign = relationship("Campaign", foreign_keys=[campaign_id])


class ApprovalWorkflow(Base):
    __tablename__ = "approval_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), nullable=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=True, index=True)
    requested_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    approver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String, default="pending", index=True)  # pending, approved, rejected
    notes = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow, index=True)
    reviewed_at = Column(DateTime, nullable=True)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requested_by])
    approver = relationship("User", foreign_keys=[approver_id])
    content = relationship("Content", foreign_keys=[content_id])
    post = relationship("Post", foreign_keys=[post_id])
    campaign = relationship("Campaign", foreign_keys=[campaign_id])
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_approval_status_approver', 'status', 'approver_id'),
        Index('idx_approval_requester_status', 'requested_by', 'status'),
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False, index=True)
    action = Column(String, nullable=False, index=True)  # created, updated, deleted, commented, approved, etc.
    resource_type = Column(String, nullable=False, index=True)  # content, post, campaign, etc.
    resource_id = Column(Integer, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    team = relationship("Team")
    user = relationship("User")
    
    # PostgreSQL-specific indexes
    __table_args__ = (
        Index('idx_activity_team_created', 'team_id', 'created_at'),
        Index('idx_activity_resource', 'resource_type', 'resource_id'),
        Index('idx_activity_user_action', 'user_id', 'action'),
    )
