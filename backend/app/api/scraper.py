"""
Scraper API endpoints
Handles web scraping operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional, Any
from ..services.scraper import search_listings, get_listing_details
from ..api.auth import get_current_user_dependency
from ..models.schemas import User as UserSchema

router = APIRouter(prefix="/scraper", tags=["scraper"])


@router.post("/search")
async def search_olx_listings(
    query: str = Query(..., description="Search query"),
    location: str = Query("", description="Location filter"),
    max_pages: int = Query(3, description="Maximum pages to scrape", ge=1, le=10),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Search for listings on OLX
    
    Args:
        query: Search query (e.g., "iPhone 12")
        location: Location filter (e.g., "Mumbai")
        max_pages: Maximum number of pages to scrape
        current_user: Current authenticated user
        
    Returns:
        List of found listings
    """
    try:
        listings = await search_listings(query, location, max_pages)
        
        return {
            "status": "success",
            "query": query,
            "location": location,
            "listings_found": len(listings),
            "listings": listings
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching listings: {str(e)}")


@router.get("/listing/details")
async def get_listing_details_endpoint(
    url: str = Query(..., description="Listing URL"),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Get detailed information for a specific listing
    
    Args:
        url: Listing URL
        current_user: Current authenticated user
        
    Returns:
        Detailed listing information
    """
    try:
        details = await get_listing_details(url)
        
        if not details:
            raise HTTPException(status_code=404, detail="Listing not found or could not be scraped")
        
        return {
            "status": "success",
            "listing": details
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting listing details: {str(e)}")


@router.post("/search/batch")
async def batch_search_listings(
    queries: List[str] = Query(..., description="List of search queries"),
    location: str = Query("", description="Location filter"),
    max_pages: int = Query(2, description="Maximum pages per query", ge=1, le=5),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Search for multiple queries in batch
    
    Args:
        queries: List of search queries
        location: Location filter
        max_pages: Maximum pages per query
        current_user: Current authenticated user
        
    Returns:
        Results for all queries
    """
    try:
        all_results = {}
        total_listings = 0
        
        for query in queries[:5]:  # Limit to 5 queries
            try:
                listings = await search_listings(query, location, max_pages)
                all_results[query] = {
                    "status": "success",
                    "listings_found": len(listings),
                    "listings": listings
                }
                total_listings += len(listings)
            except Exception as e:
                all_results[query] = {
                    "status": "error",
                    "error": str(e),
                    "listings_found": 0,
                    "listings": []
                }
        
        return {
            "status": "success",
            "queries_processed": len(queries),
            "total_listings_found": total_listings,
            "results": all_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch search: {str(e)}") 