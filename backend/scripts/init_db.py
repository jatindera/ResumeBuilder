import os
import sys
from pathlib import Path

# Add the parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings


def init_database() -> None:
    """Initialize the PostgreSQL database"""
    try:
        # Connect to default 'postgres' database first
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT,
            database="postgres"  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (settings.POSTGRES_DB,),
        )
        exists = cursor.fetchone()
        if not exists:
            print(f"Creating database {settings.POSTGRES_DB}")
            cursor.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print("Database created successfully!")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    init_database()
