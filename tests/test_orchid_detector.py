"""
Unit tests for OrchidDetector model
"""

import unittest
import numpy as np
from PIL import Image
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import OrchidDetector


class TestOrchidDetector(unittest.TestCase):
    """Test cases for OrchidDetector class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.detector = OrchidDetector()
    
    def test_detector_initialization(self):
        """Test that detector initializes correctly"""
        self.assertIsNotNone(self.detector)
        self.assertIsNotNone(self.detector.model)
        self.assertEqual(len(self.detector.ORCHID_SPECIES), 8)
    
    def test_species_list(self):
        """Test that species list is correct"""
        expected_species = [
            "Phalaenopsis",
            "Dendrobium",
            "Cattleya",
            "Cymbidium",
            "Oncidium",
            "Vanda",
            "Paphiopedilum",
            "Unknown"
        ]
        self.assertEqual(self.detector.ORCHID_SPECIES, expected_species)
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        # Create a test image
        img = Image.new('RGB', (100, 100), color='red')
        
        # Preprocess
        tensor = self.detector.preprocess_image(img)
        
        # Check shape
        self.assertEqual(tensor.shape, (1, 3, 224, 224))
    
    def test_detect_returns_result(self):
        """Test that detect returns proper result structure"""
        # Create a test image
        img = Image.new('RGB', (100, 100), color='green')
        
        # Detect
        result = self.detector.detect(img)
        
        # Check result structure
        self.assertIn('primary_species', result)
        self.assertIn('confidence', result)
        self.assertIn('all_predictions', result)
        self.assertIn('is_orchid', result)
        
        # Check types
        self.assertIsInstance(result['primary_species'], str)
        self.assertIsInstance(result['confidence'], float)
        self.assertIsInstance(result['all_predictions'], list)
        self.assertIsInstance(result['is_orchid'], bool)
    
    def test_detect_confidence_range(self):
        """Test that confidence values are in valid range"""
        img = Image.new('RGB', (100, 100), color='blue')
        result = self.detector.detect(img)
        
        # Check confidence is between 0 and 1
        self.assertGreaterEqual(result['confidence'], 0.0)
        self.assertLessEqual(result['confidence'], 1.0)
        
        # Check all predictions confidences
        for pred in result['all_predictions']:
            self.assertGreaterEqual(pred['confidence'], 0.0)
            self.assertLessEqual(pred['confidence'], 1.0)
    
    def test_batch_detect(self):
        """Test batch detection"""
        images = [
            Image.new('RGB', (100, 100), color='red'),
            Image.new('RGB', (100, 100), color='green')
        ]
        
        results = self.detector.batch_detect(images)
        
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn('primary_species', result)
            self.assertIn('confidence', result)


if __name__ == '__main__':
    unittest.main()
