"""
Enhanced AI Service Manager with Circuit Breaker and Intelligent Fallback
Implements resilient AI service calls with automatic failover
"""

import os
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import time
import logging
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
from pybreaker import CircuitBreakerError

from app.config.circuit_breaker_config import get_circuit_breaker_manager

load_dotenv()
logger = logging.getLogger(__name__)


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


class AIServiceError(Exception):
    """Base exception for AI service errors"""
    pass


class AIServiceTimeoutError(AIServiceError):
    """Raised when AI service times out"""
    pass


class AIServiceRateLimitError(AIServiceError):
    """Raised when AI service rate limit is hit"""
    pass


class AIServiceUnavailableError(AIServiceError):
    """Raised when AI service is unavailable"""
    pass


class EnhancedAIServiceManager:
    """
    Enhanced AI service manager with:
    1. Circuit breaker pattern for fault tolerance
    2. Intelligent fallback to alternative services
    3. Retry logic with exponential backoff
    4. Comprehensive error handling and logging
    5. Service health monitoring
    """
    
    def __init__(self):
        self.circuit_breaker_manager = get_circuit_breaker_manager()
        self.available_services = self._detect_available_services()
        self.fallback_chain = self._build_fallback_chain()
        self.service_clients = {}
        self._initialize_services()
        
        # Statistics tracking
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "fallback_used": 0,
            "service_usage": {provider.value: 0 for provider in AIProvider}
        }
    
    def _detect_available_services(self) -> Dict[AIProvider, bool]:
        """Detect which AI services have valid API keys configured"""
        services = {}
        
        # Google Gemini
        gemini_key = os.getenv('GEMINI_API_KEY')
        services[AIProvider.GEMINI] = bool(gemini_key and gemini_key != 'your_gemini_api_key_here')
        
        # AWS Bedrock
        aws_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_bearer = os.getenv('AWS_BEARER_TOKEN_BEDROCK')
        services[AIProvider.BEDROCK] = bool(aws_key or aws_bearer)
        
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        services[AIProvider.OPENAI] = bool(openai_key and openai_key != 'your_openai_api_key_here')
        
        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        services[AIProvider.ANTHROPIC] = bool(anthropic_key and anthropic_key != 'your_anthropic_api_key_here')
        
        # Cohere
        cohere_key = os.getenv('COHERE_API_KEY')
        services[AIProvider.COHERE] = bool(cohere_key and cohere_key != 'your_cohere_api_key_here')
        
        # HuggingFace
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        services[AIProvider.HUGGINGFACE] = bool(hf_key and hf_key != 'your_huggingface_api_key_here')
        
        # Groq
        groq_key = os.getenv('GROQ_API_KEY')
        services[AIProvider.GROQ] = bool(groq_key and groq_key != 'your_groq_api_key_here')
        
        # Together AI
        together_key = os.getenv('TOGETHER_API_KEY')
        services[AIProvider.TOGETHER] = bool(together_key and together_key != 'your_together_api_key_here')
        
        return services
    
    def _build_fallback_chain(self) -> List[AIProvider]:
        """
        Build fallback chain based on service availability and priority
        
        Priority order:
        1. Gemini (free tier, good multilingual)
        2. Bedrock (AWS, reliable)
        3. OpenAI (high quality)
        4. Anthropic (Claude, excellent content)
        5. Groq (fast inference)
        6. Cohere (good generation)
        7. Together (open source)
        8. HuggingFace (fallback)
        """
        priority_order = [
            AIProvider.GEMINI,
            AIProvider.BEDROCK,
            AIProvider.OPENAI,
            AIProvider.ANTHROPIC,
            AIProvider.GROQ,
            AIProvider.COHERE,
            AIProvider.TOGETHER,
            AIProvider.HUGGINGFACE,
        ]
        
        # Filter to only available services
        fallback_chain = [
            provider for provider in priority_order
            if self.available_services.get(provider, False)
        ]
        
        logger.info(f"Fallback chain built: {[p.value for p in fallback_chain]}")
        return fallback_chain
    
    def _initialize_services(self):
        """Initialize available service clients"""
        if self.available_services.get(AIProvider.GEMINI):
            try:
                from app.services.content_generation.gemini_service import GeminiContentGenerator
                self.service_clients[AIProvider.GEMINI] = GeminiContentGenerator()
                logger.info("Initialized Gemini service")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        if self.available_services.get(AIProvider.BEDROCK):
            try:
                from app.services.content_generation.bedrock_service import BedrockContentGenerator
                self.service_clients[AIProvider.BEDROCK] = BedrockContentGenerator()
                logger.info("Initialized Bedrock service")
            except Exception as e:
                logger.error(f"Failed to initialize Bedrock: {e}")
        
        if self.available_services.get(AIProvider.OPENAI):
            try:
                from app.services.content_generation.openai_service import OpenAIContentGenerator
                self.service_clients[AIProvider.OPENAI] = OpenAIContentGenerator()
                logger.info("Initialized OpenAI service")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI: {e}")
        
        if self.available_services.get(AIProvider.ANTHROPIC):
            try:
                from app.services.content_generation.anthropic_service import AnthropicContentGenerator
                self.service_clients[AIProvider.ANTHROPIC] = AnthropicContentGenerator()
                logger.info("Initialized Anthropic service")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic: {e}")
        
        if self.available_services.get(AIProvider.COHERE):
            try:
                from app.services.content_generation.cohere_service import CohereContentGenerator
                self.service_clients[AIProvider.COHERE] = CohereContentGenerator()
                logger.info("Initialized Cohere service")
            except Exception as e:
                logger.error(f"Failed to initialize Cohere: {e}")
    
    def _call_service_with_circuit_breaker(
        self,
        provider: AIProvider,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call AI service with circuit breaker protection
        
        Raises:
            CircuitBreakerError: If circuit is open
            AIServiceError: If service call fails
        """
        client = self.service_clients.get(provider)
        if not client:
            raise AIServiceUnavailableError(f"Service client for {provider.value} not initialized")
        
        # Define the actual service call
        def service_call():
            return client.generate_content(prompt=prompt, **kwargs)
        
        # Call with circuit breaker
        try:
            result = self.circuit_breaker_manager.call_with_circuit_breaker(
                service_name=provider.value,
                func=service_call
            )
            return result
        except CircuitBreakerError:
            logger.warning(f"Circuit breaker is OPEN for {provider.value}")
            raise AIServiceUnavailableError(f"{provider.value} service is temporarily unavailable")
        except Exception as e:
            # Classify the error
            error_msg = str(e).lower()
            
            if "timeout" in error_msg or "timed out" in error_msg:
                raise AIServiceTimeoutError(f"{provider.value} timeout: {str(e)}")
            elif "rate limit" in error_msg or "429" in error_msg:
                raise AIServiceRateLimitError(f"{provider.value} rate limit: {str(e)}")
            elif "500" in error_msg or "503" in error_msg or "502" in error_msg:
                raise AIServiceUnavailableError(f"{provider.value} server error: {str(e)}")
            else:
                raise AIServiceError(f"{provider.value} error: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((AIServiceTimeoutError, AIServiceUnavailableError)),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    def _try_service_with_retry(
        self,
        provider: AIProvider,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Try calling service with retry logic
        
        Retries up to 2 times with exponential backoff for:
        - Timeout errors
        - Service unavailable errors
        """
        return self._call_service_with_circuit_breaker(provider, prompt, **kwargs)
    
    def generate_content_with_fallback(
        self,
        prompt: str,
        language: str = "hindi",
        tone: str = "casual",
        content_type: str = "social_post",
        preferred_service: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content with intelligent fallback
        
        Process:
        1. Try preferred service (if specified) or first in fallback chain
        2. If fails, automatically try next service in fallback chain
        3. Continue until success or all services exhausted
        4. Log all attempts and failures
        
        Args:
            prompt: Content generation prompt
            language: Target language
            tone: Content tone
            content_type: Type of content
            preferred_service: Specific service to try first (optional)
            **kwargs: Additional parameters
        
        Returns:
            Dict with generated content and metadata
        
        Raises:
            AIServiceError: If all services fail
        """
        self.stats["total_requests"] += 1
        start_time = time.time()
        
        # Build service attempt order
        if preferred_service:
            try:
                preferred_provider = AIProvider(preferred_service)
                if preferred_provider in self.fallback_chain:
                    # Put preferred service first
                    attempt_order = [preferred_provider] + [
                        p for p in self.fallback_chain if p != preferred_provider
                    ]
                else:
                    logger.warning(f"Preferred service {preferred_service} not available")
                    attempt_order = self.fallback_chain
            except ValueError:
                logger.warning(f"Invalid preferred service: {preferred_service}")
                attempt_order = self.fallback_chain
        else:
            attempt_order = self.fallback_chain
        
        if not attempt_order:
            raise AIServiceError("No AI services available. Please configure at least one API key.")
        
        # Track all attempts
        attempts = []
        last_error = None
        
        # Try each service in order
        for idx, provider in enumerate(attempt_order):
            try:
                logger.info(f"Attempting {provider.value} (attempt {idx + 1}/{len(attempt_order)})")
                
                # Try service with retry
                result = self._try_service_with_retry(
                    provider=provider,
                    prompt=prompt,
                    language=language,
                    tone=tone,
                    content_type=content_type,
                    **kwargs
                )
                
                # Success!
                execution_time = time.time() - start_time
                
                # Add metadata
                result['service_used'] = provider.value
                result['fallback_used'] = idx > 0
                result['attempts'] = idx + 1
                result['execution_time'] = round(execution_time, 2)
                
                # Update statistics
                self.stats["successful_requests"] += 1
                self.stats["service_usage"][provider.value] += 1
                if idx > 0:
                    self.stats["fallback_used"] += 1
                
                logger.info(
                    f"✓ Success with {provider.value} "
                    f"(attempt {idx + 1}, {execution_time:.2f}s)"
                )
                
                return result
            
            except (AIServiceError, CircuitBreakerError) as e:
                # Log the failure
                error_type = type(e).__name__
                logger.warning(
                    f"✗ {provider.value} failed: {error_type} - {str(e)}"
                )
                
                attempts.append({
                    "service": provider.value,
                    "error_type": error_type,
                    "error_message": str(e),
                    "timestamp": time.time()
                })
                
                last_error = e
                
                # If this is not the last service, continue to next
                if idx < len(attempt_order) - 1:
                    logger.info(f"Trying fallback service: {attempt_order[idx + 1].value}")
                    continue
                else:
                    # All services exhausted
                    break
            
            except Exception as e:
                # Unexpected error
                logger.error(f"Unexpected error with {provider.value}: {str(e)}", exc_info=True)
                attempts.append({
                    "service": provider.value,
                    "error_type": "UnexpectedError",
                    "error_message": str(e),
                    "timestamp": time.time()
                })
                last_error = e
                
                # Continue to next service
                if idx < len(attempt_order) - 1:
                    continue
                else:
                    break
        
        # All services failed
        self.stats["failed_requests"] += 1
        execution_time = time.time() - start_time
        
        error_summary = {
            "message": "All AI services failed",
            "attempts": attempts,
            "total_attempts": len(attempts),
            "execution_time": round(execution_time, 2),
            "last_error": str(last_error) if last_error else "Unknown error"
        }
        
        logger.error(f"All AI services failed after {len(attempts)} attempts: {error_summary}")
        
        raise AIServiceError(
            f"All AI services failed. Tried {len(attempts)} services. "
            f"Last error: {str(last_error)}"
        )
    
    def get_service_health(self) -> Dict[str, Any]:
        """Get health status of all services"""
        health_status = {}
        
        for provider in AIProvider:
            if self.available_services.get(provider, False):
                circuit_status = self.circuit_breaker_manager.get_circuit_status(provider.value)
                health_status[provider.value] = {
                    "available": True,
                    "circuit_state": circuit_status["state"],
                    "is_healthy": circuit_status["is_available"],
                    "fail_counter": circuit_status["fail_counter"],
                    "fail_max": circuit_status["fail_max"],
                    "usage_count": self.stats["service_usage"].get(provider.value, 0)
                }
            else:
                health_status[provider.value] = {
                    "available": False,
                    "circuit_state": "n/a",
                    "is_healthy": False,
                    "reason": "API key not configured"
                }
        
        return health_status
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        success_rate = (
            (self.stats["successful_requests"] / self.stats["total_requests"] * 100)
            if self.stats["total_requests"] > 0 else 0
        )
        
        fallback_rate = (
            (self.stats["fallback_used"] / self.stats["successful_requests"] * 100)
            if self.stats["successful_requests"] > 0 else 0
        )
        
        return {
            "total_requests": self.stats["total_requests"],
            "successful_requests": self.stats["successful_requests"],
            "failed_requests": self.stats["failed_requests"],
            "success_rate": round(success_rate, 2),
            "fallback_used": self.stats["fallback_used"],
            "fallback_rate": round(fallback_rate, 2),
            "service_usage": self.stats["service_usage"],
            "available_services": len(self.fallback_chain),
            "fallback_chain": [p.value for p in self.fallback_chain]
        }
    
    def reset_statistics(self):
        """Reset usage statistics"""
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "fallback_used": 0,
            "service_usage": {provider.value: 0 for provider in AIProvider}
        }
        logger.info("Statistics reset")


# Global instance
_enhanced_ai_service_manager = None


def get_enhanced_ai_service_manager() -> EnhancedAIServiceManager:
    """Get or create global enhanced AI service manager instance"""
    global _enhanced_ai_service_manager
    if _enhanced_ai_service_manager is None:
        _enhanced_ai_service_manager = EnhancedAIServiceManager()
    return _enhanced_ai_service_manager


def generate_content_with_fallback(prompt: str, **kwargs) -> Dict[str, Any]:
    """Convenience function for content generation with fallback"""
    manager = get_enhanced_ai_service_manager()
    return manager.generate_content_with_fallback(prompt=prompt, **kwargs)


def get_service_health() -> Dict[str, Any]:
    """Convenience function to get service health"""
    manager = get_enhanced_ai_service_manager()
    return manager.get_service_health()


def get_ai_statistics() -> Dict[str, Any]:
    """Convenience function to get AI statistics"""
    manager = get_enhanced_ai_service_manager()
    return manager.get_statistics()
