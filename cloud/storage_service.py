"""Storage adapter notes.

Use STORAGE_BACKEND=local for development, MinIO for local S3-compatible
testing, and STORAGE_BACKEND=s3 with a private AWS S3 bucket in deployment.
"""
from os import getenv

def storage_target():
    return getenv("STORAGE_BACKEND", "local")
