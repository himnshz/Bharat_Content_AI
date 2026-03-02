"""
Monitoring and Health Check Routes
Provides visibility into rate limits, circuit breakers, and service health
"""
from fastapi import APIRouter, Request, Depends
from typing import Dict, Any
from app.config.circuit_breaker_config import get_all_circuit_status, get_circuit_breaker_manager
from app.services.content_generation.ai_service_manager_v2 import (
    get_enhanced_ai_service_manager,
    get_service_health,
    get_ai_statistics
)
from app.config.rate_limit_config import get_user_tier_from_request, RateLimitTier
from app.config.redis_config import get_async_redis
import redis.asyncio as aioredis

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint
    
    Returns status of all system components
    """
    try:
        # Check Redis connection
        redis_client = await get_async_redis()
        await redis_client.ping()
        redis_healthy = True
    except Exception as e:
        redis_healthy = False
    
    # Check AI services
    try:
        service_health = get_service_health()
        ai_services_healthy = any(
            service["is_healthy"] 
            for service in service_health.values() 
            if service.get("available", False)
        )
    except Exception:
        ai_services_healthy = False
        service_health = {}
    
    # Overall health
    overall_healthy = redis_healthy and ai_services_healthy
    
    return {
        "status": "healthy" if overall_healthy else "degraded",
        "timestamp": "2024-01-01T00:00:00Z",
        "components": {
            "redis": {
                "status": "healthy" if redis_healthy else "unhealthy",
                "message": "Redis connection active" if redis_healthy else "Redis connection failed"
            },
            "ai_services": {
                "status": "healthy" if ai_services_healthy else "unhealthy",
                "available_services": len([
                    s for s in service_health.values() 
                    if s.get("is_healthy", False)
                ]),
                "total_services": len(service_health)
            }
        }
    }


@router.get("/circuit-breakers")
async def get_circuit_breakers_status():
    """
    Get status of all circuit breakers
    
    Shows which external services are available or circuit-broken
    """
    return {
        "circuit_breakers": get_all_circuit_status(),
        "summary": {
            "total": len(get_all_circuit_status()),
            "open": len([
                cb for cb in get_all_circuit_status().values() 
                if cb["state"] == "open"
            ]),
            "closed": len([
                cb for cb in get_all_circuit_status().values() 
                if cb["state"] == "closed"
            ]),
            "half_open": len([
                cb for cb in get_all_circuit_status().values() 
                if cb["state"] == "half_open"
            ])
        }
    }


@router.post("/circuit-breakers/{service_name}/reset")
async def reset_circuit_breaker(service_name: str):
    """
    Manually reset a circuit breaker
    
    Useful for forcing a retry after fixing external service issues
    """
    try:
        manager = get_circuit_breaker_manager()
        manager.reset_circuit_breaker(service_name)
        return {
            "message": f"Circuit breaker for {service_name} has been reset",
            "service": service_name,
            "status": "reset"
        }
    except Exception as e:
        return {
            "error": f"Failed to reset circuit breaker: {str(e)}",
            "service": service_name,
            "status": "error"
        }


@router.post("/circuit-breakers/reset-all")
async def reset_all_circuit_breakers():
    """
    Reset all circuit breakers
    
    Use with caution - only when you're sure all services are back online
    """
    try:
        manager = get_circuit_breaker_manager()
        manager.reset_all_circuit_breakers()
        return {
            "message": "All circuit breakers have been reset",
            "status": "reset"
        }
    except Exception as e:
        return {
            "error": f"Failed to reset circuit breakers: {str(e)}",
            "status": "error"
        }


@router.get("/ai-services/health")
async def get_ai_services_health():
    """
    Get health status of all AI services
    
    Shows which AI providers are available and their circuit breaker status
    """
    return {
        "services": get_service_health(),
        "summary": {
            "total_available": len([
                s for s in get_service_health().values() 
                if s.get("available", False)
            ]),
            "total_healthy": len([
                s for s in get_service_health().values() 
                if s.get("is_healthy", False)
            ])
        }
    }


@router.get("/ai-services/statistics")
async def get_ai_services_statistics():
    """
    Get usage statistics for AI services
    
    Shows request counts, success rates, and fallback usage
    """
    return get_ai_statistics()


@router.post("/ai-services/statistics/reset")
async def reset_ai_statistics():
    """Reset AI service statistics"""
    try:
        manager = get_enhanced_ai_service_manager()
        manager.reset_statistics()
        return {
            "message": "AI service statistics have been reset",
            "status": "reset"
        }
    except Exception as e:
        return {
            "error": f"Failed to reset statistics: {str(e)}",
            "status": "error"
        }


@router.get("/rate-limits/my-limits")
async def get_my_rate_limits(request: Request):
    """
    Get rate limits for current user
    
    Shows what rate limits apply based on subscription tier
    """
    tier = get_user_tier_from_request(request)
    
    tier_config = {
        "UNAUTHENTICATED": RateLimitTier.UNAUTHENTICATED,
        "FREE": RateLimitTier.FREE,
        "BASIC": RateLimitTier.BASIC,
        "PRO": RateLimitTier.PRO,
        "ENTERPRISE": RateLimitTier.ENTERPRISE,
    }.get(tier, RateLimitTier.UNAUTHENTICATED)
    
    return {
        "tier": tier,
        "limits": tier_config,
        "message": f"You are on the {tier} tier"
    }


@router.get("/rate-limits/tiers")
async def get_all_rate_limit_tiers():
    """
    Get all available rate limit tiers
    
    Shows what limits apply to each subscription tier
    """
    return {
        "tiers": {
            "UNAUTHENTICATED": RateLimitTier.UNAUTHENTICATED,
            "FREE": RateLimitTier.FREE,
            "BASIC": RateLimitTier.BASIC,
            "PRO": RateLimitTier.PRO,
            "ENTERPRISE": RateLimitTier.ENTERPRISE,
        },
        "description": {
            "UNAUTHENTICATED": "No authentication - most restrictive",
            "FREE": "Free tier - basic limits",
            "BASIC": "Basic subscription - moderate limits",
            "PRO": "Pro subscription - high limits",
            "ENTERPRISE": "Enterprise subscription - very high limits"
        }
    }


@router.get("/system/status")
async def get_system_status():
    """
    Comprehensive system status
    
    Combines health, circuit breakers, AI services, and rate limits
    """
    # Get all status information
    health = await health_check()
    circuit_breakers = await get_circuit_breakers_status()
    ai_health = await get_ai_services_health()
    ai_stats = await get_ai_services_statistics()
    
    return {
        "overall_status": health["status"],
        "timestamp": health["timestamp"],
        "health": health,
        "circuit_breakers": circuit_breakers["summary"],
        "ai_services": {
            "health": ai_health["summary"],
            "statistics": ai_stats
        },
        "rate_limiting": {
            "enabled": True,
            "backend": "Redis"
        }
    }
