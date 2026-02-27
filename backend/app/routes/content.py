from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class ContentRequest(BaseModel):
    prompt: str
    language: str = "hindi"
    tone: str = "casual"
    content_type: str = "social_post"

class ContentResponse(BaseModel):
    content: str
    language: str
    model_used: str
    generation_time_ms: int

@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate content using Google Gemini or AWS Bedrock"""
    
    # Check which service to use
    use_gemini = os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_api_key_here'
    
    try:
        if use_gemini:
            # Use Gemini (free, easy, works immediately)
            from app.services.content_generation.gemini_service import GeminiContentGenerator
            generator = GeminiContentGenerator()
        else:
            # Use AWS Bedrock (requires setup)
            from app.services.content_generation.bedrock_service import BedrockContentGenerator
            generator = BedrockContentGenerator()
        
        result = generator.generate_content(
            prompt=request.prompt,
            language=request.language,
            tone=request.tone,
            content_type=request.content_type
        )
        
        return ContentResponse(
            content=result['content'],
            language=request.language,
            model_used=result['model_name'],
            generation_time_ms=result['generation_time_ms']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
