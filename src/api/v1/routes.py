import logging
import base64
from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File,Form
from fastapi.responses import JSONResponse
from src.core.inference import detect_and_recognize_process

router = APIRouter()

#实现一个hello world的路由
@router.get("/hello")
async def hello_world():
    return {"message": "Hello, World!"}

# 图像检测路由
@router.post("/detectImage")
async def detect_image(
                        imageFile: UploadFile = File(...),
                        detectType: str = Form(...)
                       ):
    logger = logging.getLogger("detectImage")
    try:
        # 读取上传的文件内容
        imageBytes = await imageFile.read()
        logger.info(f"Received image file: {imageFile.filename}, size: {len(imageBytes)} bytes")

        # TODO: 在这里调用你的检测模型进行推理
        result = detect_and_recognize_process(imageBytes, detectType)
        # 将图像字节转为base64编码（便于JSON传输）
        image_base64 = base64.b64encode(result["image_bytes"]).decode('utf-8')
        #logger.info(f"Detection result: { result["detections"]}")
        
        return JSONResponse(content={
            "filename": imageFile.filename,
            "image": image_base64,
            "detections": result["detections"],
            "num_detections": result["num_detections"]
        })
        
    except Exception as e:
        logger.error(f"Error during image detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/uploadFile")
async def upload_file(file: UploadFile = File(...)):
    # 打印文件信息
    print(f"Filename: {file.filename}")
    print(f"Content type: {file.content_type}")
    print(f"File size: {file.size} bytes")

    # 读取文件内容
    content = await file.read()
    print(f"File content (first 100 bytes): {content[:100]}")

    # 返回响应
    return JSONResponse(content={"filename": file.filename, "message": "File uploaded successfully"})
