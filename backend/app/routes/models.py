from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from app.config.database import get_db
from app.models import AIModelConfig, User
from app.auth.dependencies import get_current_user

router = APIRouter()

# Response Schemas
class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    description: str
    capabilities: List[str]
    cost_per_1k_tokens: float
    max_tokens: int
    is_available: bool
    is_enabled: bool
    performance_rating: float
    speed_rating: float
    quality_rating: float

class ModelUsageStats(BaseModel):
    model_id: str
    model_name: str
    total_requests: int
    total_tokens: int
    total_cost: float
    success_rate: float
    avg_response_time_ms: float
    last_used: Optional[datetime]

class ModelConfigUpdate(BaseModel):
    is_enabled: bool
    is_primary: Optional[bool] = False

class ModelResponse(BaseModel):
    id: int
    user_id: int
    model_id: str
    model_name: str
    provider: str
    is_enabled: bool
    is_primary: bool
    api_key_configured: bool
    usage_count: int
    last_used: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# Available AI Models Configuration
AVAILABLE_MODELS = {
    "gemini-pro": {
        "name": "Gemini Pro",
        "provider": "Google",
        "description": "Google's most capable AI model for text generation",
        "capabilities": ["text", "multimodal", "long-context"],
        "cost_per_1k_tokens": 0.0005,
        "max_tokens": 32000,
        "performance_rating": 9.5,
        "speed_rating": 9.0,
        "quality_rating": 9.5
    },
    "gpt-4": {
        "name": "GPT-4",
        "provider": "OpenAI",
        "description": "OpenAI's most advanced language model",
        "capabilities": ["text", "reasoning", "code"],
        "cost_per_1k_tokens": 0.03,
        "max_tokens": 8192,
        "performance_rating": 9.8,
        "speed_rating": 7.0,
        "quality_rating": 9.8
    },
    "gpt-3.5-turbo": {
        "name": "GPT-3.5 Turbo",
        "provider": "OpenAI",
        "description": "Fast and cost-effective OpenAI model",
        "capabilities": ["text", "chat"],
        "cost_per_1k_tokens": 0.002,
        "max_tokens": 4096,
        "performance_rating": 8.5,
        "speed_rating": 9.5,
        "quality_rating": 8.5
    },
    "claude-3-opus": {
        "name": "Claude 3 Opus",
        "provider": "Anthropic",
        "description": "Anthropic's most powerful model",
        "capabilities": ["text", "reasoning", "analysis"],
        "cost_per_1k_tokens": 0.015,
        "max_tokens": 200000,
        "performance_rating": 9.7,
        "speed_rating": 8.0,
        "quality_rating": 9.7
    },
    "claude-3-sonnet": {
        "name": "Claude 3 Sonnet",
        "provider": "Anthropic",
        "description": "Balanced performance and speed",
        "capabilities": ["text", "chat"],
        "cost_per_1k_tokens": 0.003,
        "max_tokens": 200000,
        "performance_rating": 9.0,
        "speed_rating": 9.0,
        "quality_rating": 9.0
    },
    "cohere-command": {
        "name": "Command",
        "provider": "Cohere",
        "description": "Cohere's flagship model for generation",
        "capabilities": ["text", "multilingual"],
        "cost_per_1k_tokens": 0.001,
        "max_tokens": 4096,
        "performance_rating": 8.0,
        "speed_rating": 8.5,
        "quality_rating": 8.0
    },
    "bedrock-titan": {
        "name": "Titan Text",
        "provider": "AWS Bedrock",
        "description": "Amazon's foundation model",
        "capabilities": ["text", "summarization"],
        "cost_per_1k_tokens": 0.0008,
        "max_tokens": 8192,
        "performance_rating": 7.5,
        "speed_rating": 8.0,
        "quality_rating": 7.5
    },
    "llama-2-70b": {
        "name": "Llama 2 70B",
        "provider": "Meta (via Together AI)",
        "description": "Open-source large language model",
        "capabilities": ["text", "chat"],
        "cost_per_1k_tokens": 0.0009,
        "max_tokens": 4096,
        "performance_rating": 8.0,
        "speed_rating": 7.5,
        "quality_rating": 8.0
    }
}


@router.get("/available", response_model=List[ModelInfo])
async def get_available_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of all available AI models with their configurations.
    """
    # Get user's model configurations
    user_configs = db.query(AIModelConfig).filter(AIModelConfig.user_id == current_user.id).all()
    config_map = {config.model_id: config for config in user_configs}
    
    models = []
    for model_id, model_data in AVAILABLE_MODELS.items():
        user_config = config_map.get(model_id)
        
        models.append(ModelInfo(
            id=model_id,
            name=model_data["name"],
            provider=model_data["provider"],
            description=model_data["description"],
            capabilities=model_data["capabilities"],
            cost_per_1k_tokens=model_data["cost_per_1k_tokens"],
            max_tokens=model_data["max_tokens"],
            is_available=True,
            is_enabled=user_config.is_enabled if user_config else False,
            performance_rating=model_data["performance_rating"],
            speed_rating=model_data["speed_rating"],
            quality_rating=model_data["quality_rating"]
        ))
    
    return models


@router.get("/user", response_model=List[ModelResponse])
async def get_user_models(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's configured AI models.
    """
    configs = db.query(AIModelConfig).filter(AIModelConfig.user_id == current_user.id).all()
    return configs


