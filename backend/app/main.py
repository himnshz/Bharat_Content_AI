from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import content, translation, social, analytics, voice, users

app = FastAPI(
    title="Bharat Content AI API",
    description="Multilingual Smart Content Assistant for Indian Languages",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes
app.include_router(content.router, prefix="/api/content", tags=["Content Generation"])
app.include_router(translation.router, prefix="/api/translation", tags=["Translation"])
app.include_router(social.router, prefix="/api/social", tags=["Social Media"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(voice.router, prefix="/api/voice", tags=["Voice Input"])
app.include_router(users.router, prefix="/api/users", tags=["User Management"])

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
