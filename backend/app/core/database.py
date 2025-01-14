from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from app.core.config import settings
from typing import Generator
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Advanced MySQL engine configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Connection Pool Settings
    pool_pre_ping=True,          # Enable automatic reconnection
    pool_size=20,                # Maximum number of persistent connections
    max_overflow=10,             # Maximum number of connections that can be created beyond pool_size
    pool_recycle=3600,           # Recycle connections after 1 hour
    pool_timeout=30,             # Timeout for getting connection from pool
    
    # Performance Settings
    pool_use_lifo=True,         # Use LIFO to reduce number of idle connections
    echo=settings.DEBUG,         # SQL logging for debugging
    
    # MySQL Specific Settings
    connect_args={
        "connect_timeout": 60,   # Connection timeout
        "charset": "utf8mb4",    # UTF8MB4 character set
        "use_unicode": True,     
        
        # Performance optimizations
        "pool_reset_session": True,
        "autocommit": False,     # Let SQLAlchemy handle transactions
        
        # Buffer Settings
        "read_buffer_size": 2 * 1024 * 1024,  # 2MB read buffer
        "write_buffer_size": 2 * 1024 * 1024,  # 2MB write buffer
        
        # Timeout Settings
        "read_timeout": 60,      # Read timeout
        "write_timeout": 60      # Write timeout
    }
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Performance optimization
)

Base = declarative_base()

# Query execution time logging
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    if settings.DEBUG:
        logger.debug("Start Query: %s", statement)

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    if settings.DEBUG:
        logger.debug("Query Complete! Time: %f", total)
    if total > 0.5:  # Log slow queries (>500ms)
        logger.warning("Slow Query: %s\nTime: %f", statement, total)

def get_db() -> Generator:
    """Database dependency with connection management and error handling"""
    db = SessionLocal()
    try:
        # Set session configuration for performance
        db.execute("SET SESSION transaction_isolation='READ-COMMITTED'")
        db.execute("SET SESSION innodb_lock_wait_timeout=50")
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

# Connection health check
def check_db_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False
    finally:
        db.close() 