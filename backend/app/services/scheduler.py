"""
Scheduler Service for periodic tasks
Handles automatic scraping and other background jobs
"""

import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from ..services.scraper import schedule_periodic_scraping

logger = logging.getLogger(__name__)

# In-memory task storage (in production, use Redis or database)
task_store = {}


class SchedulerService:
    """Service for scheduling periodic tasks"""
    
    def __init__(self):
        self.running = False
        self.task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._run_scheduler())
        logger.info("Scheduler started")
    
    async def stop(self):
        """Stop the scheduler"""
        if not self.running:
            return
        
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            try:
                # Run periodic scraping every hour
                await schedule_periodic_scraping()
                
                # Wait for 1 hour before next run
                await asyncio.sleep(3600)  # 1 hour
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error


# Global scheduler instance
scheduler_service = SchedulerService()


async def start_scheduler():
    """Start the global scheduler"""
    await scheduler_service.start()


async def stop_scheduler():
    """Stop the global scheduler"""
    await scheduler_service.stop()


# Task scheduling functions for API
async def schedule_search_task(requirement_id: str, user_id: str) -> str:
    """Schedule a search task for a requirement"""
    task_id = str(uuid.uuid4())
    task_store[task_id] = {
        "type": "search",
        "status": "queued",
        "requirement_id": requirement_id,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "result": None
    }
    
    # In a real implementation, this would queue the task
    logger.info(f"Scheduled search task {task_id} for requirement {requirement_id}")
    return task_id


async def schedule_analysis_task(listing_ids: List[str], user_id: str) -> str:
    """Schedule an analysis task for listings"""
    task_id = str(uuid.uuid4())
    task_store[task_id] = {
        "type": "analysis",
        "status": "queued",
        "listing_ids": listing_ids,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "result": None
    }
    
    # In a real implementation, this would queue the task
    logger.info(f"Scheduled analysis task {task_id} for {len(listing_ids)} listings")
    return task_id


async def schedule_valuation_task(listing_ids: List[str], user_id: str) -> str:
    """Schedule a valuation task for listings"""
    task_id = str(uuid.uuid4())
    task_store[task_id] = {
        "type": "valuation",
        "status": "queued",
        "listing_ids": listing_ids,
        "user_id": user_id,
        "created_at": datetime.utcnow(),
        "result": None
    }
    
    # In a real implementation, this would queue the task
    logger.info(f"Scheduled valuation task {task_id} for {len(listing_ids)} listings")
    return task_id


async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get status of a task"""
    if task_id not in task_store:
        raise ValueError(f"Task {task_id} not found")
    
    return task_store[task_id]


async def cancel_task(task_id: str) -> bool:
    """Cancel a task"""
    if task_id not in task_store:
        return False
    
    task = task_store[task_id]
    if task["status"] in ["queued", "running"]:
        task["status"] = "cancelled"
        task["cancelled_at"] = datetime.utcnow()
        logger.info(f"Cancelled task {task_id}")
        return True
    
    return False 