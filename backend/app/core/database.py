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
    pool_pre_ping=True,  # Enable automatic reconnection
    pool_size=settings.POOL_SIZE,  # Maximum number of persistent connections
    max_overflow=settings.MAX_OVERFLOW,  # Maximum number of connections that can be created beyond pool_size
    pool_recycle=settings.POOL_RECYCLE,  # Recycle connections after 1 hour
    pool_timeout=settings.POOL_TIMEOUT,  # Timeout for getting connection from pool
    # PostgreSQL Specific Optimizations
    connect_args={
        "connect_timeout": 60,
        "client_encoding": "utf8",
        "application_name": "resume_builder",
        "keepalives": 1,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 5,
        "sslmode": "prefer",
        "options": "-c statement_timeout=60000 -c idle_in_transaction_session_timeout=60000",  # 60 seconds
    },
    # Query Execution Settings
    execution_options={
        "isolation_level": "READ COMMITTED",
        "postgresql_readonly": False,
        "postgresql_auto_prepares": True,
        "stream_results": True,
    },
    json_serializer=settings.json_serializer,
    json_deserializer=settings.json_deserializer,
)

# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    twophase=False,  # Optimize for single database
)

Base = declarative_base()


# Query execution time logging
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    if settings.DEBUG:
        logger.debug("Start Query: %s", statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop()
    if total > 0.5:  # Log slow queries
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
