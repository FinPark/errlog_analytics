"""
Application configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    PROJECT_NAME: str = "Error Log Analytics"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ]
    
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