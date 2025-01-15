from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from urllib.parse import quote_plus
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    # Create database URL with encoded password
    encoded_password = quote_plus(settings.POSTGRES_PASSWORD)
    DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{encoded_password}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
    
    # Create engine
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Enable connection health checks
        echo=settings.DEBUG  # SQL logging if in debug mode
    )
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    logger.info("Database connection established successfully")

except Exception as e:
    logger.error(f"Database connection error: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 