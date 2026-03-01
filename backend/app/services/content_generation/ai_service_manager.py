"""
Unified AI Service Manager
Automatically detects and uses available AI services based on API keys
Supports: Google Gemini, AWS Bedrock, OpenAI, Anthropic, Cohere, and more
"""

import os
from typing import Dict, Any, Optional, List
from enum import Enum
import time
from dotenv import load_dotenv

load_dotenv()


class AIProvider(str, Enum):
    """Supported AI providers"""
    GEMINI = "gemini"
    BEDROCK = "bedrock"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"
    HUGGINGFACE = "huggingface"
    GROQ = "groq"
    TOGETHER = "together"


class AIServiceManager:
    """
    Intelligent AI service manager that:
    1. Detects available API keys
    2. Selects best available service
    3. Provides fallback options
    4. Unified interface for all providers
    """
    
    def __init__(self):
        self.available_services = self._detect_available_services()
        self.primary_service = self._select_primary_service()
        self._initialize_services()
    
    def _detect_available_services(self) -> Dict[AIProvider, bool]:
        """Detect which AI services have valid API keys configured"""
        services = {}
        
        # Google Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        services[AIProvider.GEMINI] = bool(gemini_key and gemini_key != 'your_gemini_api_key_here')
        
        # AWS Bedrock (check for credentials or bearer token)
        aws_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_bearer = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        services[AIProvider.BEDROCK] = bool(aws_key or aws_bearer)
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        services[AIProvider.OPENAI] = bool(openai_key and openai_key != 'your_openai_api_key_here')
        
        # Anthropic (Claude API)
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        services[AIProvider.ANTHROPIC] = bool(anthropic_key and anthropic_key != 'your_anthropic_api_key_here')
        
        # Cohere
        cohere_key = os.getenv('COHERE_API_KEY')
        services[AIProvider.COHERE] = bool(cohere_key and cohere_key != 'your_cohere_api_key_here')
        
        # HuggingFace
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        services[AIProvider.HUGGINGFACE] = bool(hf_key and hf_key != 'your_huggingface_api_key_here')
        
        # Groq (fast inference)
        groq_key = os.getenv('GROQ_API_KEY')
        services[AIProvider.GROQ] = bool(groq_key and groq_key != 'your_groq_api_key_here')
        
        # Together AI
        together_key = os.getenv('TOGETHER_API_KEY')
        services[AIProvider.TOGETHER] = bool(together_key and together_key != 'your_together_api_key_here')
        
        return services
    
    def _select_primary_service(self) -> Optional[AIProvider]:
        """
        Select primary service based on priority and availability
        Priority: Gemini > Bedrock > OpenAI > Anthropic > Others
        """
        priority_order = [
            AIProvider.GEMINI,      # Free tier, good multilingual support
            AIProvider.BEDROCK,     # AWS integration, multiple models
            AIProvider.OPENAI,      # High quality, widely used
            AIProvider.ANTHROPIC,   # Claude, excellent for content
            AIProvider.GROQ,        # Fast inference
            AIProvider.COHERE,      # Good for generation
            AIProvider.TOGETHER,    # Open source models
            AIProvider.HUGGINGFACE, # Fallback option
        ]
        
        for provider in priority_order:
            if self.available_services.get(provider, False):
                return provider
        
        return None
    
    def _initialize_services(self):
        """Initialize available service clients"""
        self.service_clients = {}
        
        if self.available_services.get(AIProvider.GEMINI):
            try:
                from app.services.content_generation.gemini_service import GeminiContentGenerator
                self.service_clients[AIProvider.GEMINI] = GeminiContentGenerator()
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
        
        if self.available_services.get(AIProvider.BEDROCK):
            try:
                from app.services.content_generation.bedrock_service import BedrockContentGenerator
                self.service_clients[AIProvider.BEDROCK] = BedrockContentGenerator()
            except Exception as e:
                print(f"Failed to initialize Bedrock: {e}")
        
        if self.available_services.get(AIProvider.OPENAI):
            try:
                from app.services.content_generation.openai_service import OpenAIContentGenerator
                self.service_clients[AIProvider.OPENAI] = OpenAIContentGenerator()
            except Exception as e:
                print(f"Failed to initialize OpenAI: {e}")
        
        if self.available_services.get(AIProvider.ANTHROPIC):
            try:
                from app.services.content_generation.anthropic_service import AnthropicContentGenerator
                self.service_clients[AIProvider.ANTHROPIC] = AnthropicContentGenerator()
            except Exception as e:
                print(f"Failed to initialize Anthropic: {e}")
        
        if self.available_services.get(AIProvider.COHERE):
            try:
                from app.services.content_generation.cohere_service import CohereContentGenerator
                self.service_clients[AIProvider.COHERE] = CohereContentGenerator()
            except Exception as e:
                print(f"Failed to initialize Cohere: {e}")
    
    def get_available_services(self) -> List[str]:
        """Get list of available service names"""
        return [provider.value for provider, available in self.available_services.items() if available]
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about available services"""
        return {
            "primary_service": self.primary_service.value if self.primary_service else None,
            "available_services": self.get_available_services(),
            "total_available": len(self.get_available_services()),
            "service_status": {
                provider.value: available 
                for provider, available in self.available_services.items()
            }
        }
    
    def generate_content(
        self,
        prompt: str,
        language: str = "hindi",
        tone: str = "casual",
        content_type: str = "social_post",
        preferred_service: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content using the best available AI service
        
        Args:
            prompt: Content generation prompt
            language: Target language
            tone: Content tone
            content_type: Type of content
            preferred_service: Specific service to use (optional)
            **kwargs: Additional parameters for specific services
        
        Returns:
            Dict with generated content and metadata
        """
        # Determine which service to use
        if preferred_service:
            service_enum = AIProvider(preferred_service)
            if not self.available_services.get(service_enum):
                raise ValueError(f"Service '{preferred_service}' is not available. Available: {self.get_available_services()}")
            service_to_use = service_enum
        else:
            if not self.primary_service:
                raise ValueError("No AI services available. Please configure at least one API key.")
            service_to_use = self.primary_service
        
        # Get the service client
        client = self.service_clients.get(service_to_use)
        if not client:
            raise ValueError(f"Service client for '{service_to_use.value}' not initialized")
        
        # Generate content with fallback
        try:
            result = client.generate_content(
                prompt=prompt,
                language=language,
                tone=tone,
                content_type=content_type,
                **kwargs
            )
            result['service_used'] = service_to_use.value
            return result
        
        except Exception as e:
            # Try fallback services
            print(f"Primary service {service_to_use.value} failed: {e}")
            
            for fallback_service, available in self.available_services.items():
                if available and fallback_service != service_to_use:
                    try:
                        print(f"Trying fallback service: {fallback_service.value}")
                        fallback_client = self.service_clients.get(fallback_service)
                        if fallback_client:
                            result = fallback_client.generate_content(
                                prompt=prompt,
                                language=language,
                                tone=tone,
                                content_type=content_type,
                                **kwargs
                            )
                            result['service_used'] = fallback_service.value
                            result['fallback_used'] = True
                            return result
                    except Exception as fallback_error:
                        print(f"Fallback service {fallback_service.value} also failed: {fallback_error}")
                        continue
            
            # All services failed
            raise Exception(f"All AI services failed. Last error: {str(e)}")
    
    def summarize_content(
        self,
        text: str,
        target_length: int = 100,
        language: str = "english",
        **kwargs
    ) -> Dict[str, Any]:
        """Summarize existing content"""
        prompt = f"""Summarize the following text in approximately {target_length} words.
Maintain the key points and overall message.

Text to summarize:
{text}

Provide a concise summary:"""
        
        return self.generate_content(
            prompt=prompt,
            language=language,
            tone="professional",
            content_type="social_post",
            **kwargs
        )
    
    def translate_content(
        self,
        text: str,
        source_language: str,
        target_language: str,
        maintain_tone: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """Translate content between languages"""
        tone_instruction = "Maintain the original tone and style." if maintain_tone else ""
        
        prompt = f"""Translate the following text from {source_language} to {target_language}.
{tone_instruction}
Make it culturally appropriate for the target audience.

Original text:
{text}

Provide ONLY the translated text in {target_language}:"""
        
        return self.generate_content(
            prompt=prompt,
            language=target_language,
            tone="neutral",
            content_type="social_post",
            **kwargs
        )
    
    def enhance_content(
        self,
        text: str,
        enhancement_type: str = "improve",
        language: str = "english",
        **kwargs
    ) -> Dict[str, Any]:
        """Enhance existing content (improve, expand, simplify, etc.)"""
        enhancement_prompts = {
            "improve": "Improve and enhance the following content while maintaining its core message:",
            "expand": "Expand and elaborate on the following content with more details:",
            "simplify": "Simplify and make the following content more accessible:",
            "formalize": "Make the following content more formal and professional:",
            "casualize": "Make the following content more casual and conversational:",
        }
        
        instruction = enhancement_prompts.get(enhancement_type, enhancement_prompts["improve"])
        
        prompt = f"""{instruction}

{text}

Enhanced version:"""
        
        return self.generate_content(
            prompt=prompt,
            language=language,
            tone="neutral",
            content_type="social_post",
            **kwargs
        )


# Global instance
_ai_service_manager = None


def get_ai_service_manager() -> AIServiceManager:
    """Get or create global AI service manager instance"""
    global _ai_service_manager
    if _ai_service_manager is None:
        _ai_service_manager = AIServiceManager()
    return _ai_service_manager


def get_service_info() -> Dict[str, Any]:
    """Quick function to get service information"""
    manager = get_ai_service_manager()
    return manager.get_service_info()
