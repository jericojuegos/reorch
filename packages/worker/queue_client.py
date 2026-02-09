"""
Redis queue client for job management.
"""
import json
from typing import Optional

import redis.asyncio as redis

from config import settings


class QueueClient:
    """Async Redis queue client for job dequeuing."""

    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def _get_client(self) -> redis.Redis:
        """Get or create Redis connection."""
        if self._client is None:
            self._client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                decode_responses=True,
            )
        return self._client

    async def dequeue(self) -> Optional[dict]:
        """
        Remove and return the next job from the queue.
        Returns None if queue is empty.
        """
        client = await self._get_client()
        result = await client.blpop(settings.redis_queue, timeout=1)

        if result:
            _, job_data = result
            return json.loads(job_data)
        return None

    async def enqueue(self, job: dict) -> None:
        """Add a job to the queue (for testing)."""
        client = await self._get_client()
        await client.rpush(settings.redis_queue, json.dumps(job))

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None
