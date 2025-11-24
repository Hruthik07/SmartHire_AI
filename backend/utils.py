"""
Utility functions for SmartHire AI Backend
Common helper functions used across the application
"""

import os
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def safe_parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON from text.
    
    Args:
        text: JSON string to parse
        
    Returns:
        Parsed dict or None if parsing fails
    """
    if not isinstance(text, str):
        logger.warning("Attempted to parse non-string as JSON")
        return None
    
    text = text.strip()
    if not text:
        return None
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error parsing JSON: {e}")
        return None


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename by removing dangerous characters and limiting length.
    
    Args:
        filename: Original filename
        max_length: Maximum allowed filename length
        
    Returns:
        Sanitized filename safe for filesystem use
    """
    # Get base filename without path
    base = os.path.basename(filename)
    
    # Remove or replace dangerous characters
    dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\x00']
    for char in dangerous_chars:
        base = base.replace(char, '_')
    
    # Limit length
    if len(base) > max_length:
        name, ext = os.path.splitext(base)
        name = name[:max_length - len(ext) - 3] + "..."
        base = name + ext
    
    return base


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        Formatted string (e.g., "10.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Validate that file extension is in allowed list.
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions (e.g., {'.pdf', '.txt'})
        
    Returns:
        True if extension is allowed, False otherwise
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions
