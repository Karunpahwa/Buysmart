from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    requirements = relationship("Requirement", back_populates="user")

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_query = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    budget_min = Column(Integer, nullable=False)
    budget_max = Column(Integer, nullable=False)
    timeline = Column(String(50), nullable=False)
    deal_breakers = Column(JSON, default=list)
    condition_preferences = Column(JSON, default=list)
    scraping_status = Column(String(50), default="pending")
    total_listings_found = Column(Integer, default=0)
    matching_listings_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="requirements") 