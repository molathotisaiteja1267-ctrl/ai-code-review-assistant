from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "AI Code Review Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "production-secret-key-change-in-production-min-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./code_review.db"
    
    # LLM Provider Configuration
    LLM_PROVIDER: str = "smart_fallback"
    LLM_API_KEY: Optional[str] = ""
    LLM_MODEL: str = "gpt-4o"
    LLM_BASE_URL: Optional[str] = None
    LLM_TEMPERATURE: float = 0.2
    LLM_TIMEOUT_SECONDS: int = 45
    
    # Pipeline Settings
    MIN_CONFIDENCE: float = 0.60
    MAX_FILE_SIZE_KB: int = 2048
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # GitHub Integration
    GITHUB_TOKEN: Optional[str] = ""
    GITHUB_CLIENT_ID: Optional[str] = ""
    GITHUB_CLIENT_SECRET: Optional[str] = ""

settings = Settings()