@router.post("/configure/{model_id}")
async def configure_model(
    model_id: str,
    config: ModelConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enable/disable a model for a user or set it as primary.
    """
    if model_id not in AVAILABLE_MODELS:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get or create model config
    model_config = db.query(AIModelConfig).filter(
        AIModelConfig.user_id == current_user.id,
        AIModelConfig.model_id == model_id
    ).first()
    
    if not model_config:
        model_data = AVAILABLE_MODELS[model_id]
        model_config = AIModelConfig(
            user_id=current_user.id,
            model_id=model_id,
            model_name=model_data["name"],
            provider=model_data["provider"],
            is_enabled=config.is_enabled,
            is_primary=config.is_primary or False,
            api_key_configured=False,
            usage_count=0
        )
        db.add(model_config)
    else:
        model_config.is_enabled = config.is_enabled
        if config.is_primary is not None:
            model_config.is_primary = config.is_primary
    
    # If setting as primary, unset other primary models
    if config.is_primary:
        db.query(AIModelConfig).filter(
            AIModelConfig.user_id == current_user.id,
            AIModelConfig.model_id != model_id
        ).update({"is_primary": False})
    
    db.commit()
    db.refresh(model_config)
    
    return {
        "status": "success",
        "model_id": model_id,
        "is_enabled": model_config.is_enabled,
        "is_primary": model_config.is_primary
    }


@router.get("/usage", response_model=List[ModelUsageStats])
async def get_model_usage_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get usage statistics for all models used by the user.
    """
    configs = db.query(AIModelConfig).filter(AIModelConfig.user_id == current_user.id).all()
    
    stats = []
    for config in configs:
        # Calculate success rate (simplified - in production, track actual failures)
        success_rate = 98.5 if config.usage_count > 0 else 0.0
        
        # Estimate tokens and cost (simplified)
        estimated_tokens = config.usage_count * 500  # avg 500 tokens per request
        model_data = AVAILABLE_MODELS.get(config.model_id, {})
        cost_per_1k = model_data.get("cost_per_1k_tokens", 0.001)
        estimated_cost = (estimated_tokens / 1000) * cost_per_1k
        
        stats.append(ModelUsageStats(
            model_id=config.model_id,
            model_name=config.model_name,
            total_requests=config.usage_count,
            total_tokens=estimated_tokens,
            total_cost=estimated_cost,
            success_rate=success_rate,
            avg_response_time_ms=1200.0,  # Simplified
            last_used=config.last_used
        ))
    
    return stats


@router.get("/primary")
async def get_primary_model(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the user's primary AI model.
    """
    primary = db.query(AIModelConfig).filter(
        AIModelConfig.user_id == current_user.id,
        AIModelConfig.is_primary == True
    ).first()
    
    if not primary:
        return {"model_id": None, "message": "No primary model set"}
    
    return {
        "model_id": primary.model_id,
        "model_name": primary.model_name,
        "provider": primary.provider
    }


@router.get("/comparison")
async def get_model_comparison():
    """
    Get comparison data for all available models.
    """
    comparison = []
    
    for model_id, model_data in AVAILABLE_MODELS.items():
        comparison.append({
            "model_id": model_id,
            "name": model_data["name"],
            "provider": model_data["provider"],
            "cost_per_1k_tokens": model_data["cost_per_1k_tokens"],
            "max_tokens": model_data["max_tokens"],
            "performance_rating": model_data["performance_rating"],
            "speed_rating": model_data["speed_rating"],
            "quality_rating": model_data["quality_rating"],
            "capabilities": model_data["capabilities"]
        })
    
    # Sort by performance rating
    comparison.sort(key=lambda x: x["performance_rating"], reverse=True)
    
    return {
        "models": comparison,
        "total_models": len(comparison)
    }


@router.post("/increment-usage/{model_id}")
async def increment_model_usage(
    model_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Increment usage count for a model (called internally when model is used).
    """
    config = db.query(AIModelConfig).filter(
        AIModelConfig.user_id == current_user.id,
        AIModelConfig.model_id == model_id
    ).first()
    
    if config:
        config.usage_count += 1
        config.last_used = datetime.utcnow()
        db.commit()
        
        return {"status": "success", "usage_count": config.usage_count}
    
    return {"status": "model_not_configured"}
