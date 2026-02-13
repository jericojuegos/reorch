"""
Redis queue client for the API (enqueue side).
"""
import json
from typing import Optional

import redis.asyncio as redis

from config import settings


class JobQueue:
    """Async Redis client for enqueuing jobs."""

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

    async def enqueue_job(
        self, job_id: str, track_id: str, preset: str, storage_path: str,
    ) -> None:
        """
        Push a job onto the Redis queue.

        Args:
            job_id: UUID of the job record in the database
            track_id: UUID of the track to process
            preset: Processing preset name (e.g., 'ballad_to_rock')
            storage_path: S3 key for the uploaded track file
        """
        client = await self._get_client()
        job_payload = json.dumps({
            "id": job_id,
            "track_id": track_id,
            "preset": preset,
            "storage_path": storage_path,
        })
        await client.rpush(settings.redis_queue, job_payload)

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            self._client = None


# Global queue instance
queue = JobQueue()
