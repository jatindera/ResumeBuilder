from pydantic_settings import BaseSettings
from typing import List, Dict, Any

class DatabasePoolSettings(BaseSettings):
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10
    POOL_RECYCLE: int = 3600
    POOL_TIMEOUT: int = 30
    POOL_PRE_PING: bool = True

class MySQLSettings(BaseSettings):
    CHARSET: str = "utf8mb4"
    COLLATION: str = "utf8mb4_unicode_ci"
    READ_BUFFER_SIZE: int = 2 * 1024 * 1024  # 2MB
    WRITE_BUFFER_SIZE: int = 2 * 1024 * 1024  # 2MB
    MAX_ALLOWED_PACKET: int = 64 * 1024 * 1024  # 64MB
    INNODB_BUFFER_POOL_SIZE: str = "1G"
    INNODB_LOG_BUFFER_SIZE: int = 32 * 1024 * 1024  # 32MB
    INNODB_LOCK_WAIT_TIMEOUT: int = 50
    CONNECT_TIMEOUT: int = 60
    INTERACTIVE_TIMEOUT: int = 3600

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Resume Builder API"
    OPENAI_API_KEY: str
    TEMP_DIR: str = "temp"
    DATABASE_URL: str = None
    
    # Google OAuth2 settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/callback"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Security headers
    CORS_ORIGINS: list = ["http://localhost:3000"]
    CORS_HEADERS: list = ["*"]
    
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = "resumebuilder"
    
    # Pool settings
    DB_POOL: DatabasePoolSettings = DatabasePoolSettings()
    
    # MySQL settings
    MYSQL: MySQLSettings = MySQLSettings()
    
    # Debug mode
    DEBUG: bool = False

    @property
    def get_database_url(self) -> str:
        """Construct database URL with optimized parameters"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
            
        params = {
            "charset": self.MYSQL.CHARSET,
            "connect_timeout": self.MYSQL.CONNECT_TIMEOUT,
            "local_infile": 1,
            "sql_mode": "STRICT_TRANS_TABLES",
            "client_flag": 65536,  # Enable multiple statements
        }
        
        param_str = "&".join(f"{k}={v}" for k, v in params.items())
        
        return (
            f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?{param_str}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
settings.DATABASE_URL = settings.get_database_url