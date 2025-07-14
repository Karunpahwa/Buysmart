"""
Requirements API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from sqlalchemy.exc import SQLAlchemyError
import logging

from ..database import get_db
from ..models.requirement import Requirement
from ..models.schemas import RequirementCreate, RequirementOut, RequirementUpdate
from ..enums import ScrapingStatus
from ..models.user import User

router = APIRouter()

# Mock user for development
mock_user = User(id=str(uuid.uuid4()), email="test@example.com", password_hash="test")


@router.post("/", response_model=RequirementOut)
def create_requirement(
    requirement: RequirementCreate,
    db: Session = Depends(get_db)
):
    """Create a new requirement"""
    try:
        db_requirement = Requirement(
            user_id=mock_user.id,
            **requirement.dict()
        )
        db.add(db_requirement)
        db.commit()
        db.refresh(db_requirement)
        return db_requirement
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"DB error creating requirement: {e}")
        raise HTTPException(status_code=500, detail="Database error creating requirement.")
    except Exception as e:
        logging.error(f"Validation or unknown error: {e}")
        raise HTTPException(status_code=422, detail=f"Validation error: {e}")


@router.get("/", response_model=List[RequirementOut])
def get_requirements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all requirements for the current user"""
    requirements = db.query(Requirement).filter(
        Requirement.user_id == mock_user.id
    ).offset(skip).limit(limit).all()
    return requirements


@router.get("/{requirement_id}", response_model=RequirementOut)
def get_requirement(
    requirement_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific requirement by ID"""
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id,
        Requirement.user_id == mock_user.id
    ).first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    return requirement


@router.put("/{requirement_id}", response_model=RequirementOut)
def update_requirement(
    requirement_id: str,
    requirement_update: RequirementUpdate,
    db: Session = Depends(get_db)
):
    """Update a requirement"""
    db_requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id,
        Requirement.user_id == mock_user.id
    ).first()
    
    if not db_requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    update_data = requirement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_requirement, field, value)
    
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


@router.delete("/{requirement_id}")
def delete_requirement(
    requirement_id: str,
    db: Session = Depends(get_db)
):
    """Delete a requirement"""
    db_requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id,
        Requirement.user_id == mock_user.id
    ).first()
    
    if not db_requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    db.delete(db_requirement)
    db.commit()
    return {"message": "Requirement deleted successfully"}


@router.get("/{requirement_id}/listings")
def get_requirement_listings(
    requirement_id: str,
    db: Session = Depends(get_db)
):
    """Get all listings for a specific requirement"""
    # First verify the requirement belongs to the user
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id,
        Requirement.user_id == mock_user.id
    ).first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    # Get listings for this requirement
    from ..models.listing import Listing
    listings = db.query(Listing).filter(
        Listing.requirement_id == requirement_id
    ).all()
    
    return {
        "requirement_id": requirement_id,
        "listings": listings,
        "total": len(listings)
    } 