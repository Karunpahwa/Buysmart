from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.listing import Listing as ListingModel
from ..models.requirement import Requirement as RequirementModel
from ..models.schemas import ListingOut, ListingCreate, ListingUpdate, ListingsResponse
from ..models.user import User
import uuid

router = APIRouter(prefix="/listings", tags=["listings"])

# Mock user for development
mock_user = User(id=str(uuid.uuid4()), email="test@example.com", password_hash="test")

@router.get("/{requirement_id}", response_model=ListingsResponse)
def get_listings_for_requirement(
    requirement_id: str,
    db: Session = Depends(get_db)
):
    """Fetch all listings for a given requirement"""
    # Ensure requirement belongs to user
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id,
        RequirementModel.user_id == mock_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    listings = db.query(ListingModel).filter(ListingModel.requirement_id == requirement_id).all()
    total = db.query(ListingModel).filter(ListingModel.requirement_id == requirement_id).count()
    return ListingsResponse(listings=listings, total=total)

@router.get("/item/{listing_id}", response_model=ListingOut)
def get_listing(
    listing_id: str,
    db: Session = Depends(get_db)
):
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    # Check user owns the requirement
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == listing.requirement_id,
        RequirementModel.user_id == mock_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized")
    return listing

@router.post("/", response_model=ListingOut)
def create_listing(
    listing: ListingCreate,
    db: Session = Depends(get_db)
):
    # Convert UUID to string for SQLite compatibility
    requirement_id_str = str(listing.requirement_id)
    # Check user owns the requirement
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id_str,
        RequirementModel.user_id == mock_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized to add listing to this requirement")
    # Create listing with string requirement_id
    listing_dict = listing.model_dump()
    listing_dict["requirement_id"] = requirement_id_str
    db_listing = ListingModel(**listing_dict)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.patch("/item/{listing_id}", response_model=ListingOut)
def update_listing(
    listing_id: str,
    listing_update: ListingUpdate,
    db: Session = Depends(get_db)
):
    db_listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    # Check user owns the requirement
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == db_listing.requirement_id,
        RequirementModel.user_id == mock_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = listing_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_listing, field, value)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.delete("/item/{listing_id}")
def delete_listing(
    listing_id: str,
    db: Session = Depends(get_db)
):
    db_listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    # Check user owns the requirement
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == db_listing.requirement_id,
        RequirementModel.user_id == mock_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_listing)
    db.commit()
    return {"message": "Listing deleted successfully"} 