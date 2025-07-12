from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Requirement schemas
class RequirementCreate(BaseModel):
    product_query: str = Field(..., min_length=1, max_length=500)
    category: str = Field(..., min_length=1, max_length=100)
    budget_min: int = Field(..., gt=0)
    budget_max: int = Field(..., gt=0)
    timeline: str = Field(..., min_length=1, max_length=50)
    deal_breakers: List[str] = Field(default_factory=list)
    condition_preferences: List[str] = Field(default_factory=list)

class RequirementOut(BaseModel):
    id: str
    user_id: str
    product_query: str
    category: str
    budget_min: int
    budget_max: int
    timeline: str
    deal_breakers: List[str]
    condition_preferences: List[str]
    scraping_status: str
    total_listings_found: int
    matching_listings_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 