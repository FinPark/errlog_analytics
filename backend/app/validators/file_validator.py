"""
File validation utilities
"""
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from fastapi import UploadFile

from app.core.config import settings

@dataclass
class ValidationResult:
    """File validation result"""
    valid: bool
    valid_files: List[UploadFile]
    errors: List[str]
    warnings: List[str]
    file_types: Dict[str, str]

async def validate_uploaded_files(files: List[UploadFile]) -> ValidationResult:
    """
    Validate uploaded log files
    """
    valid_files = []
    errors = []
    warnings = []
    file_types = {}
    
    if not files:
        errors.append("No files provided")
        return ValidationResult(False, [], errors, warnings, {})
    
    total_size = 0
    
    for file in files:
        # Check file extension
        if not any(file.filename.lower().endswith(ext.lower()) for ext in settings.ALLOWED_FILE_EXTENSIONS):
            errors.append(f"File '{file.filename}' has invalid extension. Allowed: {settings.ALLOWED_FILE_EXTENSIONS}")
            continue
        
        # Check file size
        if hasattr(file, 'size') and file.size:
            total_size += file.size
            if file.size > settings.MAX_FILE_SIZE:
                errors.append(f"File '{file.filename}' is too large ({file.size} bytes)")
                continue
        
        # Detect log type
        log_type = detect_log_type(file.filename)
        file_types[file.filename] = log_type
        
        if log_type == "unknown":
            warnings.append(f"Could not detect log type for '{file.filename}'")
        
        valid_files.append(file)
    
    # Check total size
    if total_size > settings.MAX_FILE_SIZE:
        errors.append(f"Total file size ({total_size} bytes) exceeds limit ({settings.MAX_FILE_SIZE} bytes)")
    
    is_valid = len(errors) == 0 and len(valid_files) > 0
    
    return ValidationResult(is_valid, valid_files, errors, warnings, file_types)

def detect_log_type(filename: str) -> str:
    """
    Detect log file type from filename
    """
    filename_upper = filename.upper()
    
    if filename_upper.startswith("E_") and filename_upper.endswith(".LOG"):
        return "visual_objects"
    elif filename_upper.startswith("EC_") and filename_upper.endswith(".LOG"):
        return "dotnet"
    else:
        return "unknown"