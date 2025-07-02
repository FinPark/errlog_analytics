"""
Application configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings
import redis

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    PROJECT_NAME: str = "Error Log Analytics"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # Allow all origins for development
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_FILE_EXTENSIONS: List[str] = [".log", ".LOG"]
    UPLOAD_DIR: str = "uploads"
    
    # Redis Settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()

# Redis client instance
_redis_client = None

def get_redis_client():
    """Get Redis client instance"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client