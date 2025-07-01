"""
File upload API endpoints
"""
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import redis
import json
import tempfile
import os
from datetime import datetime
import re

from app.core.config import settings
from app.validators.file_validator import validate_uploaded_files

router = APIRouter()

# Redis connection for storing analysis results
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

def parse_log_file(file_content: str, filename: str) -> List[dict]:
    """Parse a single log file and extract error entries"""
    errors = []
    
    try:
        if filename.upper().startswith('E_'):
            # Parse Visual Objects logs
            errors = parse_visual_objects_log(file_content, filename)
        elif filename.upper().startswith('EC_'):
            # Parse .NET logs
            errors = parse_dotnet_log(file_content, filename)
        else:
            # Try to auto-detect format
            if '***********************ERROR********************************' in file_content:
                errors = parse_visual_objects_log(file_content, filename)
            elif '------------------------------' in file_content:
                errors = parse_dotnet_log(file_content, filename)
    except Exception as e:
        print(f"Error parsing {filename}: {str(e)}")
    
    return errors

def parse_visual_objects_log(content: str, filename: str) -> List[dict]:
    """Parse Visual Objects log format"""
    errors = []
    
    # Extract user from filename (E_YYYYMMDD_USER.LOG)
    user_match = re.search(r'E_\d{8}_([^.]+)\.', filename)
    user = user_match.group(1) if user_match else "Unknown"
    
    # Split by error delimiter
    error_blocks = content.split('***********************ERROR********************************')
    
    for i, block in enumerate(error_blocks):
        if i == 0:  # Skip first block (usually header)
            continue
            
        # Extract error code and type
        code_match = re.search(r'(\d+)\s*\[\s*([^\]]+)\s*\]', block)
        if code_match:
            error_code = int(code_match.group(1))
            error_type = code_match.group(2).strip()
            
            # Extract timestamp
            timestamp_match = re.search(r'(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', block)
            timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            
            # Determine severity
            severity = "Critical" if error_code == 50 else ("High" if error_code in [2, 33] else "Medium")
            
            errors.append({
                "id": len(errors) + 1,
                "filename": filename,
                "user": user,
                "timestamp": timestamp,
                "type": error_type,
                "code": error_code,
                "severity": severity,
                "content": block.strip()[:200]  # First 200 chars
            })
    
    return errors

def parse_dotnet_log(content: str, filename: str) -> List[dict]:
    """Parse .NET log format"""
    errors = []
    
    # Extract user from filename (EC_YYYYMMDD_USER.LOG)
    user_match = re.search(r'EC_\d{8}_([^.]+)\.', filename)
    user = user_match.group(1) if user_match else "Unknown"
    
    # Split by error delimiter
    error_blocks = content.split('------------------------------')
    
    for i, block in enumerate(error_blocks):
        if i == 0:  # Skip first block
            continue
            
        # Extract logged at timestamp
        timestamp_match = re.search(r'Logged at:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', block)
        timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        
        # Extract exception type
        exception_match = re.search(r'(System\.\w+Exception)', block)
        if exception_match:
            exception_type = exception_match.group(1)
            error_type = exception_type.replace('System.', '').replace('Exception', ' ERROR')
            
            # Assign codes based on exception type
            code = 50 if 'AccessViolation' in exception_type else (51 if 'Memory' in exception_type else 52)
            severity = "Critical" if code == 50 else "High"
            
            errors.append({
                "id": len(errors) + 1,
                "filename": filename,
                "user": user,
                "timestamp": timestamp,
                "type": error_type,
                "code": code,
                "severity": severity,
                "content": block.strip()[:200]  # First 200 chars
            })
    
    return errors

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple log files for analysis
    """
    try:
        # Validate files
        validation_result = await validate_uploaded_files(files)
        
        if not validation_result.valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "File validation failed",
                    "errors": validation_result.errors,
                    "warnings": validation_result.warnings
                }
            )
        
        # Process and analyze valid files
        all_errors = []
        uploaded_files = []
        user_counts = {}
        error_type_counts = {}
        critical_error_count = 0
        
        for file in validation_result.valid_files:
            # Read file content
            content = await file.read()
            content_str = content.decode('utf-8', errors='ignore')
            
            # Parse the log file
            file_errors = parse_log_file(content_str, file.filename)
            
            # Update error IDs to be globally unique
            for error in file_errors:
                error['id'] = len(all_errors) + 1
                all_errors.append(error)
                
                # Count users
                user = error['user']
                user_counts[user] = user_counts.get(user, 0) + 1
                
                # Count error types
                error_type = error['type']
                error_type_counts[error_type] = error_type_counts.get(error_type, 0) + 1
                
                # Count critical errors
                if error['severity'] == 'Critical':
                    critical_error_count += 1
            
            file_info = {
                "filename": file.filename,
                "size": file.size,
                "content_type": file.content_type,
                "detected_type": validation_result.file_types.get(file.filename),
                "errors_found": len(file_errors)
            }
            uploaded_files.append(file_info)
        
        # Generate analytics data
        summary_data = {
            "total_errors": len(all_errors),
            "critical_errors": critical_error_count,
            "active_users": len(user_counts),
            "files_analyzed": len(uploaded_files)
        }
        
        # Prepare chart data
        error_types_data = {
            "labels": list(error_type_counts.keys())[:5],  # Top 5 error types
            "data": list(error_type_counts.values())[:5]
        }
        
        user_activity_data = {
            "labels": list(user_counts.keys()),
            "data": list(user_counts.values())
        }
        
        # Get critical errors for alerts
        critical_errors = [error for error in all_errors if error['severity'] == 'Critical'][:10]
        critical_errors_data = {
            "critical_errors": critical_errors
        }
        
        # Generate timeline data (simplified - group by date)
        timeline_data = generate_timeline_data(all_errors)
        
        # Store all data in Redis
        redis_client.setex("error_summary", 3600, json.dumps(summary_data))
        redis_client.setex("analyzed_errors", 3600, json.dumps(all_errors))
        redis_client.setex("error_types", 3600, json.dumps(error_types_data))
        redis_client.setex("user_activity", 3600, json.dumps(user_activity_data))
        redis_client.setex("critical_errors", 3600, json.dumps(critical_errors_data))
        redis_client.setex("error_timeline", 3600, json.dumps(timeline_data))
        
        return {
            "message": "Files analyzed successfully",
            "files": uploaded_files,
            "total_files": len(uploaded_files),
            "total_errors": len(all_errors),
            "summary": summary_data,
            "warnings": validation_result.warnings
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def generate_timeline_data(errors: List[dict]) -> dict:
    """Generate timeline data from errors"""
    from collections import defaultdict
    
    daily_counts = defaultdict(int)
    
    for error in errors:
        try:
            # Parse timestamp and extract date
            timestamp = error['timestamp']
            date_part = timestamp.split(' ')[0]  # Get DD.MM.YYYY part
            day, month, year = date_part.split('.')
            iso_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            daily_counts[iso_date] += 1
        except:
            # If parsing fails, use today
            today = datetime.now().strftime("%Y-%m-%d")
            daily_counts[today] += 1
    
    # Sort dates and prepare data
    sorted_dates = sorted(daily_counts.keys())
    labels = sorted_dates
    data = [daily_counts[date] for date in sorted_dates]
    
    return {
        "labels": labels,
        "data": data
    }

@router.get("/upload-status/{upload_id}")
async def get_upload_status(upload_id: str):
    """
    Get upload status by ID
    """
    # TODO: Implement upload status tracking
    return {"upload_id": upload_id, "status": "completed"}