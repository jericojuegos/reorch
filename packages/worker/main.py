"""
REORCH Worker - Audio processing job worker.
"""
import asyncio
import signal
import sys
from typing import NoReturn

from config import settings
from queue_client import QueueClient
from database import update_job_status, update_job_progress


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
        preset = job.get("preset", "unknown")
        track_id = job.get("track_id", "unknown")
        print(f"🔄 Processing job {job_id} (preset: {preset}, track: {track_id})")

        try:
            # Mark as running
            await update_job_status(job_id, "running", progress=0)

            # Simulate processing stages with progress
            stages = [
                (25, "Analyzing audio..."),
                (50, "Applying transformation..."),
                (75, "Rendering output..."),
                (100, "Finalizing..."),
            ]

            for progress, stage_name in stages:
                print(f"  ⏳ [{progress}%] {stage_name}")
                await asyncio.sleep(1)  # Simulate work
                await update_job_progress(job_id, progress)

            # Mark as succeeded
            await update_job_status(job_id, "succeeded", progress=100)
            print(f"✅ Completed job {job_id}")

        except Exception as e:
            print(f"❌ Job {job_id} failed: {e}")
            await update_job_status(
                job_id, "failed",
                error_message=str(e),
            )

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

