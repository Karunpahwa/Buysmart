from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .database import Category, RequirementStatus, RequirementTimeline, ListingStatus, MessageRole


# User schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: Optional[str] = None
    oauth_provider: Optional[str] = None
    oauth_token: Optional[str] = None


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Requirement schemas
class RequirementBase(BaseModel):
    product_query: str
    category: Category
    budget_min: float
    budget_max: float
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    location_radius_km: Optional[float] = None
    deal_breakers: Optional[List[str]] = None
    condition_preferences: Optional[List[str]] = None
    timeline: RequirementTimeline


class RequirementCreate(RequirementBase):
    pass


class RequirementUpdate(BaseModel):
    status: Optional[RequirementStatus] = None
    product_query: Optional[str] = None
    category: Optional[Category] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    location_radius_km: Optional[float] = None
    deal_breakers: Optional[List[str]] = None
    condition_preferences: Optional[List[str]] = None
    timeline: Optional[RequirementTimeline] = None


class Requirement(RequirementBase):
    id: UUID
    user_id: UUID
    status: RequirementStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RequirementOut(RequirementBase):
    id: UUID
    user_id: UUID
    status: RequirementStatus
    total_listings_found: int
    matching_listings_count: int
    last_scraped_at: Optional[datetime]
    next_scrape_at: Optional[datetime]
    scraping_status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Listing schemas
class ListingBase(BaseModel):
    olx_id: str
    title: str
    price: float
    location: str
    posted_date: datetime


class ListingCreate(ListingBase):
    requirement_id: UUID


class ListingUpdate(BaseModel):
    status: Optional[ListingStatus] = None
    title: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None


class Listing(ListingBase):
    id: UUID
    requirement_id: UUID
    status: ListingStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Message schemas
class MessageBase(BaseModel):
    content: str
    role: MessageRole


class MessageCreate(MessageBase):
    listing_id: UUID


class Message(MessageBase):
    id: UUID
    listing_id: UUID
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Parsed Response schemas
class ParsedResponseBase(BaseModel):
    condition: Optional[str] = None
    negotiable: Optional[bool] = None
    bill_available: Optional[bool] = None
    warranty: Optional[str] = None
    notes: Optional[str] = None


class ParsedResponseCreate(ParsedResponseBase):
    listing_id: UUID


class ParsedResponseUpdate(ParsedResponseBase):
    pass


class ParsedResponse(ParsedResponseBase):
    id: UUID
    listing_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# API Response schemas
class RequirementsResponse(BaseModel):
    requirements: List[RequirementOut]
    total: int


class ListingsResponse(BaseModel):
    listings: List[Listing]
    total: int


class MessagesResponse(BaseModel):
    messages: List[Message]
    total: int 