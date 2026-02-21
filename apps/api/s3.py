"""
S3/MinIO client for file storage.
"""
from typing import BinaryIO
from uuid import uuid4

import aioboto3
from botocore.exceptions import ClientError

from config import settings


class S3Client:
    """Async S3/MinIO client for file operations."""
    
    def __init__(self):
        self.session = aioboto3.Session()
        self.endpoint = settings.s3_endpoint
        self.access_key = settings.s3_access_key
        self.secret_key = settings.s3_secret_key
        self.bucket = settings.s3_bucket
    
    async def upload_file(
        self,
        file_obj: BinaryIO,
        project_id: str,
        filename: str,
        content_type: str,
    ) -> str:
        """
        Upload a file to S3/MinIO.
        
        Args:
            file_obj: File-like object to upload
            project_id: Project UUID
            filename: Original filename with extension
            content_type: MIME type (e.g., 'audio/mpeg')
        
        Returns:
            Storage path (S3 key)
        """
        # Generate unique storage path
        file_ext = filename.rsplit('.', 1)[-1].lower()
        track_id = str(uuid4())
        storage_path = f"uploads/{project_id}/{track_id}.{file_ext}"
        
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3:
            try:
                await s3.put_object(
                    Bucket=self.bucket,
                    Key=storage_path,
                    Body=file_obj,
                    ContentType=content_type,
                )
                return storage_path
            except ClientError as e:
                raise RuntimeError(f"Failed to upload file to S3: {e}")
    
    async def generate_presigned_url(self, storage_path: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL to download a file.
        
        Args:
            storage_path: S3 key of the file
            expiration: Time in seconds until URL expires (default 1 hour)
            
        Returns:
            URL string
        """
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3:
            try:
                url = await s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket, 'Key': storage_path},
                    ExpiresIn=expiration
                )
                return url
            except ClientError as e:
                raise RuntimeError(f"Failed to generate presigned URL: {e}")
    
    async def ensure_bucket_exists(self) -> None:
        """Create bucket if it doesn't exist."""
        async with self.session.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        ) as s3:
            try:
                await s3.head_bucket(Bucket=self.bucket)
            except ClientError:
                # Bucket doesn't exist, create it
                await s3.create_bucket(Bucket=self.bucket)


# Global S3 client instance
s3_client = S3Client()
