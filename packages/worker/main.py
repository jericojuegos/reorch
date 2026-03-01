"""
REORCH Worker - Audio processing job worker.
"""
import asyncio
import os
import shutil
import signal
import sys
from typing import NoReturn

from config import settings
from queue_client import QueueClient
from database import update_job_status, update_job_progress
from s3_client import s3_client
from pipeline import run_pipeline

MAX_RETRIES = 3


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
        preset = job.get("preset", "ballad_to_rock")
        track_id = job.get("track_id", "unknown")
        storage_path = job.get("storage_path", "")
        # Get retry count from the job payload, default to 0
        retries = job.get("retries", 0)
        
        print(f"🔄 Processing job {job_id} (preset: {preset}, track: {track_id}, attempt: {retries + 1}/{MAX_RETRIES + 1})")

        # Local working directories
        job_dir = os.path.join(settings.temp_dir, job_id)
        input_dir = os.path.join(job_dir, "input")
        output_dir = os.path.join(job_dir, "output")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Mark as running
            await update_job_status(job_id, "running", progress=0)

            # Download track from S3
            ext = os.path.splitext(storage_path)[1] or ".wav"
            local_input = os.path.join(input_dir, f"input{ext}")
            print(f"  ⬇️  Downloading from S3: {storage_path}")
            await s3_client.download_track(storage_path, local_input)

            # Run the audio pipeline with progress updates and a strict 15-minute timeout
            async def on_progress(pct: int, msg: str):
                print(f"  ⏳ [{pct}%] {msg}")
                await update_job_progress(job_id, pct)

            try:
                # We use asyncio.wait_for to enforce a 15-minute max processing time per job
                result = await asyncio.wait_for(
                    run_pipeline(
                        input_path=local_input,
                        output_dir=output_dir,
                        preset=preset,
                        on_progress=on_progress,
                    ),
                    timeout=900.0,
                )
            except asyncio.TimeoutError:
                raise RuntimeError(f"Job processing exceeded the maximum time limit of 15 minutes.")

            # Upload outputs to S3
            wav_key = f"outputs/{job_id}/result.wav"
            mp3_key = f"outputs/{job_id}/result.mp3"
            print(f"  ⬆️  Uploading results to S3")
            await s3_client.upload_output(result.wav_path, wav_key)
            await s3_client.upload_output(result.mp3_path, mp3_key)

            # Upload stem files to S3
            for stem_name, stem_path in result.separation.stem_paths.items():
                stem_key = f"outputs/{job_id}/stems/{stem_name}.wav"
                await s3_client.upload_output(stem_path, stem_key)
            print(f"  ⬆️  Uploaded {len(result.separation.stem_paths)} stems to S3")

            # Mark as succeeded
            await update_job_status(
                job_id, "succeeded",
                progress=100,
                output_path=mp3_key,
            )
            print(f"✅ Completed job {job_id}")

        except Exception as e:
            print(f"❌ Job {job_id} failed on attempt {retries + 1}: {e}")
            if retries < MAX_RETRIES:
                print(f"  ↪️  Requeuing job {job_id} (Attempt {retries + 2}/{MAX_RETRIES + 1})")
                job["retries"] = retries + 1
                await self.queue.enqueue(job)
            else:
                print(f"❌ Job {job_id} exceeded maximum retries. Marking as failed.")
                await update_job_status(
                    job_id, "failed",
                    error_message=str(e),
                )
        finally:
            # Clean up local files
            shutil.rmtree(job_dir, ignore_errors=True)

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
