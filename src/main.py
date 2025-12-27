import os
import sys
#添加上级目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from src.api.v1.routes import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Orchid Detector")
    
    
    # Include API routes
    app.include_router(api_router, prefix="/api/v1")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)