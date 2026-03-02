from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta

from app.config.database import get_db
from app.models import Team, TeamMember, TeamInvite, Comment, ApprovalWorkflow, ActivityLog, User, TeamRole, InviteStatus
from app.auth.dependencies import get_current_user

router = APIRouter()

# Request/Response Schemas
class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TeamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime
    member_count: int
    
    class Config:
        from_attributes = True

class InviteCreate(BaseModel):
    email: EmailStr
    role: TeamRole = TeamRole.VIEWER

class InviteResponse(BaseModel):
    id: int
    team_id: int
    email: str
    role: TeamRole
    status: InviteStatus
    invited_at: datetime
    expires_at: datetime
    
    class Config:
        from_attributes = True

class MemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    role: TeamRole
    joined_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    text: str
    content_id: Optional[int] = None
    post_id: Optional[int] = None
    campaign_id: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    user_id: int
    username: str
    text: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ApprovalRequest(BaseModel):
    approver_id: int
    content_id: Optional[int] = None
    post_id: Optional[int] = None
    campaign_id: Optional[int] = None

class ApprovalResponse(BaseModel):
    id: int
    status: str
    requested_by: int
    approver_id: int
    requested_at: datetime
    reviewed_at: Optional[datetime]
    notes: Optional[str]
    
    class Config:
        from_attributes = True

class ActivityResponse(BaseModel):
    id: int
    user_id: int
    username: str
    action: str
    resource_type: str
    resource_id: int
    details: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Team Management Endpoints

@router.post("/", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new team.
    """
    new_team = Team(
        name=team.name,
        description=team.description,
        owner_id=current_user.id
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    # Add owner as admin member
    owner_member = TeamMember(
        team_id=new_team.id,
        user_id=current_user.id,
        role=TeamRole.OWNER
    )
    db.add(owner_member)
    db.commit()
    
    # Log activity
    log_activity(db, new_team.id, current_user.id, "created", "team", new_team.id, f"Created team '{team.name}'")
    
    return {
        **new_team.__dict__,
        "member_count": 1
    }


@router.get("/user", response_model=List[TeamResponse])
async def get_user_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all teams a user is part of.
    """
    # Get teams where user is a member
    memberships = db.query(TeamMember).filter(TeamMember.user_id == current_user.id).all()
    team_ids = [m.team_id for m in memberships]
    
    teams = db.query(Team).filter(Team.id.in_(team_ids)).all()
    
    result = []
    for team in teams:
        member_count = db.query(TeamMember).filter(TeamMember.team_id == team.id).count()
        result.append({
            **team.__dict__,
            "member_count": member_count
        })
    
    return result


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: Session = Depends(get_db)):
    """
    Get team details.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    member_count = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()
    
    return {
        **team.__dict__,
        "member_count": member_count
    }


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update team details (owner/admin only).
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check permissions
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not member or member.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    if team_update.name:
        team.name = team_update.name
    if team_update.description is not None:
        team.description = team_update.description
    
    team.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(team)
    
    log_activity(db, team_id, current_user.id, "updated", "team", team_id, "Updated team details")
    
    member_count = db.query(TeamMember).filter(TeamMember.team_id == team_id).count()
    
    return {
        **team.__dict__,
        "member_count": member_count
    }


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a team (owner only).
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if team.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only team owner can delete the team")
    
    db.delete(team)
    db.commit()
    
    return {"status": "success", "message": "Team deleted successfully"}


# Team Member Management

@router.get("/{team_id}/members", response_model=List[MemberResponse])
async def get_team_members(team_id: int, db: Session = Depends(get_db)):
    """
    Get all members of a team.
    
    PERFORMANCE: Uses eager loading to prevent N+1 queries
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # ✅ OPTIMIZED: Single query with JOIN instead of N+1
    members = db.query(TeamMember)\
        .options(joinedload(TeamMember.user))\
        .filter(TeamMember.team_id == team_id)\
        .all()
    
    result = []
    for member in members:
        if member.user:  # User already loaded via joinedload
            result.append({
                "id": member.id,
                "user_id": member.user.id,
                "username": member.user.username,
                "email": member.user.email,
                "role": member.role,
                "joined_at": member.joined_at
            })
    
    return result


