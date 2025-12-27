"""
Orchid Detector Model
Handles orchid species detection and classification.
"""

import torch
import torch.nn as nn
from typing import Dict, List, Tuple
from PIL import Image
import numpy as np


class OrchidDetector:
    """
    Orchid detection and classification model.
    """
    
    # Common orchid species for detection
    ORCHID_SPECIES = [
        "Phalaenopsis",  # 蝴蝶兰
        "Dendrobium",    # 石斛兰
        "Cattleya",      # 卡特兰
        "Cymbidium",     # 蕙兰
        "Oncidium",      # 文心兰
        "Vanda",         # 万代兰
        "Paphiopedilum", # 兜兰
        "Unknown"        # 未知品种
    ]
    
    def __init__(self, model_path: str = None):
        """
        Initialize the orchid detector.
        
        Args:
            model_path: Path to the trained model weights (optional)
        """
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()
        
    def _load_model(self):
        """
        Load the detection model.
        For now, returns a simple placeholder model.
        In production, this would load a trained model.
        """
        # Placeholder model - in production, load actual trained weights
        model = SimpleOrchidClassifier(num_classes=len(self.ORCHID_SPECIES))
        model.to(self.device)
        model.eval()
        return model
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for model input.
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed image tensor
        """
        # Resize to standard size
        image = image.convert('RGB')
        image = image.resize((224, 224))
        
        # Convert to numpy array and normalize
        img_array = np.array(image).astype(np.float32) / 255.0
        
        # Normalize with ImageNet stats
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img_array = (img_array - mean) / std
        
        # Convert to tensor and add batch dimension
        img_tensor = torch.from_numpy(img_array).permute(2, 0, 1).unsqueeze(0)
        return img_tensor.float().to(self.device)
    
    def detect(self, image: Image.Image) -> Dict:
        """
        Detect orchid species in the image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Detection results including species and confidence
        """
        # Preprocess image
        img_tensor = self.preprocess_image(image)
        
        # Run inference
        with torch.no_grad():
            output = self.model(img_tensor)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
            
        # Get top 3 predictions
        top_probs, top_indices = torch.topk(probabilities[0], min(3, len(self.ORCHID_SPECIES)))
        
        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            predictions.append({
                "species": self.ORCHID_SPECIES[idx.item()],
                "confidence": float(prob.item())
            })
        
        result = {
            "primary_species": self.ORCHID_SPECIES[predicted_idx.item()],
            "confidence": float(confidence.item()),
            "all_predictions": predictions,
            "is_orchid": confidence.item() > 0.3,  # Threshold for orchid detection
        }
        
        return result
    
    def batch_detect(self, images: List[Image.Image]) -> List[Dict]:
        """
        Detect orchid species in multiple images.
        
        Args:
            images: List of PIL Image objects
            
        Returns:
            List of detection results
        """
        results = []
        for image in images:
            result = self.detect(image)
            results.append(result)
        return results


class SimpleOrchidClassifier(nn.Module):
    """
    Simple CNN classifier for orchid species.
    This is a placeholder - in production, use a pre-trained model like ResNet or EfficientNet.
    """
    
    def __init__(self, num_classes: int = 8):
        super(SimpleOrchidClassifier, self).__init__()
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(64, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
