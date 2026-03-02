"""
Circuit Breaker Configuration for External API Calls
Prevents cascading failures and implements intelligent fallback
"""
from pybreaker import CircuitBreaker, CircuitBreakerError
from typing import Dict, Any, Callable
import logging
from datetime import datetime
from app.config.redis_config import get_sync_redis
import json

logger = logging.getLogger(__name__)


class RedisCircuitBreakerStorage:
    """Redis-backed storage for circuit breaker state"""
    
    def __init__(self, redis_client, namespace="circuit_breaker"):
        self.redis = redis_client
        self.namespace = namespace
    
    def _get_key(self, circuit_name: str) -> str:
        return f"{self.namespace}:{circuit_name}"
    
    def get_state(self, circuit_name: str) -> Dict[str, Any]:
        """Get circuit breaker state from Redis"""
        key = self._get_key(circuit_name)
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return {
            "state": "closed",
            "fail_counter": 0,
            "last_failure": None,
            "opened_at": None
        }
    
    def set_state(self, circuit_name: str, state: Dict[str, Any]):
        """Save circuit breaker state to Redis"""
        key = self._get_key(circuit_name)
        self.redis.setex(key, 3600, json.dumps(state))  # 1 hour TTL
    
    def increment_failure(self, circuit_name: str):
        """Increment failure counter"""
        state = self.get_state(circuit_name)
        state["fail_counter"] += 1
        state["last_failure"] = datetime.utcnow().isoformat()
        self.set_state(circuit_name, state)
    
    def reset(self, circuit_name: str):
        """Reset circuit breaker state"""
        state = {
            "state": "closed",
            "fail_counter": 0,
            "last_failure": None,
            "opened_at": None
        }
        self.set_state(circuit_name, state)


# Circuit breaker configurations for different services
CIRCUIT_BREAKER_CONFIGS = {
    "gemini": {
        "fail_max": 5,              # Open after 5 failures
        "timeout_duration": 60,      # Stay open for 60 seconds
        "expected_exception": Exception,
        "name": "gemini_api"
    },
    "bedrock": {
        "fail_max": 3,              # Open after 3 failures (AWS is usually reliable)
        "timeout_duration": 30,
        "expected_exception": Exception,
        "name": "bedrock_api"
    },
    "openai": {
        "fail_max": 5,
        "timeout_duration": 60,
        "expected_exception": Exception,
        "name": "openai_api"
    },
    "anthropic": {
        "fail_max": 5,
        "timeout_duration": 60,
        "expected_exception": Exception,
        "name": "anthropic_api"
    },
    "cohere": {
        "fail_max": 5,
        "timeout_duration": 60,
        "expected_exception": Exception,
        "name": "cohere_api"
    },
    "huggingface": {
        "fail_max": 10,             # More tolerant for free tier
        "timeout_duration": 120,
        "expected_exception": Exception,
        "name": "huggingface_api"
    },
    "groq": {
        "fail_max": 5,
        "timeout_duration": 60,
        "expected_exception": Exception,
        "name": "groq_api"
    },
    "together": {
        "fail_max": 5,
        "timeout_duration": 60,
        "expected_exception": Exception,
        "name": "together_api"
    },
    # Social media platforms
    "facebook": {
        "fail_max": 3,
        "timeout_duration": 300,     # 5 minutes for social platforms
        "expected_exception": Exception,
        "name": "facebook_api"
    },
    "instagram": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "instagram_api"
    },
    "twitter": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "twitter_api"
    },
    "linkedin": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "linkedin_api"
    },
    "youtube": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "youtube_api"
    },
    "pinterest": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "pinterest_api"
    },
    "tiktok": {
        "fail_max": 3,
        "timeout_duration": 300,
        "expected_exception": Exception,
        "name": "tiktok_api"
    },
}


