from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Cloud Assignment Portal API"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173"
    MAX_UPLOAD_BYTES: int = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS: str = ".pdf,.doc,.docx,.ppt,.pptx,.zip,.png,.jpg,.jpeg"
    ALLOW_LATE_SUBMISSIONS: bool = True
    STORAGE_BACKEND: str = "local"
    LOCAL_STORAGE_DIR: str = "storage"
    S3_ENDPOINT_URL: str | None = None
    S3_REGION: str = "us-east-1"
    S3_BUCKET: str = "assignment-portal"
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins(self):
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    @property
    def allowed_extensions(self):
        return {x.strip().lower() for x in self.ALLOWED_EXTENSIONS.split(",") if x.strip()}

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
