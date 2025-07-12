"""
User model for database operations
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import os

# Check if we're using SQLite (for development) or PostgreSQL (for production)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
IS_SQLITE = "sqlite" in DATABASE_URL

# Conditional import for UUID support
if IS_SQLITE:
    # Custom UUID type for SQLite that converts to string
    class SQLiteUUID(String):
        def __init__(self, length=36):
            super().__init__(length)
        
        def process_bind_param(self, value, dialect):
            if value is not None:
                return str(value)
            return value
        
        def process_result_value(self, value, dialect):
            if value is not None:
                return uuid.UUID(value)
            return value
    
    UUID = SQLiteUUID
else:
    # For PostgreSQL, use proper UUID columns
    from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)
    oauth_provider = Column(String, nullable=True)
    oauth_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # requirements = relationship("Requirement", back_populates="user") 