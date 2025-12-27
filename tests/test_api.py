from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_disease():
    # Assuming the endpoint is /api/v1/predict and expects a POST request with an image
    with open("tests/test_image.jpg", "rb") as image_file:
        response = client.post("/api/v1/predict", files={"file": image_file})
    assert response.status_code == 200
    assert "disease" in response.json()  # Check if the response contains a disease key

def test_invalid_image_upload():
    response = client.post("/api/v1/predict", files={"file": ("test.txt", b"not an image")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid image format."}  # Adjust based on actual error handling