"""
Scraper Service for OLX India
Handles web scraping using Playwright
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from playwright.async_api import async_playwright, Browser, Page
from ..models.database import Listing, Requirement
from ..database import get_db, SessionLocal

logger = logging.getLogger(__name__)


class ScraperService:
    """Service for scraping OLX listings"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()
    
    async def search_listings(self, query: str, location: str = "", max_pages: int = 3) -> List[Dict]:
        """
        Search for listings on OLX based on query and location
        
        Args:
            query: Search query (e.g., "iPhone 12")
            location: Location filter (e.g., "Mumbai")
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of listing data dictionaries
        """
        try:
            listings = []
            
            # Construct search URL
            search_url = f"https://www.olx.in/items/q-{query.replace(' ', '-')}"
            if location:
                search_url += f"-in-{location.replace(' ', '-')}"
            
            logger.info(f"Searching OLX: {search_url}")
            
            # Navigate to search page
            await self.page.goto(search_url, wait_until="networkidle")
            
            # Handle cookie consent if present
            try:
                cookie_button = await self.page.wait_for_selector('[data-testid="cookie-banner-accept"]', timeout=5000)
                if cookie_button:
                    await cookie_button.click()
            except:
                pass  # No cookie banner
            
            for page_num in range(1, max_pages + 1):
                logger.info(f"Scraping page {page_num}")
                
                # Wait for listings to load
                await self.page.wait_for_selector('[data-testid="listing-grid"]', timeout=10000)
                
                # Extract listing data
                page_listings = await self._extract_listings_from_page()
                listings.extend(page_listings)
                
                # Try to go to next page
                if page_num < max_pages:
                    try:
                        next_button = await self.page.query_selector('[data-testid="pagination-forward"]')
                        if next_button and await next_button.is_enabled():
                            await next_button.click()
                            await self.page.wait_for_load_state("networkidle")
                        else:
                            break  # No more pages
                    except:
                        break  # Error going to next page
            
            logger.info(f"Found {len(listings)} listings")
            return listings
            
        except Exception as e:
            logger.error(f"Error scraping listings: {e}")
            return []
    
    async def _extract_listings_from_page(self) -> List[Dict]:
        """Extract listing data from current page"""
        listings = []
        
        try:
            # Find all listing cards
            listing_cards = await self.page.query_selector_all('[data-testid="listing-card"]')
            
            for card in listing_cards:
                try:
                    # Extract listing data
                    listing_data = await self._extract_listing_data(card)
                    if listing_data:
                        listings.append(listing_data)
                except Exception as e:
                    logger.warning(f"Error extracting listing data: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Error extracting listings from page: {e}")
        
        return listings
    
    async def _extract_listing_data(self, card) -> Optional[Dict]:
        """Extract data from a single listing card"""
        try:
            # Extract title
            title_elem = await card.query_selector('[data-testid="ad-title"]')
            title = await title_elem.text_content() if title_elem else ""
            
            # Extract price
            price_elem = await card.query_selector('[data-testid="ad-price"]')
            price_text = await price_elem.text_content() if price_elem else ""
            price = self._extract_price(price_text)
            
            # Extract location
            location_elem = await card.query_selector('[data-testid="location-text"]')
            location = await location_elem.text_content() if location_elem else ""
            
            # Extract URL
            link_elem = await card.query_selector('a[href*="/item/"]')
            url = await link_elem.get_attribute("href") if link_elem else ""
            if url and not url.startswith("http"):
                url = f"https://www.olx.in{url}"
            
            # Extract image
            img_elem = await card.query_selector('img')
            image_url = await img_elem.get_attribute("src") if img_elem else ""
            
            # Extract posted date
            date_elem = await card.query_selector('[data-testid="date-text"]')
            posted_date = await date_elem.text_content() if date_elem else ""
            
            return {
                "title": title.strip() if title else "",
                "price": price,
                "location": location.strip() if location else "",
                "url": url,
                "image_url": image_url,
                "posted_date": posted_date.strip() if posted_date else "",
                "source": "olx",
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"Error extracting listing data: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from price text"""
        if not price_text:
            return None
        
        try:
            # Remove currency symbols and commas
            price_clean = price_text.replace("₹", "").replace(",", "").replace(" ", "")
            
            # Extract first number
            import re
            numbers = re.findall(r'\d+', price_clean)
            if numbers:
                return float(numbers[0])
            
            return None
        except:
            return None
    
    async def get_listing_details(self, url: str) -> Optional[Dict]:
        """
        Get detailed information for a specific listing
        
        Args:
            url: Listing URL
            
        Returns:
            Detailed listing data or None
        """
        try:
            await self.page.goto(url, wait_until="networkidle")
            
            # Extract detailed information
            details = {}
            
            # Title
            title_elem = await self.page.query_selector('[data-testid="ad-title"]')
            if title_elem:
                details["title"] = await title_elem.text_content()
            
            # Price
            price_elem = await self.page.query_selector('[data-testid="ad-price"]')
            if price_elem:
                price_text = await price_elem.text_content()
                details["price"] = self._extract_price(price_text)
            
            # Description
            desc_elem = await self.page.query_selector('[data-testid="ad-description"]')
            if desc_elem:
                details["description"] = await desc_elem.text_content()
            
            # Seller info
            seller_elem = await self.page.query_selector('[data-testid="seller-name"]')
            if seller_elem:
                details["seller"] = await seller_elem.text_content()
            
            # Images
            img_elems = await self.page.query_selector_all('[data-testid="ad-image"] img')
            details["images"] = []
            for img in img_elems:
                src = await img.get_attribute("src")
                if src:
                    details["images"].append(src)
            
            # Attributes
            attr_elems = await self.page.query_selector_all('[data-testid="ad-attribute"]')
            details["attributes"] = {}
            for attr in attr_elems:
                try:
                    label_elem = await attr.query_selector('[data-testid="attribute-label"]')
                    value_elem = await attr.query_selector('[data-testid="attribute-value"]')
                    if label_elem and value_elem:
                        label = await label_elem.text_content()
                        value = await value_elem.text_content()
                        details["attributes"][label.strip()] = value.strip()
                except:
                    continue
            
            details["url"] = url
            details["source"] = "olx"
            details["scraped_at"] = datetime.utcnow().isoformat()
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting listing details: {e}")
            return None


# Global scraper service instance
scraper_service = ScraperService()


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
        
        # Update scraping status
        requirement.scraping_status = "in_progress"
        requirement.last_scraped_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Starting scraping for requirement {requirement_id}: {requirement.product_query}")
        
        # Perform scraping
        async with scraper_service as scraper:
            # Determine location for search
            location = ""
            if requirement.location_lat and requirement.location_lng:
                # You could implement reverse geocoding here
                location = "Mumbai"  # Default for now
            
            # Search for listings
            listings_data = await scraper.search_listings(
                query=requirement.product_query,
                location=location,
                max_pages=3
            )
            
            # Filter listings based on budget and preferences
            matching_listings = []
            for listing in listings_data:
                if _is_listing_matching_requirement(listing, requirement):
                    matching_listings.append(listing)
            
            # Save listings to database
            saved_count = 0
            for listing_data in matching_listings:
                try:
                    # Check if listing already exists
                    existing = db.query(Listing).filter(
                        Listing.olx_id == listing_data.get("olx_id", ""),
                        Listing.requirement_id == requirement_id
                    ).first()
                    
                    if not existing:
                        db_listing = Listing(
                            requirement_id=requirement_id,
                            olx_id=listing_data.get("olx_id", ""),
                            title=listing_data.get("title", ""),
                            price=listing_data.get("price", 0),
                            location=listing_data.get("location", ""),
                            posted_date=datetime.utcnow(),  # You could parse the actual date
                            status="active"
                        )
                        db.add(db_listing)
                        saved_count += 1
                        
                except Exception as e:
                    logger.error(f"Error saving listing: {e}")
                    continue
            
            # Update requirement with results
            requirement.total_listings_found = len(listings_data)
            requirement.matching_listings_count = len(matching_listings)
            requirement.scraping_status = "completed"
            requirement.last_scraped_at = datetime.utcnow()
            requirement.next_scrape_at = datetime.utcnow() + timedelta(hours=24)
            
            db.commit()
            
            logger.info(f"Scraping completed for requirement {requirement_id}: "
                       f"Found {len(listings_data)} listings, "
                       f"Saved {saved_count} matching listings")
            
    except Exception as e:
        logger.error(f"Error during scraping for requirement {requirement_id}: {e}")
        # Update requirement status to failed
        try:
            requirement.scraping_status = "failed"
            db.commit()
        except:
            pass
    finally:
        db.close()


def _is_listing_matching_requirement(listing: Dict, requirement: Requirement) -> bool:
    """
    Check if a listing matches the requirement criteria
    
    Args:
        listing: Listing data dictionary
        requirement: Requirement object
        
    Returns:
        True if listing matches requirement criteria
    """
    try:
        # Check price range
        price = listing.get("price", 0)
        if price < requirement.budget_min or price > requirement.budget_max:
            return False
        
        # Check location (if requirement has location constraints)
        if requirement.location_radius_km and requirement.location_lat and requirement.location_lng:
            # You could implement distance calculation here
            pass
        
        # Check deal breakers
        if requirement.deal_breakers:
            title_lower = listing.get("title", "").lower()
            for deal_breaker in requirement.deal_breakers:
                if deal_breaker.lower() in title_lower:
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking listing match: {e}")
        return False


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

# Standalone functions for API compatibility
async def search_listings(query: str, location: str = "", max_pages: int = 3) -> List[Dict]:
    """Standalone function to search listings"""
    async with ScraperService() as scraper:
        return await scraper.search_listings(query, location, max_pages)

async def get_listing_details(url: str) -> Optional[Dict]:
    """Standalone function to get listing details"""
    async with ScraperService() as scraper:
        return await scraper.get_listing_details(url) 