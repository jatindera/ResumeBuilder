from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    google_id = Column(String, unique=True)
    picture = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
