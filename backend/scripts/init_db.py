import mysql.connector
from app.core.config import settings

def init_database() -> None:
    """Initialize the database and create tables"""
    # Create database if it doesn't exist
    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()

    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
    cursor.execute(f"USE {settings.DB_NAME}")

    # Create tables (optional - SQLAlchemy can handle this)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_database() 