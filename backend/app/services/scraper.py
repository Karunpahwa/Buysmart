"""
Scraping service for OLX listings
"""

import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import SessionLocal
from ..models.requirement import Requirement
from ..models.listing import Listing
from ..enums import ScrapingStatus

logger = logging.getLogger(__name__)


async def trigger_scraping_for_requirement(requirement_id: str):
    """
    Trigger scraping for a specific requirement
    
    Args:
        requirement_id: ID of the requirement to scrape for
    """
    db = SessionLocal()
    try:
        # Get requirement
        requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
        if not requirement:
            logger.error(f"Requirement {requirement_id} not found")
            return
        
        # Update scraping status to in_progress
        requirement.update_scraping_status(ScrapingStatus.IN_PROGRESS)
        db.commit()
        
        logger.info(f"Starting scraping for requirement {requirement_id}: {requirement.product_query}")
        
        # Perform scraping
        try:
            listings = await search_listings(requirement.product_query, requirement.category.value)
            
            # Save listings to database
            saved_listings = []
            for listing_data in listings:
                listing = Listing(
                    requirement_id=requirement_id,
                    external_id=listing_data.get("id", ""),
                    title=listing_data.get("title", ""),
                    description=listing_data.get("description", ""),
                    price=listing_data.get("price"),
                    location=listing_data.get("location", ""),
                    seller_name=listing_data.get("seller_name", ""),
                    listing_url=listing_data.get("url", ""),
                    image_urls=listing_data.get("images", [])
                )
                db.add(listing)
                saved_listings.append(listing)
            
            db.commit()
            
            # Update requirement with success status
            requirement.update_scraping_status(ScrapingStatus.COMPLETED, len(saved_listings))
            db.commit()
            
            logger.info(f"Scraping completed for requirement {requirement_id}. Found {len(saved_listings)} listings")
            
        except Exception as e:
            logger.error(f"Scraping failed for requirement {requirement_id}: {e}")
            requirement.update_scraping_status(ScrapingStatus.FAILED)
            db.commit()
            
    except Exception as e:
        logger.error(f"Error in trigger_scraping_for_requirement: {e}")
    finally:
        db.close()


async def search_listings(query: str, category: str) -> List[dict]:
    """
    Search for listings on OLX
    
    Args:
        query: Search query
        category: Product category
        
    Returns:
        List of listing dictionaries
    """
    # Mock implementation - replace with actual OLX scraping
    logger.info(f"Searching for '{query}' in category '{category}'")
    
    # Simulate API delay
    await asyncio.sleep(2)
    
    # Return mock data
    return [
        {
            "id": f"olx_{i}",
            "title": f"{query} - Item {i}",
            "description": f"Description for {query} item {i}",
            "price": 1000 + (i * 100),
            "location": "Mumbai, Maharashtra",
            "seller_name": f"Seller {i}",
            "url": f"https://olx.in/item/{i}",
            "images": [f"https://example.com/image_{i}.jpg"]
        }
        for i in range(1, 6)  # Return 5 mock listings
    ]


async def get_listing_details(listing_id: str) -> Optional[dict]:
    """
    Get detailed information about a specific listing
    
    Args:
        listing_id: OLX listing ID
        
    Returns:
        Listing details dictionary or None
    """
    # Mock implementation
    logger.info(f"Getting details for listing {listing_id}")
    
    await asyncio.sleep(1)
    
    return {
        "id": listing_id,
        "title": f"Detailed listing {listing_id}",
        "description": "Detailed description of the listing",
        "price": 1500,
        "location": "Mumbai, Maharashtra",
        "seller_name": "John Doe",
        "url": f"https://olx.in/item/{listing_id}",
        "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    }


async def schedule_periodic_scraping():
    """
    Schedule periodic scraping for all active requirements
    This should be called by a scheduler (e.g., Celery, APScheduler)
    """
    db = SessionLocal()
    try:
        # Get all active requirements that need scraping
        now = datetime.utcnow()
        requirements = db.query(Requirement).filter(
            Requirement.status == "active",
            Requirement.next_scrape_at <= now
        ).all()
        
        for requirement in requirements:
            await trigger_scraping_for_requirement(requirement.id)
            
    except Exception as e:
        logger.error(f"Error in periodic scraping: {e}")
    finally:
        db.close() 