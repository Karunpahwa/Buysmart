"""
Scheduler API endpoints
Handles background task scheduling and management
"""

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from ..services.scheduler import (
    schedule_search_task, schedule_analysis_task, schedule_valuation_task,
    get_task_status, cancel_task
)
from ..api.auth import get_current_user_dependency
from ..models.schemas import User as UserSchema

router = APIRouter(prefix="/scheduler", tags=["scheduler"])


class TaskRequest(BaseModel):
    """Request for scheduling tasks"""
    listing_ids: Optional[List[str]] = None
    requirement_id: Optional[str] = None


@router.post("/search")
async def schedule_search(
    request: TaskRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Schedule a search task for a requirement
    
    Args:
        request: Task request with requirement_id
        current_user: Current authenticated user
        
    Returns:
        Task ID and status
    """
    try:
        if not request.requirement_id:
            raise HTTPException(status_code=400, detail="requirement_id is required")
        
        task_id = await schedule_search_task(request.requirement_id, str(current_user.id))
        
        return {
            "status": "success",
            "task_id": task_id,
            "task_type": "search",
            "requirement_id": request.requirement_id,
            "message": "Search task scheduled successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling search task: {str(e)}")


@router.post("/analyze")
async def schedule_analysis(
    request: TaskRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Schedule an analysis task for listings
    
    Args:
        request: Task request with listing_ids
        current_user: Current authenticated user
        
    Returns:
        Task ID and status
    """
    try:
        if not request.listing_ids:
            raise HTTPException(status_code=400, detail="listing_ids is required")
        
        task_id = await schedule_analysis_task(request.listing_ids, str(current_user.id))
        
        return {
            "status": "success",
            "task_id": task_id,
            "task_type": "analysis",
            "listings_count": len(request.listing_ids),
            "message": "Analysis task scheduled successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling analysis task: {str(e)}")


@router.post("/valuate")
async def schedule_valuation(
    request: TaskRequest = Body(...),
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Schedule a valuation task for listings
    
    Args:
        request: Task request with listing_ids
        current_user: Current authenticated user
        
    Returns:
        Task ID and status
    """
    try:
        if not request.listing_ids:
            raise HTTPException(status_code=400, detail="listing_ids is required")
        
        task_id = await schedule_valuation_task(request.listing_ids, str(current_user.id))
        
        return {
            "status": "success",
            "task_id": task_id,
            "task_type": "valuation",
            "listings_count": len(request.listing_ids),
            "message": "Valuation task scheduled successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling valuation task: {str(e)}")


@router.get("/status/{task_id}")
async def get_task_status_endpoint(
    task_id: str,
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Get status of a scheduled task
    
    Args:
        task_id: Task ID to check
        current_user: Current authenticated user
        
    Returns:
        Task status information
    """
    try:
        status = await get_task_status(task_id)
        
        return {
            "status": "success",
            "task_status": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting task status: {str(e)}")


@router.delete("/cancel/{task_id}")
async def cancel_task_endpoint(
    task_id: str,
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Cancel a scheduled task
    
    Args:
        task_id: Task ID to cancel
        current_user: Current authenticated user
        
    Returns:
        Cancellation status
    """
    try:
        cancelled = await cancel_task(task_id)
        
        if cancelled:
            return {
                "status": "success",
                "task_id": task_id,
                "message": "Task cancelled successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Task not found or already completed")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling task: {str(e)}")


@router.get("/tasks")
async def list_user_tasks(
    current_user: UserSchema = Depends(get_current_user_dependency),
    limit: int = Query(10, description="Number of tasks to return", ge=1, le=50),
    offset: int = Query(0, description="Number of tasks to skip", ge=0)
) -> Dict[str, Any]:
    """
    List tasks for the current user
    
    Args:
        current_user: Current authenticated user
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip
        
    Returns:
        List of user tasks
    """
    try:
        # This would typically query the database for user tasks
        # For now, we'll return a mock response
        tasks = [
            {
                "task_id": "task_123",
                "type": "search",
                "status": "completed",
                "created_at": "2024-01-15T10:30:00Z",
                "completed_at": "2024-01-15T10:35:00Z",
                "result": {
                    "listings_found": 25,
                    "requirement_id": "req_456"
                }
            },
            {
                "task_id": "task_124",
                "type": "analysis",
                "status": "queued",
                "created_at": "2024-01-15T11:00:00Z",
                "listings_count": 10
            }
        ]
        
        return {
            "status": "success",
            "tasks": tasks[:limit],
            "total": len(tasks),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tasks: {str(e)}")


@router.get("/queue/status")
async def get_queue_status(
    current_user: UserSchema = Depends(get_current_user_dependency)
) -> Dict[str, Any]:
    """
    Get current queue status
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Queue status information
    """
    try:
        # This would typically query Redis for queue status
        # For now, we'll return a mock response
        queue_status = {
            "total_jobs": 5,
            "queued_jobs": 2,
            "running_jobs": 1,
            "completed_jobs": 2,
            "failed_jobs": 0,
            "workers": 1,
            "queue_name": "buysmart_tasks"
        }
        
        return {
            "status": "success",
            "queue_status": queue_status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting queue status: {str(e)}") 