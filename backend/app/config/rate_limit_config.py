"""
Redis-backed Rate Limiting Configuration
Implements tier-based rate limits for API protection
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config.redis_config import get_sync_redis
from typing import Optional
from fastapi import Request
import os


# Rate limit tiers based on subscription
class RateLimitTier:
    """Rate limit configurations for different user tiers"""
    
    # Unauthenticated users (most restrictive)
    UNAUTHENTICATED = {
        "content_generation": "5/hour",      # 5 content generations per hour
        "translation": "10/hour",            # 10 translations per hour
        "bulk_operations": "1/day",          # 1 bulk operation per day
        "api_general": "100/hour",           # 100 general API calls per hour
        "social_posting": "5/hour",          # 5 social posts per hour
    }
    
    # Free tier (basic limits)
    FREE = {
        "content_generation": "20/hour",     # 20 content generations per hour
        "translation": "50/hour",            # 50 translations per hour
        "bulk_operations": "2/day",          # 2 bulk operations per day
        "api_general": "500/hour",           # 500 general API calls per hour
        "social_posting": "20/hour",         # 20 social posts per hour
    }
    
    # Basic tier (moderate limits)
    BASIC = {
        "content_generation": "100/hour",    # 100 content generations per hour
        "translation": "200/hour",           # 200 translations per hour
        "bulk_operations": "10/day",         # 10 bulk operations per day
        "api_general": "2000/hour",          # 2000 general API calls per hour
        "social_posting": "100/hour",        # 100 social posts per hour
    }
    
    # Pro tier (high limits)
    PRO = {
        "content_generation": "500/hour",    # 500 content generations per hour
        "translation": "1000/hour",          # 1000 translations per hour
        "bulk_operations": "50/day",         # 50 bulk operations per day
        "api_general": "10000/hour",         # 10000 general API calls per hour
        "social_posting": "500/hour",        # 500 social posts per hour
    }
    
    # Enterprise tier (very high limits)
    ENTERPRISE = {
        "content_generation": "5000/hour",   # 5000 content generations per hour
        "translation": "10000/hour",         # 10000 translations per hour
        "bulk_operations": "unlimited",      # Unlimited bulk operations
        "api_general": "100000/hour",        # 100000 general API calls per hour
        "social_posting": "5000/hour",       # 5000 social posts per hour
    }


def get_user_tier_from_request(request: Request) -> str:
    """
    Extract user tier from request
    
    Priority:
    1. Check JWT token for subscription_tier
    2. Check user session
    3. Default to unauthenticated
    """
    try:
        # Try to get from JWT token (if auth is implemented)
        if hasattr(request.state, "user"):
            user = request.state.user
            if hasattr(user, "subscription_tier"):
                return user.subscription_tier.upper()
        
        # Try to get from headers (for testing)
        tier_header = request.headers.get("X-User-Tier")
        if tier_header:
            return tier_header.upper()
        
        # Check if user is authenticated
        auth_header = request.headers.get("Authorization")
        if auth_header:
            # Default authenticated users to FREE tier
            return "FREE"
        
        # Unauthenticated
        return "UNAUTHENTICATED"
    
    except Exception:
        return "UNAUTHENTICATED"


def get_rate_limit_key(request: Request, operation_type: str = "api_general") -> str:
    """
    Generate rate limit key based on user tier and operation type
    
    Returns rate limit string like "100/hour" or "unlimited"
    """
    tier = get_user_tier_from_request(request)
    
    # Get tier configuration
    tier_config = {
        "UNAUTHENTICATED": RateLimitTier.UNAUTHENTICATED,
        "FREE": RateLimitTier.FREE,
        "BASIC": RateLimitTier.BASIC,
        "PRO": RateLimitTier.PRO,
        "ENTERPRISE": RateLimitTier.ENTERPRISE,
    }.get(tier, RateLimitTier.UNAUTHENTICATED)
    
    # Get rate limit for operation type
    rate_limit = tier_config.get(operation_type, tier_config["api_general"])
    
    return rate_limit


def get_identifier(request: Request) -> str:
    """
    Get unique identifier for rate limiting
    
    Priority:
    1. User ID (if authenticated)
    2. API Key (if provided)
    3. IP Address (fallback)
    """
    try:
        # Try to get user ID from JWT
        if hasattr(request.state, "user"):
            user = request.state.user
            if hasattr(user, "id"):
                return f"user:{user.id}"
        
        # Try to get API key from headers
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"apikey:{api_key[:16]}"  # Use first 16 chars
        
        # Fallback to IP address
        return get_remote_address(request)
    
    except Exception:
        return get_remote_address(request)


# Initialize Redis-backed limiter
def get_redis_storage():
    """Get Redis storage for rate limiting"""
    try:
        redis_client = get_sync_redis()
        return redis_client
    except Exception as e:
        print(f"Warning: Redis not available for rate limiting: {e}")
        return None


# Create limiter instance
limiter = Limiter(
    key_func=get_identifier,
    storage_uri=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    default_limits=["1000/hour"],  # Default limit for all routes
    headers_enabled=True,  # Add rate limit headers to responses
)


# Custom rate limit decorators for different operations
def rate_limit_content_generation(request: Request):
    """Rate limit for content generation endpoints"""
    return get_rate_limit_key(request, "content_generation")


def rate_limit_translation(request: Request):
    """Rate limit for translation endpoints"""
    return get_rate_limit_key(request, "translation")


def rate_limit_bulk_operations(request: Request):
    """Rate limit for bulk operations"""
    return get_rate_limit_key(request, "bulk_operations")


def rate_limit_social_posting(request: Request):
    """Rate limit for social media posting"""
    return get_rate_limit_key(request, "social_posting")


def rate_limit_api_general(request: Request):
    """Rate limit for general API calls"""
    return get_rate_limit_key(request, "api_general")


# Rate limit bypass for internal services
def is_internal_request(request: Request) -> bool:
    """Check if request is from internal service (Celery worker, etc.)"""
    internal_token = request.headers.get("X-Internal-Token")
    expected_token = os.getenv("INTERNAL_SERVICE_TOKEN", "")
    
    if internal_token and expected_token and internal_token == expected_token:
        return True
    
    # Check if request is from localhost (for development)
    remote_addr = get_remote_address(request)
    if remote_addr in ["127.0.0.1", "localhost", "::1"]:
        return True
    
    return False
