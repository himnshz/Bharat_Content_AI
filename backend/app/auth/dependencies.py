"""
Authentication and Authorization Dependencies
Secure JWT-based authentication with role-based access control
"""
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

from app.config.database import get_db
from app.models.user import User, UserRole

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE-THIS-IN-PRODUCTION-USE-STRONG-SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token with expiration
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token with longer expiration
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Check expiration (automatically handled by jwt.decode)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return payload
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id: int = payload.get("sub")
    
    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (additional check)
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def require_role(allowed_roles: list[UserRole]):
    """
    Dependency to check if user has required role
    
    Usage:
        @router.post("/admin-only")
        async def admin_route(
            current_user: User = Depends(require_role([UserRole.BUSINESS, UserRole.STARTUP]))
        ):
            return {"message": "Admin access granted"}
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    
    return role_checker


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get user if token provided, otherwise return None
    Useful for endpoints that work with or without authentication
    """
    if not authorization:
        return None
    
    try:
        # Extract token from "Bearer <token>"
        if not authorization.startswith("Bearer "):
            return None
        
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        
        user = db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None
    
    except:
        return None


# Rate limiting helper
def check_rate_limit(user: User, operation: str, limit: int, window_seconds: int = 60):
    """
    Check if user has exceeded rate limit for operation
    
    TODO: Implement with Redis for production
    """
    # Placeholder - implement with Redis in production
    pass


# Quota checking helper
def check_user_quota(user: User, operation: str) -> bool:
    """
    Check if user has remaining quota for operation
    """
    from app.models.user import SubscriptionTier
    
    # Define quota limits per tier
    QUOTA_LIMITS = {
        SubscriptionTier.FREE: {
            "content_generation": 100,
            "translations": 50,
            "posts_scheduled": 20
        },
        SubscriptionTier.BASIC: {
            "content_generation": 1000,
            "translations": 500,
            "posts_scheduled": 200
        },
        SubscriptionTier.PRO: {
            "content_generation": 10000,
            "translations": 5000,
            "posts_scheduled": 2000
        },
        SubscriptionTier.ENTERPRISE: {
            "content_generation": -1,  # Unlimited
            "translations": -1,
            "posts_scheduled": -1
        }
    }
    
    tier_limits = QUOTA_LIMITS.get(user.subscription_tier, QUOTA_LIMITS[SubscriptionTier.FREE])
    limit = tier_limits.get(operation, 0)
    
    # -1 means unlimited
    if limit == -1:
        return True
    
    # Check current usage
    if operation == "content_generation":
        return user.content_generated_count < limit
    elif operation == "translations":
        return user.translations_count < limit
    elif operation == "posts_scheduled":
        return user.posts_scheduled_count < limit
    
    return False


def enforce_quota(operation: str):
    """
    Dependency to enforce quota limits
    
    Usage:
        @router.post("/generate")
        async def generate(
            current_user: User = Depends(enforce_quota("content_generation"))
        ):
            # User has quota available
    """
    async def quota_checker(current_user: User = Depends(get_current_user)) -> User:
        if not check_user_quota(current_user, operation):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Monthly quota exceeded for {operation}. Please upgrade your subscription."
            )
        return current_user
    
    return quota_checker
