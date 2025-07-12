"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional, List
from datetime import datetime
import json

from ..enums import Category, RequirementStatus, ScrapingStatus, Timeline, ListingStatus, MessageType


# User schemas
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Requirement schemas
class RequirementBase(BaseModel):
    product_query: str
    category: Category
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    timeline: Timeline = Timeline.FLEXIBLE
    deal_breakers: List[str] = Field(default_factory=list)
    condition_preferences: List[str] = Field(default_factory=list)

    @field_validator("deal_breakers", mode="before")
    @classmethod
    def coerce_deal_breakers(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return []
        return v

    @field_validator("condition_preferences", mode="before")
    @classmethod
    def coerce_condition_preferences(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return []
        return v


class RequirementCreate(RequirementBase):
    pass


class RequirementUpdate(BaseModel):
    product_query: Optional[str] = None
    category: Optional[Category] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    timeline: Optional[Timeline] = None
    deal_breakers: Optional[List[str]] = None
    condition_preferences: Optional[List[str]] = None
    status: Optional[RequirementStatus] = None


class RequirementOut(RequirementBase):
    id: str
    user_id: str
    status: RequirementStatus
    scraping_status: ScrapingStatus
    last_scraped_at: Optional[datetime] = None
    next_scrape_at: Optional[datetime] = None
    total_listings_found: int = 0
    matching_listings_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Listing schemas
class ListingBase(BaseModel):
    external_id: str
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "INR"
    location: Optional[str] = None
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    listing_url: str
    image_urls: List[str] = Field(default_factory=list)
    condition: Optional[str] = None

    @validator('image_urls', pre=True)
    def ensure_image_urls_list(cls, v):
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except Exception:
                pass
            return []
        return v


class ListingCreate(ListingBase):
    requirement_id: str


class ListingOut(ListingBase):
    id: str
    requirement_id: str
    status: ListingStatus
    relevance_score: Optional[float] = None
    price_score: Optional[float] = None
    condition_score: Optional[float] = None
    overall_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ListingUpdate(BaseModel):
    external_id: str = None
    title: str = None
    description: str = None
    price: float = None
    currency: str = None
    location: str = None
    seller_name: str = None
    seller_rating: float = None
    listing_url: str = None
    image_urls: list = None
    condition: str = None
    status: ListingStatus = None
    relevance_score: float = None
    price_score: float = None
    condition_score: float = None
    overall_score: float = None

class ListingsResponse(BaseModel):
    listings: list[ListingOut]
    total: int


# Message schemas
class MessageBase(BaseModel):
    listing_id: str
    message_type: MessageType
    content: str


class MessageCreate(MessageBase):
    pass


class MessageOut(MessageBase):
    id: str
    response_content: Optional[str] = None
    response_received_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessagesResponse(BaseModel):
    messages: list[MessageOut]
    total: int


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# API Response schemas
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime 