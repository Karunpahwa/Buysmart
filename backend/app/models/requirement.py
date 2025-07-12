"""
Requirement model for database operations
"""

from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey, Text, Integer, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
import json

from ..database import Base

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
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_query = Column(String, nullable=False)
    category = Column(Enum(Category), nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    location_radius_km = Column(Float, nullable=True)
    deal_breakers = Column(JSON, nullable=True, default=list)
    condition_preferences = Column(JSON, nullable=True, default=list)
    timeline = Column(Enum(RequirementTimeline), nullable=False)
    status = Column(Enum(RequirementStatus), default=RequirementStatus.ACTIVE)
    
    # Progress tracking fields
    total_listings_found = Column(Integer, default=0)
    matching_listings_count = Column(Integer, default=0)
    last_scraped_at = Column(DateTime, nullable=True)
    next_scrape_at = Column(DateTime, nullable=True)
    scraping_status = Column(String, default="pending")  # pending, in_progress, completed, failed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 