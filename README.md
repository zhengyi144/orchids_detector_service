# Orchid Disease Detector

This project is a FastAPI application designed for detecting and recognizing diseases in orchids using machine learning techniques. It provides an API for users to upload images of orchids and receive predictions regarding potential diseases.

## Project Structure

```
orchid-disease-detector
├── src
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api                   # Contains API related files
│   │   ├── v1                # Version 1 of the API
│   │   │   ├── routes.py     # API routes
│   │   │   └── schemas.py    # Request and response schemas
│   │   └── deps.py           # Dependency functions
│   ├── core                  # Core application logic
│   │   ├── config.py         # Configuration settings
│   │   └── logging.py        # Logging configurations
│   ├── services              # Business logic for inference
│   │   └── inference.py      # Disease detection and recognition logic
│   ├── models                # Machine learning model definitions
│   │   ├── model.py          # Model architecture and loading
│   │   └── predictor.py      # Prediction functions
│   ├── ml                    # Machine learning related files
│   │   ├── train.py          # Training logic for the model
│   │   └── dataset.py        # Dataset management
│   └── utils                 # Utility functions
│       ├── image_processing.py# Image processing utilities
│       └── metrics.py        # Evaluation metrics
├── tests                     # Test files
│   ├── test_api.py          # Unit tests for API endpoints
│   └── test_inference.py     # Unit tests for inference logic
├── requirements.txt          # Project dependencies
├── pyproject.toml           # Project configuration
├── Dockerfile                # Docker image instructions
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd orchid-disease-detector
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Copy `.env.example` to `.env` and configure the necessary variables.

5. **Run the application:**
   ```
   # 开发模式（自动重载）
   nohup uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
   
   # 生产模式
   nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4 &
   ```

## Usage

- Send a POST request to `/api/v1/predict` with an image of an orchid to receive disease predictions.

## Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push to your branch and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
# orchids_detector_service