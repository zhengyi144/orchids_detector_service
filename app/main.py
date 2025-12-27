"""
Main Flask application
"""

from flask import Flask, render_template
from flask_cors import CORS
from app.routes import api_bp
import os


def create_app():
    """
    Create and configure Flask application.
    
    Returns:
        Configured Flask app
    """
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Root route
    @app.route('/')
    def index():
        """Home page"""
        try:
            return render_template('index.html')
        except:
            return """
            <html>
                <head><title>Orchid Detection Service</title></head>
                <body>
                    <h1>兰花检测服务 (Orchid Detection Service)</h1>
                    <p>API 端点:</p>
                    <ul>
                        <li>GET /api/health - 健康检查</li>
                        <li>POST /api/detect - 检测兰花 (上传图片)</li>
                        <li>GET /api/species - 获取支持的品种列表</li>
                        <li>GET /api/info - 获取服务信息</li>
                    </ul>
                </body>
            </html>
            """
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
