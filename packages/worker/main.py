"""
REORCH Worker - Audio processing job worker.
"""
import asyncio
import signal
import sys
from typing import NoReturn

from config import settings
from queue_client import QueueClient


class Worker:
    """Audio processing worker that polls Redis for jobs."""

    def __init__(self):
        self.running = False
        self.queue = QueueClient()

    async def start(self) -> NoReturn:
        """Start the worker polling loop."""
        self.running = True
        print(f"🎵 REORCH Worker starting...")
        print(f"📡 Connecting to Redis at {settings.redis_host}:{settings.redis_port}")

        while self.running:
            try:
                job = await self.queue.dequeue()
                if job:
                    await self.process_job(job)
                else:
                    # No job available, wait before polling again
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Error processing job: {e}")
                await asyncio.sleep(5)

    async def process_job(self, job: dict) -> None:
        """Process a single job from the queue."""
        job_id = job.get("id", "unknown")
        job_type = job.get("type", "unknown")
        print(f"🔄 Processing job {job_id} ({job_type})")

        # TODO: Implement actual audio processing in Phase 1
        # For now, just simulate processing
        await asyncio.sleep(2)

        print(f"✅ Completed job {job_id}")

    def stop(self) -> None:
        """Stop the worker gracefully."""
        print("🛑 Stopping worker...")
        self.running = False


def main() -> None:
    """Entry point for the worker."""
    worker = Worker()

    # Handle shutdown signals
    def signal_handler(sig, frame):
        worker.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run the worker
    asyncio.run(worker.start())


if __name__ == "__main__":
    main()
