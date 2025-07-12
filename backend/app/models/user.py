"""
User model for authentication and user management
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from ..database import Base


class User(Base):
    __tablename__ = "users"

    # Use String(36) for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    oauth_provider = Column(String(50), nullable=True)
    oauth_token = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    requirements = relationship("Requirement", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>" 