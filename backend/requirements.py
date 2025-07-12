from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database import get_db
from models import User, Requirement
from schemas import RequirementCreate, RequirementOut
from auth import get_current_user

router = APIRouter()

@router.post("/", response_model=RequirementOut)
def create_requirement(
    requirement: RequirementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate budget range
    if requirement.budget_min > requirement.budget_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="budget_min cannot be greater than budget_max"
        )
    
    # Create requirement
    db_requirement = Requirement(
        user_id=current_user.id,
        product_query=requirement.product_query,
        category=requirement.category,
        budget_min=requirement.budget_min,
        budget_max=requirement.budget_max,
        timeline=requirement.timeline,
        deal_breakers=requirement.deal_breakers,
        condition_preferences=requirement.condition_preferences
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement

@router.get("/{requirement_id}", response_model=RequirementOut)
def get_requirement(
    requirement_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a single requirement by ID for the current user"""
    requirement = db.query(Requirement).filter(
        Requirement.id == requirement_id,
        Requirement.user_id == current_user.id
    ).first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    return requirement

@router.get("/", response_model=List[RequirementOut])
def list_requirements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all requirements for the current user"""
    requirements = db.query(Requirement).filter(
        Requirement.user_id == current_user.id
    ).order_by(Requirement.created_at.desc()).all()
    return requirements 