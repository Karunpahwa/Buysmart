"""
Listing model for database operations
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid
import enum
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


class ListingStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    ELIMINATED = "eliminated"


class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(UUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    requirement_id = Column(UUID(), ForeignKey("requirements.id"), nullable=True)
    olx_id = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    source = Column(String, default="olx")
    status = Column(Enum(ListingStatus), default=ListingStatus.NEW)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 