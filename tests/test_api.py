"""
Integration tests for API endpoints
"""

import unittest
import json
import io
import sys
import os
from PIL import Image

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import create_app


class TestAPIEndpoints(unittest.TestCase):
    """Test cases for API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'orchid_detector')
    
    def test_get_species(self):
        """Test get species endpoint"""
        response = self.client.get('/api/species')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('species', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 8)
        self.assertIsInstance(data['species'], list)
    
    def test_get_info(self):
        """Test get info endpoint"""
        response = self.client.get('/api/info')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('service', data)
        self.assertIn('version', data)
        self.assertIn('supported_formats', data)
    
    def test_detect_no_file(self):
        """Test detect endpoint without file"""
        response = self.client.post('/api/detect')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_detect_with_image(self):
        """Test detect endpoint with image"""
        # Create test image in memory
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Send request
        response = self.client.post(
            '/api/detect',
            data={'image': (img_bytes, 'test.png')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('result', data)
        self.assertTrue(data['success'])
        
        # Check result structure
        result = data['result']
        self.assertIn('primary_species', result)
        self.assertIn('confidence', result)
        self.assertIn('all_predictions', result)
    
    def test_detect_invalid_file(self):
        """Test detect endpoint with invalid file"""
        # Create a text file instead of image
        txt_file = io.BytesIO(b'not an image')
        
        response = self.client.post(
            '/api/detect',
            data={'image': (txt_file, 'test.txt')},
            content_type='multipart/form-data'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_index_page(self):
        """Test index page"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
