"""
Listing model for database operations
"""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, Enum
from datetime import datetime
import uuid
import enum
from ..database import Base

class ListingStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    ELIMINATED = "eliminated"

class Listing(Base):
    __tablename__ = "listings"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    requirement_id = Column(String(36), ForeignKey("requirements.id"), nullable=True)
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