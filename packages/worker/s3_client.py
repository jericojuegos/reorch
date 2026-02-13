"""
S3/MinIO client for the REORCH Worker.
Downloads input tracks and uploads processed outputs.
"""
import os
from pathlib import Path

import aioboto3
from botocore.exceptions import ClientError

from config import settings


class WorkerS3Client:
    """Async S3 client for worker file operations."""

    def __init__(self):
        self.session = aioboto3.Session()

    def _client_kwargs(self) -> dict:
        return {
            "endpoint_url": settings.s3_endpoint,
            "aws_access_key_id": settings.s3_access_key,
            "aws_secret_access_key": settings.s3_secret_key,
        }

    async def download_track(self, storage_path: str, local_path: str) -> str:
        """
        Download a track from S3 to a local file.

        Args:
            storage_path: S3 key (e.g. "uploads/{project}/{track}.wav")
            local_path: Local destination path

        Returns:
            The local_path for convenience.
        """
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        async with self.session.client("s3", **self._client_kwargs()) as s3:
            try:
                await s3.download_file(settings.s3_bucket, storage_path, local_path)
                return local_path
            except ClientError as e:
                raise RuntimeError(f"Failed to download {storage_path}: {e}")

    async def upload_output(self, local_path: str, output_key: str) -> str:
        """
        Upload a processed file to S3.

        Args:
            local_path: Local file path to upload
            output_key: S3 key for the output (e.g. "outputs/{job_id}/result.wav")

        Returns:
            The output_key for convenience.
        """
        async with self.session.client("s3", **self._client_kwargs()) as s3:
            try:
                await s3.upload_file(local_path, settings.s3_bucket, output_key)
                return output_key
            except ClientError as e:
                raise RuntimeError(f"Failed to upload to {output_key}: {e}")


# Global instance
s3_client = WorkerS3Client()