class CircuitBreakerManager:
    """Manages circuit breakers for all external services"""
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._initialize_circuit_breakers()
    
    def _initialize_circuit_breakers(self):
        """Initialize circuit breakers for all configured services"""
        for service_name, config in CIRCUIT_BREAKER_CONFIGS.items():
            self.circuit_breakers[service_name] = CircuitBreaker(
                fail_max=config["fail_max"],
                timeout_duration=config["timeout_duration"],
                expected_exception=config["expected_exception"],
                name=config["name"],
                listeners=[
                    self._on_circuit_open,
                    self._on_circuit_close,
                    self._on_circuit_half_open
                ]
            )
    
    def _on_circuit_open(self, cb: CircuitBreaker, exc: Exception):
        """Called when circuit breaker opens"""
        logger.warning(
            f"Circuit breaker OPENED for {cb.name}. "
            f"Failures: {cb.fail_counter}/{cb.fail_max}. "
            f"Error: {str(exc)}"
        )
    
    def _on_circuit_close(self, cb: CircuitBreaker):
        """Called when circuit breaker closes"""
        logger.info(f"Circuit breaker CLOSED for {cb.name}. Service recovered.")
    
    def _on_circuit_half_open(self, cb: CircuitBreaker):
        """Called when circuit breaker enters half-open state"""
        logger.info(f"Circuit breaker HALF-OPEN for {cb.name}. Testing service...")
    
    def get_circuit_breaker(self, service_name: str) -> CircuitBreaker:
        """Get circuit breaker for a service"""
        if service_name not in self.circuit_breakers:
            # Create default circuit breaker for unknown services
            self.circuit_breakers[service_name] = CircuitBreaker(
                fail_max=5,
                timeout_duration=60,
                expected_exception=Exception,
                name=f"{service_name}_api"
            )
        return self.circuit_breakers[service_name]
    
    def call_with_circuit_breaker(
        self,
        service_name: str,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute function with circuit breaker protection
        
        Args:
            service_name: Name of the service (e.g., 'gemini', 'openai')
            func: Function to execute
            *args, **kwargs: Arguments to pass to function
        
        Returns:
            Result from function
        
        Raises:
            CircuitBreakerError: If circuit is open
            Exception: If function fails
        """
        cb = self.get_circuit_breaker(service_name)
        
        try:
            result = cb.call(func, *args, **kwargs)
            return result
        except CircuitBreakerError as e:
            logger.error(
                f"Circuit breaker is OPEN for {service_name}. "
                f"Service is temporarily unavailable."
            )
            raise
        except Exception as e:
            logger.error(
                f"Error calling {service_name}: {str(e)}. "
                f"Failures: {cb.fail_counter}/{cb.fail_max}"
            )
            raise
    
    def get_circuit_status(self, service_name: str) -> Dict[str, Any]:
        """Get current status of a circuit breaker"""
        cb = self.get_circuit_breaker(service_name)
        return {
            "service": service_name,
            "state": cb.current_state,
            "fail_counter": cb.fail_counter,
            "fail_max": cb.fail_max,
            "timeout_duration": cb.timeout_duration,
            "last_failure": cb.last_failure_time.isoformat() if cb.last_failure_time else None,
            "is_available": cb.current_state != "open"
        }
    
    def get_all_circuit_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all circuit breakers"""
        return {
            service_name: self.get_circuit_status(service_name)
            for service_name in self.circuit_breakers.keys()
        }
    
    def reset_circuit_breaker(self, service_name: str):
        """Manually reset a circuit breaker"""
        if service_name in self.circuit_breakers:
            cb = self.circuit_breakers[service_name]
            cb.close()
            logger.info(f"Circuit breaker manually reset for {service_name}")
    
    def reset_all_circuit_breakers(self):
        """Manually reset all circuit breakers"""
        for service_name in self.circuit_breakers.keys():
            self.reset_circuit_breaker(service_name)
        logger.info("All circuit breakers manually reset")


# Global circuit breaker manager instance
_circuit_breaker_manager = None


def get_circuit_breaker_manager() -> CircuitBreakerManager:
    """Get or create global circuit breaker manager"""
    global _circuit_breaker_manager
    if _circuit_breaker_manager is None:
        _circuit_breaker_manager = CircuitBreakerManager()
    return _circuit_breaker_manager


def call_with_circuit_breaker(service_name: str, func: Callable, *args, **kwargs) -> Any:
    """Convenience function to call with circuit breaker"""
    manager = get_circuit_breaker_manager()
    return manager.call_with_circuit_breaker(service_name, func, *args, **kwargs)


def get_circuit_status(service_name: str) -> Dict[str, Any]:
    """Convenience function to get circuit status"""
    manager = get_circuit_breaker_manager()
    return manager.get_circuit_status(service_name)


def get_all_circuit_status() -> Dict[str, Dict[str, Any]]:
    """Convenience function to get all circuit statuses"""
    manager = get_circuit_breaker_manager()
    return manager.get_all_circuit_status()
