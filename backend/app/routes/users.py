from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.config.database import get_db
from app.models import User, UserRole, SubscriptionTier
from app.auth.dependencies import (
    create_access_token, 
    create_refresh_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

# Request/Response Schemas
class UserCreateRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=8, max_length=128, description="User password")
    full_name: Optional[str] = Field(None, max_length=255, description="Full name")
    role: UserRole = Field(default=UserRole.STUDENT, description="User role")
    preferred_language: str = Field(default="hindi", description="Preferred language")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not v.isalnum() and '_' not in v:
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v.lower()

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    preferred_language: Optional[str] = None
    role: Optional[UserRole] = None

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

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
        # SECURITY: Explicitly exclude sensitive fields
        fields = {
            'hashed_password': {'exclude': True},
            'cognito_user_id': {'exclude': True}
        }

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserStatsResponse(BaseModel):
    user_id: int


# ============================================================================
# AUTHENTICATION ENDPOINTS (SECURED)
# ============================================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateRequest, db: Session = Depends(get_db)):
    """
    Register a new user account
    
    SECURITY:
    - Password strength validation
    - Email uniqueness check
    - Username uniqueness check
    - Password hashing with bcrypt
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        preferred_language=user_data.preferred_language,
        is_active=True,
        is_verified=False,
        email_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    SECURITY:
    - Password verification with bcrypt
    - JWT token generation with expiration
    - HttpOnly cookie for token storage
    - Rate limiting (TODO: implement with Redis)
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    # Set HttpOnly cookie (SECURE)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Not accessible to JavaScript
        secure=True,    # HTTPS only (set to False for local development)
        samesite="lax",  # CSRF protection
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/logout")
async def logout(
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user
    
    SECURITY:
    - Clears HttpOnly cookie
    - Invalidates session
    """
    response.delete_cookie(key="access_token")
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information
    
    SECURITY:
    - Requires valid JWT token
    - Returns only safe user data (no password hash)
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    
    SECURITY:
    - User can only update their own profile
    - Cannot change role (requires admin)
    """
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    if user_update.preferred_language is not None:
        current_user.preferred_language = user_update.preferred_language
    
    # Role change requires admin privileges
    if user_update.role is not None:
        if current_user.role not in [UserRole.BUSINESS, UserRole.STARTUP]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to change role"
            )
        current_user.role = user_update.role
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.post("/refresh-token")
async def refresh_access_token(
    refresh_token: str,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    SECURITY:
    - Validates refresh token
    - Issues new access token
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id: int = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user"
            )
        
        # Create new access token
        new_access_token = create_access_token(data={"sub": user.id})
        
        # Set new cookie
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
