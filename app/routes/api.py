"""
API Routes for orchid detection service
"""

from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from app.models import OrchidDetector
from app.utils import save_upload_file, load_image, cleanup_file, validate_image_size
import os

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize detector
detector = OrchidDetector()


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "service": "orchid_detector",
        "version": "1.0.0"
    }), 200


@api_bp.route('/detect', methods=['POST'])
def detect_orchid():
    """
    Detect orchid species from uploaded image.
    
    Expected: multipart/form-data with 'image' file field
    
    Returns:
        JSON with detection results
    """
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({
            "error": "No image file provided",
            "message": "请上传图片文件"
        }), 400
    
    file = request.files['image']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({
            "error": "Empty filename",
            "message": "文件名不能为空"
        }), 400
    
    # Save uploaded file
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    filepath = save_upload_file(file, upload_folder)
    
    if not filepath:
        return jsonify({
            "error": "Invalid file type",
            "message": "不支持的文件格式，请上传 PNG, JPG, JPEG, GIF 或 BMP 格式的图片"
        }), 400
    
    # Validate file size
    if not validate_image_size(filepath):
        cleanup_file(filepath)
        return jsonify({
            "error": "File too large",
            "message": "文件大小超过限制（最大 10MB）"
        }), 400
    
    try:
        # Load image
        image = load_image(filepath)
        if image is None:
            cleanup_file(filepath)
            return jsonify({
                "error": "Failed to load image",
                "message": "无法加载图片文件"
            }), 400
        
        # Detect orchid
        result = detector.detect(image)
        
        # Clean up uploaded file
        cleanup_file(filepath)
        
        # Return results
        return jsonify({
            "success": True,
            "result": result,
            "message": "检测完成"
        }), 200
        
    except Exception as e:
        # Clean up on error
        cleanup_file(filepath)
        return jsonify({
            "error": "Detection failed",
            "message": f"检测失败: {str(e)}"
        }), 500


@api_bp.route('/species', methods=['GET'])
def get_species():
    """
    Get list of supported orchid species.
    
    Returns:
        JSON with list of species
    """
    return jsonify({
        "species": OrchidDetector.ORCHID_SPECIES,
        "count": len(OrchidDetector.ORCHID_SPECIES)
    }), 200


@api_bp.route('/info', methods=['GET'])
def get_info():
    """
    Get service information.
    
    Returns:
        JSON with service details
    """
    return jsonify({
        "service": "Orchid Detection Service",
        "description": "兰花检测服务 - 用于识别和分类兰花品种",
        "version": "1.0.0",
        "supported_formats": ["PNG", "JPG", "JPEG", "GIF", "BMP"],
        "max_file_size": "10MB",
        "endpoints": {
            "health": "/api/health",
            "detect": "/api/detect (POST)",
            "species": "/api/species",
            "info": "/api/info"
        }
    }), 200
