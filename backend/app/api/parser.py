"""
Parser API endpoints
Handles listing analysis and information extraction
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from ..services.parser import analyze_listing, analyze_multiple_listings, extract_key_information, compare_listings
from ..api.auth import get_current_user_dependency
from ..models.schemas import User as UserSchema

router = APIRouter(prefix="/parser", tags=["parser"])


class ListingData(BaseModel):
    """Listing data for analysis"""
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    posted_date: Optional[str] = None


class AnalysisRequest(BaseModel):
    """Request for listing analysis"""
    listings: List[ListingData]


@router.post("/analyze")
async def analyze_single_listing(
    listing: ListingData = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Analyze a single listing
    
    Args:
        listing: Listing data to analyze
        current_user: Current authenticated user
        
    Returns:
        Analyzed listing with insights
    """
    try:
        listing_dict = listing.dict()
        analyzed = await analyze_listing(listing_dict)
        
        return {
            "status": "success",
            "analysis": analyzed
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing listing: {str(e)}")


@router.post("/analyze/batch")
async def analyze_multiple_listings_endpoint(
    request: AnalysisRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Analyze multiple listings in batch
    
    Args:
        request: Request with list of listings to analyze
        current_user: Current authenticated user
        
    Returns:
        List of analyzed listings
    """
    try:
        listings = [listing.dict() for listing in request.listings]
        analyzed_listings = await analyze_multiple_listings(listings)
        
        return {
            "status": "success",
            "listings_analyzed": len(analyzed_listings),
            "analyzed_listings": analyzed_listings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing listings: {str(e)}")


@router.post("/extract")
async def extract_key_information_endpoint(
    listing: ListingData = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Extract key information from a listing
    
    Args:
        listing: Listing data to extract information from
        current_user: Current authenticated user
        
    Returns:
        Extracted key information
    """
    try:
        listing_dict = listing.dict()
        key_info = await extract_key_information(listing_dict)
        
        return {
            "status": "success",
            "key_information": key_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting information: {str(e)}")


@router.post("/compare")
async def compare_listings_endpoint(
    request: AnalysisRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Compare multiple listings
    
    Args:
        request: Request with list of listings to compare
        current_user: Current authenticated user
        
    Returns:
        Comparison analysis
    """
    try:
        listings = [listing.dict() for listing in request.listings]
        comparison = await compare_listings(listings)
        
        return {
            "status": "success",
            "comparison": comparison
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing listings: {str(e)}")


@router.post("/analyze/url")
async def analyze_listing_by_url(
    url: str = Body(..., embed=True),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Analyze a listing by URL (combines scraping and analysis)
    
    Args:
        url: Listing URL to analyze
        current_user: Current authenticated user
        
    Returns:
        Analyzed listing data
    """
    try:
        from ..services.scraper import get_listing_details
        
        # First get listing details
        listing_data = await get_listing_details(url)
        
        if not listing_data:
            raise HTTPException(status_code=404, detail="Could not fetch listing from URL")
        
        # Then analyze the listing
        analyzed = await analyze_listing(listing_data)
        
        return {
            "status": "success",
            "url": url,
            "analysis": analyzed
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing listing by URL: {str(e)}") 