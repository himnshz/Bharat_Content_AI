from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext

from app.config.database import get_db
from app.models import User, UserRole, SubscriptionTier

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request/Response Schemas
class UserCreateRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    role: UserRole = Field(default=UserRole.STUDENT, description="User role")
    preferred_language: str = Field(default="hindi", description="Preferred language")

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    preferred_language: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: UserRole
    subscription_tier: SubscriptionTier
    preferred_language: str
    is_active: bool
    is_verified: bool
    email_verified: bool
    content_generated_count: int
    translations_count: int
    posts_scheduled_count: int
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserStatsResponse(BaseModel):
    user_id: int
    username: str
    total_content: int
    total_translations: int
    total_posts: int
    total_published: int
    account_age_days: int
    subscription_tier: SubscriptionTier


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Register a new user account.
    """
    try:
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create new user
        user = User(
            email=request.email,
            username=request.username,
            hashed_password=hash_password(request.password),
            full_name=request.full_name,
            role=request.role,
            preferred_language=request.preferred_language,
            subscription_tier=SubscriptionTier.FREE,
            is_active=True,
            is_verified=False,
            email_verified=False
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user profile by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get user profile by username.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, request: UserUpdateRequest, db: Session = Depends(get_db)):
    """
    Update user profile information.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.full_name is not None:
        user.full_name = request.full_name
    if request.preferred_language is not None:
        user.preferred_language = request.preferred_language
    if request.role is not None:
        user.role = request.role
    
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive statistics for a user.
    """
    from app.models import Content, Post, PostStatus
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Count content
    total_content = db.query(Content).filter(Content.user_id == user_id).count()
    
    # Count posts
    total_posts = db.query(Post).filter(Post.user_id == user_id).count()
    total_published = db.query(Post).filter(
        Post.user_id == user_id,
        Post.status == PostStatus.PUBLISHED
    ).count()
    
    # Calculate account age
    account_age = (datetime.utcnow() - user.created_at).days
    
    return UserStatsResponse(
        user_id=user.id,
        username=user.username,
        total_content=total_content,
        total_translations=user.translations_count,
        total_posts=total_posts,
        total_published=total_published,
        account_age_days=account_age,
        subscription_tier=user.subscription_tier
    )


@router.post("/{user_id}/upgrade-subscription")
async def upgrade_subscription(
    user_id: int,
    tier: SubscriptionTier,
    db: Session = Depends(get_db)
):
    """
    Upgrade user subscription tier.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate upgrade path
    tier_order = {
        SubscriptionTier.FREE: 0,
        SubscriptionTier.BASIC: 1,
        SubscriptionTier.PRO: 2,
        SubscriptionTier.ENTERPRISE: 3
    }
    
    if tier_order[tier] <= tier_order[user.subscription_tier]:
        raise HTTPException(status_code=400, detail="Cannot downgrade or maintain same tier")
    
    user.subscription_tier = tier
    user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "user_id": user.id,
        "new_tier": user.subscription_tier.value,
        "message": f"Successfully upgraded to {tier.value} tier"
    }


@router.post("/{user_id}/verify-email")
async def verify_email(user_id: int, db: Session = Depends(get_db)):
    """
    Mark user email as verified.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.email_verified:
        return {"status": "already_verified", "message": "Email already verified"}
    
    user.email_verified = True
    user.is_verified = True
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Email verified successfully"
    }


@router.post("/{user_id}/login")
async def record_login(user_id: int, db: Session = Depends(get_db)):
    """
    Record user login timestamp.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "status": "success",
        "last_login": user.last_login
    }


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user account (soft delete by deactivating).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Soft delete - just deactivate
    user.is_active = False
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return None
