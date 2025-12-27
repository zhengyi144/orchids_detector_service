import time
import cv2
import logging
import numpy as np
from src.utils.tools import *
from src.ml.model_builder import init_models


config = load_model_config()
models= init_models(config['models'])

logger = logging.getLogger("inference")

def save_image(image):
    #提取当前时间戳作为文件名
    timestamp = int(time.time())
    filename = f"image_{timestamp}.jpg"
    imagePath = config["images"]["save_path"] + filename
    #判断路径是否存在，不存在则创建
    #os.makedirs(config["images"]["save_path"], exist_ok=True)
    cv2.imwrite(imagePath, image)
    logger.info(f"Image saved to {imagePath}")
    return imagePath

def detect_disease(model, image):
    # Make a prediction using the trained model
    processedImage = preprocess_image(image)
    prediction = model(processedImage)
    return prediction

def detect_and_recognize_process(imageBytes, projectName):
    # Main function to detect and recognize orchid diseases
    # 将字节数据转换为图像
    nparr = np.frombuffer(imageBytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # 保存图像以供调试
    save_image(image)
    #加载模型并进行预测
    model = models.get(projectName)
    prediction = detect_disease(model, image)

    #对预测结果进行处理并返回
    # 在图像上绘制预测结果
    annotatedImage,detections = draw_predictions(image, prediction)
    logger.info(f"Detections: {detections}")
    #cv2.imshow("Predictions", annotatedImage)
    #cv2.waitKey(0)
    
    # 将绘制后的图像转换为字节
    _, buffer = cv2.imencode('.jpg', annotatedImage)
    resImageBytes = buffer.tobytes()

    # 返回图像字节和检测结果
    return {
        "image_bytes": resImageBytes,
        "detections": detections,
        "num_detections": len(detections)
    }