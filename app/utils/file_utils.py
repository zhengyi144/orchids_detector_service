"""
Utility functions for the orchid detection service
"""

import os
import uuid
from typing import Optional
from PIL import Image
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed.
    
    Args:
        filename: Name of the file
        
    Returns:
        True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(file, upload_folder: str) -> Optional[str]:
    """
    Save uploaded file with a unique name.
    
    Args:
        file: File object from request
        upload_folder: Directory to save the file
        
    Returns:
        Path to saved file or None if failed
    """
    if not file or not allowed_file(file.filename):
        return None
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4()}.{ext}"
    
    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    return filepath


def load_image(filepath: str) -> Optional[Image.Image]:
    """
    Load image from filepath.
    
    Args:
        filepath: Path to image file
        
    Returns:
        PIL Image object or None if failed
    """
    try:
        image = Image.open(filepath)
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


def cleanup_file(filepath: str) -> bool:
    """
    Delete a file from filesystem.
    
    Args:
        filepath: Path to file
        
    Returns:
        True if deletion successful
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def validate_image_size(filepath: str) -> bool:
    """
    Validate that image file size is within limits.
    
    Args:
        filepath: Path to image file
        
    Returns:
        True if file size is valid
    """
    try:
        file_size = os.path.getsize(filepath)
        return file_size <= MAX_FILE_SIZE
    except Exception:
        return False
