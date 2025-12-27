import torch
import logging
from typing import Optional
from ultralytics import YOLO

logger = logging.getLogger("model_builder")


def get_device(use_gpu: bool = True) -> torch.device:
    """
    自动识别并返回可用的设备（GPU/CPU）
    
    Args:
        use_gpu: 是否使用GPU（如果可用）
        
    Returns:
        torch.device: 可用的设备对象
    """
    if use_gpu and torch.cuda.is_available():
        device = torch.device("cuda")
        logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
        logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        device = torch.device("cpu")
        logger.info("Using CPU")
        if use_gpu and not torch.cuda.is_available():
            logger.warning("GPU requested but not available, falling back to CPU")
    
    return device

def load_model(model_path: str, model_name: Optional[object] = None, device: Optional[torch.device] = None) -> torch.nn.Module:
    """
    加载PyTorch模型
    
    Args:
        model_path: 模型文件路径
        model_name: 模型名称或类（如果需要实例化）
        device: 目标设备，如果为None则自动识别
        
    Returns:
        torch.nn.Module: 加载的模型
    """
    if device is None:
        device = get_device()
    
    try:
        logger.info(f"Loading {model_name} model from {model_path}")
        
        if model_name.lower() in ["yolov11", "yolov8"]:
            # 加载YOLO模型
            model = YOLO(model_path)
            # YOLO模型会自动处理设备
            logger.info(f"YOLO model loaded successfully")
        else:
            # 加载标准PyTorch模型
            model = torch.load(model_path, map_location=device)
            model.to(device)
            model.eval()
            logger.info(f"PyTorch model loaded successfully on {device}")
        
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

def init_models(model_config):
    """
    根据配置初始化多个模型：
    orchids_disease_detect:
        model_path: "src/ml/weight/best.pt"
        model_name: "yolov11"
    """
    models = {}
    
    for project_name, model_config in model_config.items():
        try:
            model_path = model_config.get("model_path")
            model_name = model_config.get("model_name")
            
            if not model_path:
                logger.warning(f"Model path not found for {model_name}, skipping...")
                continue
            
            logger.info(f"Initializing model: {model_name}")
            
            # 加载模型（这里假设是完整模型文件）
            model = load_model(model_path, model_name)
            models[project_name] = model
            
            logger.info(f"Model {model_name} initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize model {model_name}: {e}")
            # 继续加载其他模型，不中断整个初始化过程
            continue
    
    if not models:
        logger.error("No models were successfully initialized")
        raise RuntimeError("Failed to initialize any models")
    
    logger.info(f"Successfully initialized {len(models)} model(s): {list(models.keys())}")
    return models


def move_to_device(data, device: torch.device):
    """
    将数据移动到指定设备
    
    Args:
        data: 输入数据（tensor、list、tuple或dict）
        device: 目标设备
        
    Returns:
        移动后的数据
    """
    if isinstance(data, torch.Tensor):
        return data.to(device)
    elif isinstance(data, (list, tuple)):
        return type(data)(move_to_device(item, device) for item in data)
    elif isinstance(data, dict):
        return {key: move_to_device(value, device) for key, value in data.items()}
    else:
        return data