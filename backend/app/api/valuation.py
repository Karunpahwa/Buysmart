"""
Valuation API endpoints
Handles value estimation and market insights
"""

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from ..services.valuation import estimate_value, compare_values, get_market_insights, batch_valuate_listings
from ..api.auth import get_current_user_dependency
from ..models.schemas import User as UserSchema

router = APIRouter(prefix="/valuation", tags=["valuation"])


class ListingData(BaseModel):
    """Listing data for valuation"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    analysis: Optional[Dict[str, Any]] = None


class ValuationRequest(BaseModel):
    """Request for listing valuation"""
    listings: List[ListingData]


@router.post("/estimate")
async def estimate_listing_value(
    listing: ListingData = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Estimate fair market value for a listing
    
    Args:
        listing: Listing data to valuate
        current_user: Current authenticated user
        
    Returns:
        Valuation analysis
    """
    try:
        listing_dict = listing.dict()
        valuation = await estimate_value(listing_dict)
        
        return {
            "status": "success",
            "valuation": valuation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error estimating value: {str(e)}")


@router.post("/estimate/batch")
async def estimate_multiple_values(
    request: ValuationRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Estimate values for multiple listings in batch
    
    Args:
        request: Request with list of listings to valuate
        current_user: Current authenticated user
        
    Returns:
        List of listings with valuations
    """
    try:
        listings = [listing.dict() for listing in request.listings]
        valuated_listings = await batch_valuate_listings(listings)
        
        return {
            "status": "success",
            "listings_valuated": len(valuated_listings),
            "valuated_listings": valuated_listings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error estimating values: {str(e)}")


@router.post("/compare")
async def compare_listing_values(
    request: ValuationRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Compare values across multiple listings
    
    Args:
        request: Request with list of listings to compare
        current_user: Current authenticated user
        
    Returns:
        Value comparison analysis
    """
    try:
        listings = [listing.dict() for listing in request.listings]
        comparison = await compare_values(listings)
        
        return {
            "status": "success",
            "comparison": comparison
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing values: {str(e)}")


@router.get("/market-insights")
async def get_market_insights_endpoint(
    product_type: str = Query(..., description="Type of product (e.g., 'iPhone', 'laptop')"),
    location: str = Query("", description="Location for market analysis"),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Get market insights for a product type and location
    
    Args:
        product_type: Type of product
        location: Location for analysis
        current_user: Current authenticated user
        
    Returns:
        Market insights and recommendations
    """
    try:
        insights = await get_market_insights(product_type, location)
        
        return {
            "status": "success",
            "product_type": product_type,
            "location": location,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting market insights: {str(e)}")


@router.post("/estimate/url")
async def estimate_value_by_url(
    url: str = Body(..., embed=True),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Estimate value for a listing by URL (combines scraping and valuation)
    
    Args:
        url: Listing URL to valuate
        current_user: Current authenticated user
        
    Returns:
        Valuation analysis
    """
    try:
        from ..services.scraper import get_listing_details
        
        # First get listing details
        listing_data = await get_listing_details(url)
        
        if not listing_data:
            raise HTTPException(status_code=404, detail="Could not fetch listing from URL")
        
        # Then estimate the value
        valuation = await estimate_value(listing_data)
        
        return {
            "status": "success",
            "url": url,
            "valuation": valuation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error estimating value by URL: {str(e)}")


@router.get("/price-history")
async def get_price_history(
    product_type: str = Query(..., description="Type of product"),
    location: str = Query("", description="Location"),
    days: int = Query(30, description="Number of days to analyze", ge=7, le=365),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Get price history and trends for a product type
    
    Args:
        product_type: Type of product
        location: Location for analysis
        days: Number of days to analyze
        current_user: Current authenticated user
        
    Returns:
        Price history and trend analysis
    """
    try:
        # This would typically involve querying historical data
        # For now, we'll return a mock response
        price_history = {
            "product_type": product_type,
            "location": location,
            "analysis_period_days": days,
            "trend": "stable",  # increasing, decreasing, stable
            "average_price": "₹25,000",
            "price_range": {
                "min": "₹20,000",
                "max": "₹35,000"
            },
            "seasonal_factors": ["Holiday season affects prices"],
            "recommendations": [
                "Prices are currently stable",
                "Good time to buy",
                "Consider negotiating 10-15% off listed prices"
            ]
        }
        
        return {
            "status": "success",
            "price_history": price_history
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting price history: {str(e)}") 