"""
Error analysis endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import redis
import json
from datetime import datetime, timedelta
import random

router = APIRouter()

# Redis connection for storing analysis results
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

@router.get("/errors/summary")
async def get_error_summary():
    """Get summary statistics of analyzed errors"""
    try:
        # Try to get summary from Redis
        summary_data = redis_client.get("error_summary")
        if summary_data:
            return json.loads(summary_data)
        
        # If no data in Redis, return empty summary
        return {
            "total_errors": 0,
            "critical_errors": 0,
            "active_users": 0,
            "files_analyzed": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get error summary: {str(e)}")

@router.get("/errors")
async def get_errors(page: int = 1, limit: int = 100):
    """Get paginated list of all errors"""
    try:
        # Try to get errors from Redis
        errors_data = redis_client.get("analyzed_errors")
        if errors_data:
            all_errors = json.loads(errors_data)
            
            # Paginate results
            start_idx = (page - 1) * limit
            end_idx = start_idx + limit
            paginated_errors = all_errors[start_idx:end_idx]
            
            return {
                "errors": paginated_errors,
                "total": len(all_errors),
                "page": page,
                "limit": limit,
                "has_more": end_idx < len(all_errors)
            }
        
        # If no data, return empty
        return {
            "errors": [],
            "total": 0,
            "page": page,
            "limit": limit,
            "has_more": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get errors: {str(e)}")

@router.get("/errors/timeline")
async def get_error_timeline():
    """Get error timeline data for charts"""
    try:
        # Try to get timeline from Redis
        timeline_data = redis_client.get("error_timeline")
        if timeline_data:
            return json.loads(timeline_data)
        
        # Generate demo timeline data
        now = datetime.now()
        dates = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
        counts = [random.randint(0, 25) for _ in dates]
        
        return {
            "labels": dates,
            "data": counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get timeline: {str(e)}")

@router.get("/errors/types")
async def get_error_types():
    """Get error types distribution for pie chart"""
    try:
        # Try to get types from Redis
        types_data = redis_client.get("error_types")
        if types_data:
            return json.loads(types_data)
        
        # Generate demo error types data
        return {
            "labels": ["DATA TYPE ERROR", "BOUND ERROR", "ACCESS VIOLATION", "INVALID OPERATION", "MEMORY ERROR"],
            "data": [45, 30, 15, 7, 3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get error types: {str(e)}")

@router.get("/errors/users")
async def get_user_activity():
    """Get user activity data for bar chart"""
    try:
        # Try to get user activity from Redis
        users_data = redis_client.get("user_activity")
        if users_data:
            return json.loads(users_data)
        
        # Generate demo user activity data
        return {
            "labels": ["GAM", "SWE", "AVB", "MSP", "JAE", "TOM", "LIS"],
            "data": [25, 18, 12, 8, 6, 4, 2]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user activity: {str(e)}")

@router.get("/errors/critical")
async def get_critical_errors():
    """Get list of critical errors that need attention"""
    try:
        # Try to get critical errors from Redis
        critical_data = redis_client.get("critical_errors")
        if critical_data:
            return json.loads(critical_data)
        
        # Generate demo critical errors
        return {
            "critical_errors": [
                {
                    "id": 1,
                    "type": "ACCESS VIOLATION",
                    "user": "GAM",
                    "timestamp": "02.12.2024 12:54:19",
                    "code": 50,
                    "severity": "Critical"
                },
                {
                    "id": 2,
                    "type": "MEMORY ERROR",
                    "user": "SWE",
                    "timestamp": "01.12.2024 15:23:41",
                    "code": 51,
                    "severity": "Critical"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get critical errors: {str(e)}")