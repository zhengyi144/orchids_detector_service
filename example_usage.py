"""
Example usage of the Orchid Detection Service API
"""

import requests
import sys


def test_health_check(base_url):
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{base_url}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_get_species(base_url):
    """Test getting list of species"""
    print("Getting supported species...")
    response = requests.get(f"{base_url}/api/species")
    data = response.json()
    print(f"Supported species ({data['count']}):")
    for species in data['species']:
        print(f"  - {species}")
    print()


def test_detect_orchid(base_url, image_path):
    """Test orchid detection"""
    print(f"Detecting orchid in image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': f}
            response = requests.post(f"{base_url}/api/detect", files=files)
            
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                result = data['result']
                print(f"Detection successful!")
                print(f"Primary species: {result['primary_species']}")
                print(f"Confidence: {result['confidence']:.2%}")
                print(f"Is orchid: {result['is_orchid']}")
                
                if len(result['all_predictions']) > 1:
                    print("\nOther predictions:")
                    for pred in result['all_predictions'][1:]:
                        print(f"  - {pred['species']}: {pred['confidence']:.2%}")
            else:
                print(f"Detection failed: {data.get('message')}")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def main():
    base_url = "http://localhost:5000"
    
    # Test health check
    test_health_check(base_url)
    
    # Test getting species
    test_get_species(base_url)
    
    # Test detection (if image path is provided)
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_detect_orchid(base_url, image_path)
    else:
        print("Usage: python example_usage.py [image_path]")
        print("Example: python example_usage.py my_orchid.jpg")


if __name__ == "__main__":
    main()
