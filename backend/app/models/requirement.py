"""
Requirement model for database operations
"""

from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey, Text
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

class RequirementStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    FULFILLED = "fulfilled"

class RequirementTimeline(str, enum.Enum):
    URGENT = "urgent"
    FLEXIBLE = "flexible"

class Category(str, enum.Enum):
    ELECTRONICS = "electronics"
    HOME_DECOR = "home_decor"
    FURNITURE = "furniture"
    APPAREL = "apparel"

class Requirement(Base):
    __tablename__ = "requirements"
    id = Column(UUID(), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(UUID(), ForeignKey("users.id"), nullable=False)
    product_query = Column(String, nullable=False)
    category = Column(Enum(Category), nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    location_radius_km = Column(Float, nullable=True)
    deal_breakers = Column(Text, nullable=True)
    condition_preferences = Column(Text, nullable=True)
    timeline = Column(Enum(RequirementTimeline), nullable=False)
    status = Column(Enum(RequirementStatus), default=RequirementStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # user = relationship("User", back_populates="requirements") 