@router.put("/{team_id}/members/{member_id}/role")
async def update_member_role(
    team_id: int,
    member_id: int,
    new_role: TeamRole,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a team member's role (owner/admin only).
    
    SECURITY:
    - Requires authentication
    - Only owner/admin can update roles
    """
    # Check permissions
    requester = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not requester or requester.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Can't change owner role
    if member.role == TeamRole.OWNER:
        raise HTTPException(status_code=400, detail="Cannot change owner role")
    
    member.role = new_role
    db.commit()
    
    log_activity(db, team_id, current_user.id, "updated", "member", member_id, f"Changed role to {new_role}")
    
    return {"status": "success", "new_role": new_role}


@router.delete("/{team_id}/members/{member_id}")
async def remove_team_member(
    team_id: int, 
    member_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a member from the team (owner/admin only).
    
    SECURITY:
    - Requires authentication
    - Only owner/admin can remove members
    """
    # Check permissions
    requester = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not requester or requester.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    member = db.query(TeamMember).filter(TeamMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Can't remove owner
    if member.role == TeamRole.OWNER:
        raise HTTPException(status_code=400, detail="Cannot remove team owner")
    
    db.delete(member)
    db.commit()
    
    log_activity(db, team_id, current_user.id, "removed", "member", member_id, "Removed team member")
    
    return {"status": "success", "message": "Member removed successfully"}


# Helper function for activity logging
def log_activity(db: Session, team_id: int, user_id: int, action: str, resource_type: str, resource_id: int, details: str = None):
    """
    Log team activity.
    """
    activity = ActivityLog(
        team_id=team_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details
    )
    db.add(activity)
    db.commit()



# Team Invites

@router.post("/{team_id}/invites", response_model=InviteResponse)
async def invite_member(
    team_id: int, 
    invite: InviteCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Invite a new member to the team.
    
    SECURITY:
    - Requires authentication
    - Only owner/admin can invite members
    """
    # Check permissions
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not member or member.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Check if user already invited or member
    existing_invite = db.query(TeamInvite).filter(
        TeamInvite.team_id == team_id,
        TeamInvite.email == invite.email,
        TeamInvite.status == InviteStatus.PENDING
    ).first()
    
    if existing_invite:
        raise HTTPException(status_code=400, detail="User already invited")
    
    # Create invite
    new_invite = TeamInvite(
        team_id=team_id,
        email=invite.email,
        role=invite.role,
        invited_by=current_user.id,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(new_invite)
    db.commit()
    db.refresh(new_invite)
    
    log_activity(db, team_id, current_user.id, "invited", "member", new_invite.id, f"Invited {invite.email}")
    
    return new_invite


@router.get("/{team_id}/invites", response_model=List[InviteResponse])
async def get_team_invites(team_id: int, db: Session = Depends(get_db)):
    """
    Get all pending invites for a team.
    """
    invites = db.query(TeamInvite).filter(
        TeamInvite.team_id == team_id,
        TeamInvite.status == InviteStatus.PENDING
    ).all()
    
    return invites


@router.post("/invites/{invite_id}/accept")
async def accept_invite(
    invite_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accept a team invite.
    
    SECURITY:
    - Requires authentication
    - User can only accept invites sent to their email
    """
    invite = db.query(TeamInvite).filter(TeamInvite.id == invite_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    # Verify invite is for current user's email
    if invite.email.lower() != current_user.email.lower():
        raise HTTPException(status_code=403, detail="This invite is not for you")
    
    if invite.status != InviteStatus.PENDING:
        raise HTTPException(status_code=400, detail="Invite already processed")
    
    if invite.expires_at < datetime.utcnow():
        invite.status = InviteStatus.EXPIRED
        db.commit()
        raise HTTPException(status_code=400, detail="Invite expired")
    
    # Check if already a member
    existing_member = db.query(TeamMember).filter(
        TeamMember.team_id == invite.team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a team member")
    
    # Add as member
    new_member = TeamMember(
        team_id=invite.team_id,
        user_id=current_user.id,
        role=invite.role
    )
    db.add(new_member)
    
    # Update invite status
    invite.status = InviteStatus.ACCEPTED
    invite.accepted_at = datetime.utcnow()
    
    db.commit()
    
    log_activity(db, invite.team_id, current_user.id, "joined", "team", invite.team_id, "Accepted invite and joined team")
    
    return {"status": "success", "message": "Invite accepted"}


@router.post("/invites/{invite_id}/decline")
async def decline_invite(invite_id: int, db: Session = Depends(get_db)):
    """
    Decline a team invite.
    """
    invite = db.query(TeamInvite).filter(TeamInvite.id == invite_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invite not found")
    
    if invite.status != InviteStatus.PENDING:
        raise HTTPException(status_code=400, detail="Invite already processed")
    
    invite.status = InviteStatus.DECLINED
    db.commit()
    
    return {"status": "success", "message": "Invite declined"}


# Comments

@router.post("/{team_id}/comments", response_model=CommentResponse)
async def add_comment(
    team_id: int, 
    comment: CommentCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a comment to content/post/campaign.
    
    SECURITY:
    - Requires authentication
    - User must be team member
    """
    # Verify user is team member
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="Not a team member")
    
    new_comment = Comment(
        content_id=comment.content_id,
        post_id=comment.post_id,
        campaign_id=comment.campaign_id,
        user_id=current_user.id,
        text=comment.text
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Log activity
    resource_type = "content" if comment.content_id else "post" if comment.post_id else "campaign"
    resource_id = comment.content_id or comment.post_id or comment.campaign_id
    log_activity(db, team_id, current_user.id, "commented", resource_type, resource_id, comment.text[:50])
    
    return {
        "id": new_comment.id,
        "user_id": current_user.id,
        "username": current_user.username,
        "text": new_comment.text,
        "created_at": new_comment.created_at
    }


@router.get("/comments/{resource_type}/{resource_id}", response_model=List[CommentResponse])
async def get_comments(resource_type: str, resource_id: int, db: Session = Depends(get_db)):
    """
    Get all comments for a resource.
    
    PERFORMANCE: Uses eager loading to prevent N+1 queries
    """
    # ✅ OPTIMIZED: Single query with JOIN
    query = db.query(Comment).options(joinedload(Comment.user))
    
    if resource_type == "content":
        comments = query.filter(Comment.content_id == resource_id).all()
    elif resource_type == "post":
        comments = query.filter(Comment.post_id == resource_id).all()
    elif resource_type == "campaign":
        comments = query.filter(Comment.campaign_id == resource_id).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid resource type")
    
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "user_id": comment.user_id,
            "username": comment.user.username if comment.user else "Unknown",
            "text": comment.text,
            "created_at": comment.created_at
        })
    
    return result


# Approval Workflows

@router.post("/{team_id}/approvals", response_model=ApprovalResponse)
async def request_approval(
    team_id: int, 
    approval: ApprovalRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request approval for content/post/campaign.
    
    SECURITY:
    - Requires authentication
    - User must be team member
    """
    # Verify user is team member
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not member:
        raise HTTPException(status_code=403, detail="Not a team member")
    
    # Verify approver is admin or owner
    approver = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == approval.approver_id
    ).first()
    
    if not approver or approver.role not in [TeamRole.OWNER, TeamRole.ADMIN]:
        raise HTTPException(status_code=400, detail="Approver must be admin or owner")
    
    new_approval = ApprovalWorkflow(
        content_id=approval.content_id,
        post_id=approval.post_id,
        campaign_id=approval.campaign_id,
        requested_by=current_user.id,
        approver_id=approval.approver_id
    )
    db.add(new_approval)
    db.commit()
    db.refresh(new_approval)
    
    # Log activity
    resource_type = "content" if approval.content_id else "post" if approval.post_id else "campaign"
    resource_id = approval.content_id or approval.post_id or approval.campaign_id
    log_activity(db, team_id, current_user.id, "requested_approval", resource_type, resource_id)
    
    return new_approval


@router.put("/approvals/{approval_id}/review")
async def review_approval(
    approval_id: int,
    status: str,
    notes: Optional[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve or reject an approval request.
    
    SECURITY:
    - Requires authentication
    - Only assigned approver can review
    """
    approval = db.query(ApprovalWorkflow).filter(ApprovalWorkflow.id == approval_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    if approval.approver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only assigned approver can review")
    
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")
    
    approval.status = status
    approval.notes = notes
    approval.reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(approval)
    
    return approval


@router.get("/{team_id}/approvals/pending", response_model=List[ApprovalResponse])
async def get_pending_approvals(
    team_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all pending approval requests for authenticated user.
    
    SECURITY:
    - Requires authentication
    - User can only see approvals assigned to them
    """
    approvals = db.query(ApprovalWorkflow).filter(
        ApprovalWorkflow.approver_id == current_user.id,
        ApprovalWorkflow.status == "pending"
    ).all()
    
    return approvals


# Activity Feed

@router.get("/{team_id}/activity", response_model=List[ActivityResponse])
async def get_team_activity(team_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get recent activity for a team.
    
    PERFORMANCE: Uses eager loading to prevent N+1 queries
    """
    # ✅ OPTIMIZED: Single query with JOIN
    activities = db.query(ActivityLog)\
        .options(joinedload(ActivityLog.user))\
        .filter(ActivityLog.team_id == team_id)\
        .order_by(ActivityLog.created_at.desc())\
        .limit(limit)\
        .all()
    
    result = []
    for activity in activities:
        result.append({
            "id": activity.id,
            "user_id": activity.user_id,
            "username": activity.user.username if activity.user else "Unknown",
            "action": activity.action,
            "resource_type": activity.resource_type,
            "resource_id": activity.resource_id,
            "details": activity.details,
            "created_at": activity.created_at
        })
    
    return result
