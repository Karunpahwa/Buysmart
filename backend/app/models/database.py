from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Enum, JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
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


class ListingStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    ELIMINATED = "eliminated"


class MessageRole(str, enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=True)  # Null for OAuth users
    oauth_provider = Column(String, nullable=True)
    oauth_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requirements = relationship("Requirement", back_populates="user")


class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_query = Column(String, nullable=False)
    category = Column(Enum(Category, values_callable=lambda x: [e.value for e in x]), nullable=False)
    budget_min = Column(Float, nullable=False)
    budget_max = Column(Float, nullable=False)
    location_lat = Column(Float, nullable=True)
    location_lng = Column(Float, nullable=True)
    location_radius_km = Column(Float, nullable=True)
    deal_breakers = Column(JSON, nullable=True, default=list)
    condition_preferences = Column(JSON, nullable=True, default=list)
    timeline = Column(Enum(RequirementTimeline, values_callable=lambda x: [e.value for e in x]), nullable=False)
    status = Column(Enum(RequirementStatus, values_callable=lambda x: [e.value for e in x]), default=RequirementStatus.ACTIVE.value)
    
    # Progress tracking fields
    total_listings_found = Column(Integer, default=0)
    matching_listings_count = Column(Integer, default=0)
    last_scraped_at = Column(DateTime, nullable=True)
    next_scrape_at = Column(DateTime, nullable=True)
    scraping_status = Column(String, default="pending")  # pending, in_progress, completed, failed
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="requirements")
    listings = relationship("Listing", back_populates="requirement")


class Listing(Base):
    __tablename__ = "listings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    requirement_id = Column(String(36), ForeignKey("requirements.id"), nullable=True)
    olx_id = Column(String, unique=True, nullable=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    posted_date = Column(DateTime, nullable=True)
    status = Column(Enum(ListingStatus, values_callable=lambda x: [e.value for e in x]), default=ListingStatus.NEW.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requirement = relationship("Requirement", back_populates="listings")
    messages = relationship("Message", back_populates="listing")
    parsed_response = relationship("ParsedResponse", back_populates="listing", uselist=False)


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False)
    role = Column(Enum(MessageRole, values_callable=lambda x: [e.value for e in x]), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    listing = relationship("Listing", back_populates="messages")


class ParsedResponse(Base):
    __tablename__ = "parsed_responses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False)
    condition = Column(String, nullable=True)
    negotiable = Column(Boolean, nullable=True)
    bill_available = Column(Boolean, nullable=True)
    warranty = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    listing = relationship("Listing", back_populates="parsed_response") 