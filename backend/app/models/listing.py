"""
Listing model for scraped listings
"""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from sqlalchemy.ext.mutable import MutableList

from ..database import Base
from ..enums import ListingStatus


class Listing(Base):
    __tablename__ = "listings"

    # Use String(36) for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    requirement_id = Column(String(36), ForeignKey("requirements.id"), nullable=False)
    external_id = Column(String(255), nullable=False)  # OLX listing ID
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String(10), default="INR")
    location = Column(String(255), nullable=True)
    seller_name = Column(String(255), nullable=True)
    seller_rating = Column(Float, nullable=True)
    listing_url = Column(String(1000), nullable=False)
    image_urls = Column(MutableList.as_mutable(JSON), nullable=True, default=list)
    condition = Column(String(100), nullable=True)
    status = Column(SQLEnum(ListingStatus), nullable=False, default=ListingStatus.ACTIVE)
    
    # Analysis fields
    relevance_score = Column(Float, nullable=True)
    price_score = Column(Float, nullable=True)
    condition_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    requirement = relationship("Requirement", back_populates="listings")
    messages = relationship("Message", back_populates="listing")
    parsed_response = relationship("ParsedResponse", back_populates="listing", uselist=False)

    def __repr__(self):
        return f"<Listing(id={self.id}, title={self.title}, price={self.price})>" 