from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.database import Requirement as RequirementModel
import json
from datetime import datetime, timedelta
from ..models.schemas import Requirement, RequirementCreate, RequirementUpdate, RequirementsResponse, RequirementOut
from ..api.auth import get_current_user_dependency
from ..models.database import User

router = APIRouter(prefix="/requirements", tags=["requirements"])


@router.post("/", response_model=RequirementOut)
def create_requirement(
    requirement: RequirementCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Create a new requirement and trigger scraping"""
    from datetime import datetime, timedelta
    
    # Set next scrape time to 24 hours from now
    next_scrape_at = datetime.utcnow() + timedelta(hours=24)
    
    db_requirement = RequirementModel(
        user_id=current_user.id,
        product_query=requirement.product_query,
        category=requirement.category,
        budget_min=requirement.budget_min,
        budget_max=requirement.budget_max,
        location_lat=requirement.location_lat,
        location_lng=requirement.location_lng,
        location_radius_km=requirement.location_radius_km,
        deal_breakers=requirement.deal_breakers or [],
        condition_preferences=requirement.condition_preferences or [],
        timeline=requirement.timeline,
        scraping_status="pending",
        next_scrape_at=next_scrape_at
    )
    db.add(db_requirement)
    db.commit()
    db.refresh(db_requirement)
    
    # Trigger immediate scraping (async)
    try:
        from ..services.scraper import trigger_scraping_for_requirement
        import asyncio
        asyncio.create_task(trigger_scraping_for_requirement(db_requirement.id))
    except Exception as e:
        print(f"Failed to trigger scraping: {e}")
    
    return RequirementOut(
        id=db_requirement.id,
        user_id=db_requirement.user_id,
        product_query=db_requirement.product_query,
        category=db_requirement.category,
        budget_min=db_requirement.budget_min,
        budget_max=db_requirement.budget_max,
        location_lat=db_requirement.location_lat,
        location_lng=db_requirement.location_lng,
        location_radius_km=db_requirement.location_radius_km,
        deal_breakers=db_requirement.deal_breakers,
        condition_preferences=db_requirement.condition_preferences,
        timeline=db_requirement.timeline,
        status=db_requirement.status,
        total_listings_found=db_requirement.total_listings_found,
        matching_listings_count=db_requirement.matching_listings_count,
        last_scraped_at=db_requirement.last_scraped_at,
        next_scrape_at=db_requirement.next_scrape_at,
        scraping_status=db_requirement.scraping_status,
        created_at=db_requirement.created_at,
        updated_at=db_requirement.updated_at
    )


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
    
    requirements_out = [
        RequirementOut(
            id=r.id,
            user_id=r.user_id,
            product_query=r.product_query,
            category=r.category,
            budget_min=r.budget_min,
            budget_max=r.budget_max,
            location_lat=r.location_lat,
            location_lng=r.location_lng,
            location_radius_km=r.location_radius_km,
            deal_breakers=r.deal_breakers,
            condition_preferences=r.condition_preferences,
            timeline=r.timeline,
            status=r.status,
            total_listings_found=r.total_listings_found,
            matching_listings_count=r.matching_listings_count,
            last_scraped_at=r.last_scraped_at,
            next_scrape_at=r.next_scrape_at,
            scraping_status=r.scraping_status,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in requirements
    ]
    return RequirementsResponse(requirements=requirements_out, total=total)


@router.get("/{requirement_id}", response_model=RequirementOut)
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
    
    return RequirementOut(
        id=requirement.id,
        user_id=requirement.user_id,
        product_query=requirement.product_query,
        category=requirement.category,
        budget_min=requirement.budget_min,
        budget_max=requirement.budget_max,
        location_lat=requirement.location_lat,
        location_lng=requirement.location_lng,
        location_radius_km=requirement.location_radius_km,
        deal_breakers=requirement.deal_breakers,
        condition_preferences=requirement.condition_preferences,
        timeline=requirement.timeline,
        status=requirement.status,
        total_listings_found=requirement.total_listings_found,
        matching_listings_count=requirement.matching_listings_count,
        last_scraped_at=requirement.last_scraped_at,
        next_scrape_at=requirement.next_scrape_at,
        scraping_status=requirement.scraping_status,
        created_at=requirement.created_at,
        updated_at=requirement.updated_at
    )


@router.put("/{requirement_id}", response_model=RequirementOut)
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
    
    # If status changed to ACTIVE, trigger scraping
    if requirement_update.status == "active" and db_requirement.scraping_status == "paused":
        db_requirement.scraping_status = "pending"
        db_requirement.next_scrape_at = datetime.utcnow() + timedelta(hours=24)
        try:
            from ..services.scraper import trigger_scraping_for_requirement
            import asyncio
            asyncio.create_task(trigger_scraping_for_requirement(db_requirement.id))
        except Exception as e:
            print(f"Failed to trigger scraping: {e}")
    
    db.commit()
    db.refresh(db_requirement)
    
    return RequirementOut(
        id=db_requirement.id,
        user_id=db_requirement.user_id,
        product_query=db_requirement.product_query,
        category=db_requirement.category,
        budget_min=db_requirement.budget_min,
        budget_max=db_requirement.budget_max,
        location_lat=db_requirement.location_lat,
        location_lng=db_requirement.location_lng,
        location_radius_km=db_requirement.location_radius_km,
        deal_breakers=db_requirement.deal_breakers,
        condition_preferences=db_requirement.condition_preferences,
        timeline=db_requirement.timeline,
        status=db_requirement.status,
        total_listings_found=db_requirement.total_listings_found,
        matching_listings_count=db_requirement.matching_listings_count,
        last_scraped_at=db_requirement.last_scraped_at,
        next_scrape_at=db_requirement.next_scrape_at,
        scraping_status=db_requirement.scraping_status,
        created_at=db_requirement.created_at,
        updated_at=db_requirement.updated_at
    )


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


@router.post("/{requirement_id}/trigger-scraping")
def trigger_scraping(
    requirement_id: str,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Manually trigger scraping for a requirement"""
    db_requirement = db.query(RequirementModel).filter(
        RequirementModel.id == requirement_id,
        RequirementModel.user_id == current_user.id
    ).first()
    
    if not db_requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement not found"
        )
    
    # Update scraping status
    db_requirement.scraping_status = "pending"
    db_requirement.next_scrape_at = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    # Trigger scraping
    try:
        from ..services.scraper import trigger_scraping_for_requirement
        import asyncio
        asyncio.create_task(trigger_scraping_for_requirement(db_requirement.id))
        return {"message": "Scraping triggered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger scraping: {str(e)}"
        ) 