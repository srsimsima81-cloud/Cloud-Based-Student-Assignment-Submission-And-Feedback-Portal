from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from .config import settings

class StorageService:
    def __init__(self):
        self.backend = settings.STORAGE_BACKEND.lower()
        if self.backend == "local":
            Path(settings.LOCAL_STORAGE_DIR).mkdir(parents=True, exist_ok=True)
        else:
            self.client = boto3.client(
                "s3", endpoint_url=settings.S3_ENDPOINT_URL,
                region_name=settings.S3_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            self.ensure_bucket()

    def ensure_bucket(self):
        try:
            self.client.head_bucket(Bucket=settings.S3_BUCKET)
        except ClientError:
            if settings.S3_ENDPOINT_URL:
                self.client.create_bucket(Bucket=settings.S3_BUCKET)
            else:
                raise

    def upload(self, data, key, content_type):
        if self.backend == "local":
            path = Path(settings.LOCAL_STORAGE_DIR) / key
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        else:
            self.client.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=data, ContentType=content_type)

    def exists(self, key):
        if self.backend == "local":
            return (Path(settings.LOCAL_STORAGE_DIR) / key).exists()
        try:
            self.client.head_object(Bucket=settings.S3_BUCKET, Key=key)
            return True
        except ClientError:
            return False

    def delete(self, key):
        if self.backend == "local":
            p = Path(settings.LOCAL_STORAGE_DIR) / key
            if p.exists(): p.unlink()
        else:
            self.client.delete_object(Bucket=settings.S3_BUCKET, Key=key)

    def signed_download(self, key, filename):
        if self.backend == "local": return None
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.S3_BUCKET, "Key": key,
                    "ResponseContentDisposition": f'attachment; filename="{filename}"'},
            ExpiresIn=300
        )

    def local_path(self, key):
        return Path(settings.LOCAL_STORAGE_DIR) / key

storage = StorageService()
