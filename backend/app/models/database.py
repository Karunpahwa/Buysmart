"""
Additional database models
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from ..database import Base
from ..enums import MessageType


class Message(Base):
    __tablename__ = "messages"

    # Use String(36) for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False)
    message_type = Column(SQLEnum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    response_content = Column(Text, nullable=True)
    response_received_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    listing = relationship("Listing", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, type={self.message_type}, listing_id={self.listing_id})>"


class ParsedResponse(Base):
    __tablename__ = "parsed_responses"

    # Use String(36) for SQLite compatibility
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    listing_id = Column(String(36), ForeignKey("listings.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    parsed_data = Column(JSON, nullable=True)
    sentiment = Column(String(50), nullable=True)
    intent = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    listing = relationship("Listing", back_populates="parsed_response")

    def __repr__(self):
        return f"<ParsedResponse(id={self.id}, listing_id={self.listing_id})>" 