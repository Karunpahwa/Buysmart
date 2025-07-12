from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.database import Requirement as RequirementModel
from ..models.schemas import Requirement, RequirementCreate, RequirementUpdate, RequirementsResponse
from ..api.auth import get_current_user_dependency
from ..models.database import User

router = APIRouter(prefix="/requirements", tags=["requirements"])


@router.post("/", response_model=Requirement)
def create_requirement(
    requirement: RequirementCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Create a new requirement"""
    db_requirement = RequirementModel(
        user_id=current_user.id,
        product_query=requirement.product_query,
        category=requirement.category,
        budget_min=requirement.budget_min,
        budget_max=requirement.budget_max,
        location_lat=requirement.location_lat,
        location_lng=requirement.location_lng,
        location_radius_km=requirement.location_radius_km,
        deal_breakers=requirement.deal_breakers,
        condition_preferences=requirement.condition_preferences,
        timeline=requirement.timeline
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


@router.get("/", response_model=RequirementsResponse)
def get_requirements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get all requirements for the current user"""
    requirements = db.query(RequirementModel).filter(
        RequirementModel.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    total = db.query(RequirementModel).filter(
        RequirementModel.user_id == current_user.id
    ).count()
    
    return RequirementsResponse(requirements=requirements, total=total)


@router.get("/{requirement_id}", response_model=Requirement)
def get_requirement(
    requirement_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get a specific requirement by ID"""
    requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    return requirement


@router.patch("/{requirement_id}", response_model=Requirement)
def update_requirement(
    requirement_id: str,
    requirement_update: RequirementUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Update a requirement"""
    db_requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    
    if not db_requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    # Update only provided fields
    update_data = requirement_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_requirement, field, value)
    
    db.commit()
    db.refresh(db_requirement)
    return db_requirement


@router.delete("/{requirement_id}")
def delete_requirement(
    requirement_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Delete a requirement"""
    db_requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    
    if not db_requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    db.delete(db_requirement)
    db.commit()
    return {"message": "Requirement deleted successfully"} 