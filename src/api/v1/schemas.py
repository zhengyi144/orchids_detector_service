from pydantic import BaseModel
from typing import List, Optional

class DiseasePrediction(BaseModel):
    disease_name: str
    confidence: float

class ImageRequest(BaseModel):
    image_url: str

class ImageResponse(BaseModel):
    predictions: List[DiseasePrediction]
    message: Optional[str] = None