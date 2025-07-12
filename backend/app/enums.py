"""
Centralized enums for BuySmart application
"""

from enum import Enum


class Category(str, Enum):
    """Product categories"""
    ELECTRONICS = "electronics"
    VEHICLES = "vehicles"
    PROPERTY = "property"
    FASHION = "fashion"
    HOME_GARDEN = "home_garden"
    SPORTS = "sports"
    BOOKS = "books"
    OTHER = "other"


class RequirementStatus(str, Enum):
    """Requirement status"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ScrapingStatus(str, Enum):
    """Scraping status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Timeline(str, Enum):
    """Timeline options"""
    URGENT = "urgent"
    FLEXIBLE = "flexible"
    LONG_TERM = "long_term"


class ListingStatus(str, Enum):
    """Listing status"""
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
    REMOVED = "removed"


class MessageType(str, Enum):
    """Message types"""
    INQUIRY = "inquiry"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"
    FOLLOW_UP = "follow_up" 