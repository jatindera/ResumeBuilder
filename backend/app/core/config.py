from pydantic_settings import BaseSettings
from typing import Optional, List
from pathlib import Path
from urllib.parse import quote_plus


class Settings(BaseSettings):
    # Version Settings
    VERSION: str = "1.0.0"
    
    # Swagger UI Settings
    ENABLE_SWAGGER_AUTH: bool = False  # Default to False for safety
    
    # API Settings
    API_VERSION: str = "v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Rate Limiter Settings
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_WINDOW: int = 60
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Project Settings
    PROJECT_NAME: str = "Resume Builder API"
    TEMP_DIR: str = "temp"
    
    # Database Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "resumebuilder"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None

    # Google OAuth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"

    # OpenAI Settings
    OPENAI_API_KEY: str

    # Security Settings
    SECRET_KEY: str
    
    # Pool Settings
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 3600

    @property
    def get_database_url(self) -> str:
        """Construct database URL if not provided"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # URL encode the password to handle special characters
        encoded_password = quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql://{self.POSTGRES_USER}:{encoded_password}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
settings.DATABASE_URL = settings.get_database_url
