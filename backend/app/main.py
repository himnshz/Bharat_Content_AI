from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import content, translation, social, analytics, voice, users, campaigns, models, teams, templates, bulk, monitoring
from app.config.redis_config import get_async_redis, close_async_redis
from app.config.rate_limit_config import limiter
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle (startup/shutdown)"""
    # Startup
    logger.info("🚀 Starting Bharat Content AI API...")
    logger.info("📦 Initializing Redis connection...")
    await get_async_redis()
    logger.info("✅ Redis connected")
    logger.info("🛡️  Rate limiting enabled")
    logger.info("⚡ Circuit breakers initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Bharat Content AI API...")
    logger.info("📦 Closing Redis connection...")
    await close_async_redis()
    logger.info("✅ Redis closed")

app = FastAPI(
    title="Bharat Content AI API",
    description="Multilingual Smart Content Assistant for Indian Languages with Rate Limiting and Circuit Breakers",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add rate limiter state
app.state.limiter = limiter

# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors"""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Please try again later.",
            "detail": str(exc.detail) if hasattr(exc, 'detail') else None
        },
        headers=exc.headers if hasattr(exc, 'headers') else {}
    )

# CORS middleware - SECURITY: Whitelist specific origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # SECURITY: Only allow specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"],
    expose_headers=["Content-Disposition"],
    max_age=600  # Cache preflight requests for 10 minutes
)

# Include routers with proper prefixes
app.include_router(content.router, prefix="/api/content", tags=["Content Generation"])
app.include_router(translation.router, prefix="/api/translation", tags=["Translation"])
app.include_router(social.router, prefix="/api/social", tags=["Social Media"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice Input"])
app.include_router(users.router, prefix="/api/users", tags=["User Management"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(models.router, prefix="/api/models", tags=["AI Models"])
app.include_router(teams.router, prefix="/api/teams", tags=["Team Collaboration"])
app.include_router(templates.router, prefix="/api/templates", tags=["Content Templates"])
app.include_router(bulk.router, prefix="/api/bulk", tags=["Bulk Operations"])
app.include_router(monitoring.router, prefix="/api/monitoring", tags=["Monitoring & Health"])

@app.get("/")
def read_root():
    return {
        "message": "Bharat Content AI API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security headers to all responses
    
    SECURITY:
    - X-Content-Type-Options: Prevent MIME sniffing
    - X-Frame-Options: Prevent clickjacking
    - X-XSS-Protection: Enable XSS filter
    - Strict-Transport-Security: Enforce HTTPS
    - Content-Security-Policy: Prevent XSS and injection attacks
    """
    response = await call_next(request)
    
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Only add HSTS in production
    if os.getenv("ENVIRONMENT") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"
    
    return response
