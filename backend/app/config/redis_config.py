"""
Redis Configuration for Caching and Task Progress Tracking
"""
import redis.asyncio as aioredis
import redis
import os
from dotenv import load_dotenv
import json
from typing import Optional, Any

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Async Redis client for FastAPI
async_redis_client: Optional[aioredis.Redis] = None

# Sync Redis client for Celery tasks
sync_redis_client: Optional[redis.Redis] = None


async def get_async_redis() -> aioredis.Redis:
    """Get async Redis client for FastAPI endpoints"""
    global async_redis_client
    if async_redis_client is None:
        async_redis_client = await aioredis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
    return async_redis_client


def get_sync_redis() -> redis.Redis:
    """Get sync Redis client for Celery tasks"""
    global sync_redis_client
    if sync_redis_client is None:
        sync_redis_client = redis.from_url(
            REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
    return sync_redis_client


async def close_async_redis():
    """Close async Redis connection"""
    global async_redis_client
    if async_redis_client:
        await async_redis_client.close()
        async_redis_client = None


def close_sync_redis():
    """Close sync Redis connection"""
    global sync_redis_client
    if sync_redis_client:
        sync_redis_client.close()
        sync_redis_client = None


class TaskProgressTracker:
    """Track task progress in Redis for SSE updates"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def set_progress(
        self,
        task_id: str,
        current: int,
        total: int,
        status: str = "processing",
        message: str = "",
        result: Optional[Any] = None
    ):
        """Update task progress"""
        progress_data = {
            "task_id": task_id,
            "current": current,
            "total": total,
            "percentage": round((current / total) * 100, 2) if total > 0 else 0,
            "status": status,
            "message": message,
            "result": result,
        }
        
        # Store in Redis with 24-hour expiration
        self.redis.setex(
            f"task_progress:{task_id}",
            86400,  # 24 hours
            json.dumps(progress_data)
        )
        
        # Publish to channel for SSE
        self.redis.publish(
            f"task_progress_channel:{task_id}",
            json.dumps(progress_data)
        )
    
    def get_progress(self, task_id: str) -> Optional[dict]:
        """Get current task progress"""
        data = self.redis.get(f"task_progress:{task_id}")
        if data:
            return json.loads(data)
        return None
    
    def delete_progress(self, task_id: str):
        """Delete task progress"""
        self.redis.delete(f"task_progress:{task_id}")


class AsyncTaskProgressTracker:
    """Async version for FastAPI endpoints"""
    
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client
    
    async def get_progress(self, task_id: str) -> Optional[dict]:
        """Get current task progress"""
        data = await self.redis.get(f"task_progress:{task_id}")
        if data:
            return json.loads(data)
        return None
    
    async def subscribe_to_progress(self, task_id: str):
        """Subscribe to task progress updates (for SSE)"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"task_progress_channel:{task_id}")
        return pubsub
