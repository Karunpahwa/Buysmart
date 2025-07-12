"""
Scheduler Service for background tasks
Handles task scheduling and execution using Redis Queue
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json
from rq import Queue
from redis import Redis
from ..config.settings import settings
from ..services.scraper import search_listings, get_listing_details
from ..services.parser import analyze_multiple_listings, compare_listings
from ..services.valuation import batch_valuate_listings, get_market_insights
from ..database import get_db
from ..models.requirement import Requirement
from ..models.listing import Listing

logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_conn = Redis.from_url(settings.redis_url)
task_queue = Queue('buysmart_tasks', connection=redis_conn)


class SchedulerService:
    """Service for scheduling and managing background tasks"""
    
    def __init__(self):
        self.redis = redis_conn
        self.queue = task_queue
    
    async def schedule_search_task(self, requirement_id: str, user_id: str) -> str:
        """
        Schedule a search task for a requirement
        
        Args:
            requirement_id: ID of the requirement
            user_id: ID of the user
            
        Returns:
            Task ID
        """
        try:
            # Get requirement details
            db = get_db()
            requirement = db.query(Requirement).filter(Requirement.id == requirement_id).first()
            
            if not requirement:
                raise ValueError("Requirement not found")
            
            # Create task data
            task_data = {
                "type": "search_listings",
                "requirement_id": requirement_id,
                "user_id": user_id,
                "query": requirement.product_name,
                "location": requirement.location,
                "max_price": requirement.max_price,
                "min_price": requirement.min_price,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Schedule task
            job = self.queue.enqueue(
                self._execute_search_task,
                task_data,
                job_timeout='10m',
                result_ttl=3600  # Keep results for 1 hour
            )
            
            logger.info(f"Scheduled search task {job.id} for requirement {requirement_id}")
            return job.id
            
        except Exception as e:
            logger.error(f"Error scheduling search task: {e}")
            raise
    
    async def schedule_analysis_task(self, listing_ids: List[str], user_id: str) -> str:
        """
        Schedule an analysis task for listings
        
        Args:
            listing_ids: List of listing IDs to analyze
            user_id: ID of the user
            
        Returns:
            Task ID
        """
        try:
            task_data = {
                "type": "analyze_listings",
                "listing_ids": listing_ids,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
            
            job = self.queue.enqueue(
                self._execute_analysis_task,
                task_data,
                job_timeout='15m',
                result_ttl=3600
            )
            
            logger.info(f"Scheduled analysis task {job.id} for {len(listing_ids)} listings")
            return job.id
            
        except Exception as e:
            logger.error(f"Error scheduling analysis task: {e}")
            raise
    
    async def schedule_valuation_task(self, listing_ids: List[str], user_id: str) -> str:
        """
        Schedule a valuation task for listings
        
        Args:
            listing_ids: List of listing IDs to valuate
            user_id: ID of the user
            
        Returns:
            Task ID
        """
        try:
            task_data = {
                "type": "valuate_listings",
                "listing_ids": listing_ids,
                "user_id": user_id,
                "created_at": datetime.utcnow().isoformat()
            }
            
            job = self.queue.enqueue(
                self._execute_valuation_task,
                task_data,
                job_timeout='20m',
                result_ttl=3600
            )
            
            logger.info(f"Scheduled valuation task {job.id} for {len(listing_ids)} listings")
            return job.id
            
        except Exception as e:
            logger.error(f"Error scheduling valuation task: {e}")
            raise
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get status of a scheduled task
        
        Args:
            task_id: Task ID
            
        Returns:
            Task status information
        """
        try:
            job = self.queue.fetch_job(task_id)
            
            if not job:
                return {"status": "not_found"}
            
            status = {
                "task_id": task_id,
                "status": job.get_status(),
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "ended_at": job.ended_at.isoformat() if job.ended_at else None,
                "result": job.result if job.is_finished else None,
                "error": str(job.exc_info) if job.is_failed else None
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting task status: {e}")
            return {"status": "error", "error": str(e)}
    
    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task
        
        Args:
            task_id: Task ID
            
        Returns:
            True if cancelled successfully
        """
        try:
            job = self.queue.fetch_job(task_id)
            
            if not job:
                return False
            
            job.cancel()
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling task: {e}")
            return False
    
    def _execute_search_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search task (synchronous for RQ)"""
        try:
            logger.info(f"Executing search task for requirement {task_data['requirement_id']}")
            
            # Search for listings
            listings = asyncio.run(search_listings(
                query=task_data["query"],
                location=task_data.get("location", ""),
                max_pages=3
            ))
            
            # Filter by price if specified
            if task_data.get("max_price"):
                listings = [l for l in listings if l.get("price", 0) <= task_data["max_price"]]
            
            if task_data.get("min_price"):
                listings = [l for l in listings if l.get("price", 0) >= task_data["min_price"]]
            
            # Store results in database
            db = get_db()
            for listing_data in listings:
                listing = Listing(
                    title=listing_data.get("title", ""),
                    description=listing_data.get("description", ""),
                    price=listing_data.get("price"),
                    location=listing_data.get("location", ""),
                    url=listing_data.get("url", ""),
                    image_url=listing_data.get("image_url", ""),
                    source=listing_data.get("source", "olx"),
                    requirement_id=task_data["requirement_id"],
                    user_id=task_data["user_id"],
                    scraped_at=datetime.utcnow()
                )
                db.add(listing)
            
            db.commit()
            
            result = {
                "status": "completed",
                "listings_found": len(listings),
                "requirement_id": task_data["requirement_id"],
                "completed_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Search task completed: {len(listings)} listings found")
            return result
            
        except Exception as e:
            logger.error(f"Error executing search task: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "requirement_id": task_data.get("requirement_id")
            }
    
    def _execute_analysis_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis task (synchronous for RQ)"""
        try:
            logger.info(f"Executing analysis task for {len(task_data['listing_ids'])} listings")
            
            # Get listings from database
            db = get_db()
            listings = db.query(Listing).filter(
                Listing.id.in_(task_data["listing_ids"])
            ).all()
            
            # Convert to dict format for analysis
            listing_data = []
            for listing in listings:
                listing_data.append({
                    "id": str(listing.id),
                    "title": listing.title,
                    "description": listing.description,
                    "price": listing.price,
                    "location": listing.location,
                    "url": listing.url,
                    "image_url": listing.image_url,
                    "source": listing.source
                })
            
            # Analyze listings
            analyzed_listings = asyncio.run(analyze_multiple_listings(listing_data))
            
            # Compare listings
            comparison = asyncio.run(compare_listings(analyzed_listings))
            
            result = {
                "status": "completed",
                "listings_analyzed": len(analyzed_listings),
                "comparison": comparison,
                "completed_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Analysis task completed: {len(analyzed_listings)} listings analyzed")
            return result
            
        except Exception as e:
            logger.error(f"Error executing analysis task: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_valuation_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute valuation task (synchronous for RQ)"""
        try:
            logger.info(f"Executing valuation task for {len(task_data['listing_ids'])} listings")
            
            # Get listings from database
            db = get_db()
            listings = db.query(Listing).filter(
                Listing.id.in_(task_data["listing_ids"])
            ).all()
            
            # Convert to dict format for valuation
            listing_data = []
            for listing in listings:
                listing_data.append({
                    "id": str(listing.id),
                    "title": listing.title,
                    "description": listing.description,
                    "price": listing.price,
                    "location": listing.location,
                    "url": listing.url,
                    "image_url": listing.image_url,
                    "source": listing.source
                })
            
            # Valuate listings
            valuated_listings = asyncio.run(batch_valuate_listings(listing_data))
            
            # Compare values
            value_comparison = asyncio.run(compare_values(valuated_listings))
            
            result = {
                "status": "completed",
                "listings_valuated": len(valuated_listings),
                "value_comparison": value_comparison,
                "completed_at": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Valuation task completed: {len(valuated_listings)} listings valuated")
            return result
            
        except Exception as e:
            logger.error(f"Error executing valuation task: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }


# Global scheduler service instance
scheduler_service = SchedulerService()


async def schedule_search_task(requirement_id: str, user_id: str) -> str:
    """Schedule a search task"""
    return await scheduler_service.schedule_search_task(requirement_id, user_id)


async def schedule_analysis_task(listing_ids: List[str], user_id: str) -> str:
    """Schedule an analysis task"""
    return await scheduler_service.schedule_analysis_task(listing_ids, user_id)


async def schedule_valuation_task(listing_ids: List[str], user_id: str) -> str:
    """Schedule a valuation task"""
    return await scheduler_service.schedule_valuation_task(listing_ids, user_id)


async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get task status"""
    return await scheduler_service.get_task_status(task_id)


async def cancel_task(task_id: str) -> bool:
    """Cancel a task"""
    return await scheduler_service.cancel_task(task_id) 