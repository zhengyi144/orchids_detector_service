import pytest
from src.services.inference import detect_disease

def test_detect_disease_valid_image():
    image_path = "tests/test_images/healthy_orchid.jpg"
    result = detect_disease(image_path)
    assert result['disease'] == 'healthy'
    assert result['confidence'] >= 0.9

def test_detect_disease_diseased_image():
    image_path = "tests/test_images/diseased_orchid.jpg"
    result = detect_disease(image_path)
    assert result['disease'] in ['black_spot', 'powdery_mildew']
    assert result['confidence'] >= 0.8

def test_detect_disease_invalid_image():
    image_path = "tests/test_images/invalid_image.txt"
    with pytest.raises(ValueError):
        detect_disease(image_path)