"""
Unit tests for file utilities
"""

import unittest
import os
import tempfile
from PIL import Image
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils import (
    allowed_file,
    save_upload_file,
    load_image,
    cleanup_file,
    validate_image_size
)


class TestFileUtils(unittest.TestCase):
    """Test cases for file utility functions"""
    
    def test_allowed_file_valid(self):
        """Test allowed_file with valid extensions"""
        valid_files = [
            'image.png',
            'photo.jpg',
            'picture.jpeg',
            'test.gif',
            'bitmap.bmp'
        ]
        for filename in valid_files:
            self.assertTrue(allowed_file(filename))
    
    def test_allowed_file_invalid(self):
        """Test allowed_file with invalid extensions"""
        invalid_files = [
            'document.pdf',
            'script.py',
            'text.txt',
            'noextension',
            'image.exe'
        ]
        for filename in invalid_files:
            self.assertFalse(allowed_file(filename))
    
    def test_load_image(self):
        """Test loading an image"""
        # Create temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Load image
            loaded_img = load_image(tmp_path)
            self.assertIsNotNone(loaded_img)
            self.assertIsInstance(loaded_img, Image.Image)
        finally:
            # Cleanup
            os.unlink(tmp_path)
    
    def test_load_image_invalid(self):
        """Test loading invalid image"""
        result = load_image('nonexistent.png')
        self.assertIsNone(result)
    
    def test_cleanup_file(self):
        """Test file cleanup"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'test')
            tmp_path = tmp.name
        
        # File should exist
        self.assertTrue(os.path.exists(tmp_path))
        
        # Cleanup
        result = cleanup_file(tmp_path)
        self.assertTrue(result)
        
        # File should not exist
        self.assertFalse(os.path.exists(tmp_path))
    
    def test_cleanup_nonexistent_file(self):
        """Test cleanup of nonexistent file"""
        result = cleanup_file('nonexistent_file.tmp')
        self.assertFalse(result)
    
    def test_validate_image_size(self):
        """Test image size validation"""
        # Create small temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'small file')
            tmp_path = tmp.name
        
        try:
            result = validate_image_size(tmp_path)
            self.assertTrue(result)
        finally:
            os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()
