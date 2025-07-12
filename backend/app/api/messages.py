from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.database import Message as MessageModel
from ..models.listing import Listing as ListingModel
from ..models.requirement import Requirement as RequirementModel
from ..models.user import User
from ..models.schemas import MessageOut, MessageCreate, MessagesResponse
from ..api.auth import get_current_user_dependency

router = APIRouter(prefix="/message", tags=["messages"])

@router.post("/send", response_model=MessageOut)
def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Send a message to a seller for a specific listing"""
    # Verify the listing exists and user owns the requirement
    listing = db.query(ListingModel).filter(ListingModel.id == message.listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == listing.requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized to send message for this listing")
    
    # Create the message
    db_message = MessageModel(
        listing_id=message.listing_id,
        role=message.role,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/history/{listing_id}", response_model=MessagesResponse)
def get_message_history(
    listing_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get conversation history for a specific listing"""
    # Verify the listing exists and user owns the requirement
    listing = db.query(ListingModel).filter(ListingModel.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == listing.requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    if not requirement:
        raise HTTPException(status_code=403, detail="Not authorized to view messages for this listing")
    
    # Get all messages for this listing, ordered by timestamp
    messages = db.query(MessageModel).filter(
        MessageModel.listing_id == listing_id
    ).order_by(MessageModel.timestamp).all()
    
    total = db.query(MessageModel).filter(MessageModel.listing_id == listing_id).count()
    
    return MessagesResponse(messages=messages, total=total)

@router.get("/history", response_model=MessagesResponse)
def get_all_messages(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all messages for all listings owned by the current user"""
    # Get all requirements for the user
    user_requirements = db.query(RequirementModel).filter(
        RequirementModel.user_id == current_user.id
    ).all()
    
    requirement_ids = [req.id for req in user_requirements]
    
    # Get all listings for these requirements
    user_listings = db.query(ListingModel).filter(
        ListingModel.requirement_id.in_(requirement_ids)
    ).all()
    
    listing_ids = [listing.id for listing in user_listings]
    
    # Get all messages for these listings
    messages = db.query(MessageModel).filter(
        MessageModel.listing_id.in_(listing_ids)
    ).order_by(MessageModel.timestamp.desc()).offset(skip).limit(limit).all()
    
    total = db.query(MessageModel).filter(
        MessageModel.listing_id.in_(listing_ids)
    ).count()
    
    return MessagesResponse(messages=messages, total=total) 