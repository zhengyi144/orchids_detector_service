import yaml
import os
import cv2
import torch
from src.utils.logging import *

logger = logging.getLogger(__name__)

def load_model_config(config_path: str = "src/config/model_config.yaml") -> dict:
    """
    加载模型配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        dict: 模型配置字典
    """
    try:
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Model config loaded from {config_path}")
        return config
    
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise

def preprocess_image(image, target_size=(640, 640)):
    """
    预处理图像以适应模型输入要求
    
    Args:
        image: 输入图像（numpy数组）
        target_size: 目标尺寸（宽, 高）     
    Returns:
        预处理后的图像      
    """
    # 调整图像大小
    image_resized = cv2.resize(image, target_size)
    # 转换为RGB格式
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    # 归一化到[0, 1]
    image_normalized = image_rgb / 255.0
    # 转换为张量并添加批次维度
    image_tensor = torch.from_numpy(image_normalized).permute(2, 0, 1).unsqueeze(0).float()
    return image_tensor

def draw_predictions(image, results, target_size=(640, 640), conf_threshold: float = 0.7):
    """
    在图像上绘制预测结果
    
    Args:
        image: 原始图像
        results: YOLO预测结果
        
    Returns:
        (annotated_image, detections):
            annotated_image 为按原图尺寸绘制了检测框的图像
            detections 为基于原图坐标的检测结果列表
    """
    # 原图尺寸
    orig_h, orig_w = image.shape[:2]
    target_w, target_h = target_size

    # 预处理阶段将原图拉伸为 target_size，这里反向缩放回原图坐标
    scale_x = target_w / orig_w
    scale_y = target_h / orig_h

    # 复制原图以避免修改原图
    annotated_image = image.copy()
    detections = []
    
    # 遍历检测结果
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 获取在预处理后(640x640)图像上的边界框坐标
            x1_r, y1_r, x2_r, y2_r = box.xyxy[0].cpu().numpy().astype(float)

            # 反算到原图坐标系
            x1 = int(x1_r / scale_x)
            y1 = int(y1_r / scale_y)
            x2 = int(x2_r / scale_x)
            y2 = int(y2_r / scale_y)
            # 获取置信度和类别
            conf = float(box.conf[0])
            # 过滤低置信度检测
            if conf < conf_threshold:
                continue

            cls = int(box.cls[0])
            class_name = result.names[cls]

            detection = {
                "class": class_name,
                "confidence": conf,
                "bbox": {
                    "x1": int(x1),
                    "y1": int(y1),
                    "x2": int(x2),
                    "y2": int(y2)
                }
            }
            detections.append(detection)
            # 绘制边界框
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # 绘制标签和置信度
            label = f"{class_name}: {conf:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(annotated_image, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (0, 255, 0), -1)
            cv2.putText(annotated_image, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    return annotated_image,detections