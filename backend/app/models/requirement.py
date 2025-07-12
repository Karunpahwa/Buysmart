"""
Requirement model for user requirements
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import uuid
from sqlalchemy.ext.mutable import MutableList

from ..database import Base
from ..enums import Category, RequirementStatus, ScrapingStatus, Timeline


class Requirement(Base):
    __tablename__ = "requirements"

    # Use String(36) for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_query = Column(String(500), nullable=False)
    category = Column(SQLEnum(Category), nullable=False)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    timeline = Column(SQLEnum(Timeline), nullable=False, default=Timeline.FLEXIBLE)
    deal_breakers = Column(MutableList.as_mutable(JSON), default=list)
    condition_preferences = Column(MutableList.as_mutable(JSON), default=list)
    status = Column(SQLEnum(RequirementStatus), nullable=False, default=RequirementStatus.ACTIVE)
    
    # Scraping fields
    scraping_status = Column(SQLEnum(ScrapingStatus), nullable=False, default=ScrapingStatus.PENDING)
    last_scraped_at = Column(DateTime, nullable=True)
    next_scrape_at = Column(DateTime, nullable=True)
    total_listings_found = Column(Integer, default=0)
    matching_listings_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="requirements")
    listings = relationship("Listing", back_populates="requirement")

    def __repr__(self):
        return f"<Requirement(id={self.id}, product_query={self.product_query}, status={self.status})>"

    def update_scraping_status(self, status: ScrapingStatus, listings_count: int = None):
        """Update scraping status and related fields"""
        self.scraping_status = status
        self.last_scraped_at = datetime.utcnow()
        
        if status == ScrapingStatus.COMPLETED and listings_count is not None:
            self.matching_listings_count = listings_count
            # Set next scrape time (e.g., 24 hours later)
            self.next_scrape_at = datetime.utcnow() + timedelta(hours=24)
        elif status == ScrapingStatus.FAILED:
            # Retry in 1 hour on failure
            self.next_scrape_at = datetime.utcnow() + timedelta(hours=1) 