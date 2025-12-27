# Orchid Detection Service

兰花检测服务 - 基于深度学习的兰花品种识别系统

## 功能特点

- 🌸 支持多种兰花品种识别
- 📷 支持图片上传和实时检测
- 🎯 提供置信度评分
- 🌐 提供 REST API 接口
- 🐳 支持 Docker 容器化部署

## 支持的兰花品种

- 蝴蝶兰 (Phalaenopsis)
- 石斛兰 (Dendrobium)
- 卡特兰 (Cattleya)
- 蕙兰 (Cymbidium)
- 文心兰 (Oncidium)
- 万代兰 (Vanda)
- 兜兰 (Paphiopedilum)

## 安装

### 使用 Docker (推荐)

```bash
# 构建并运行
docker-compose up -d

# 访问服务
# Web 界面: http://localhost:5000
# API: http://localhost:5000/api
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/zhengyi144/orchids_detector_service.git
cd orchids_detector_service

# 安装依赖
pip install -r requirements.txt

# 运行服务
python app/main.py
```

## API 使用

### 健康检查

```bash
GET /api/health
```

响应:
```json
{
  "status": "healthy",
  "service": "orchid_detector",
  "version": "1.0.0"
}
```

### 检测兰花

```bash
POST /api/detect
Content-Type: multipart/form-data

参数:
- image: 图片文件 (PNG, JPG, JPEG, GIF, BMP)
```

响应:
```json
{
  "success": true,
  "result": {
    "primary_species": "Phalaenopsis",
    "confidence": 0.92,
    "all_predictions": [
      {
        "species": "Phalaenopsis",
        "confidence": 0.92
      },
      {
        "species": "Dendrobium",
        "confidence": 0.05
      }
    ],
    "is_orchid": true
  },
  "message": "检测完成"
}
```

### 获取支持的品种列表

```bash
GET /api/species
```

响应:
```json
{
  "species": [
    "Phalaenopsis",
    "Dendrobium",
    "Cattleya",
    "Cymbidium",
    "Oncidium",
    "Vanda",
    "Paphiopedilum",
    "Unknown"
  ],
  "count": 8
}
```

### 获取服务信息

```bash
GET /api/info
```

响应:
```json
{
  "service": "Orchid Detection Service",
  "description": "兰花检测服务 - 用于识别和分类兰花品种",
  "version": "1.0.0",
  "supported_formats": ["PNG", "JPG", "JPEG", "GIF", "BMP"],
  "max_file_size": "10MB"
}
```

## 使用示例

### Python

```python
import requests

# 检测兰花
with open('orchid.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/api/detect', files=files)
    result = response.json()
    print(result)
```

### cURL

```bash
curl -X POST -F "image=@orchid.jpg" http://localhost:5000/api/detect
```

### JavaScript (Fetch)

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/api/detect', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 项目结构

```
orchids_detector_service/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask 应用主文件
│   ├── models/
│   │   ├── __init__.py
│   │   └── orchid_detector.py  # 检测模型
│   ├── routes/
│   │   ├── __init__.py
│   │   └── api.py           # API 路由
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py    # 文件处理工具
├── templates/
│   └── index.html           # Web 界面
├── static/                  # 静态文件
├── uploads/                 # 上传文件目录
├── tests/                   # 测试文件
├── Dockerfile              # Docker 配置
├── docker-compose.yml      # Docker Compose 配置
├── requirements.txt        # Python 依赖
├── wsgi.py                # WSGI 入口
└── README.md              # 项目文档
```

## 技术栈

- **后端**: Flask, PyTorch
- **深度学习**: CNN (Convolutional Neural Network)
- **图像处理**: Pillow, NumPy
- **部署**: Docker, Gunicorn

## 注意事项

- 上传图片大小限制: 10MB
- 支持的图片格式: PNG, JPG, JPEG, GIF, BMP
- 模型为演示版本，实际生产环境需要使用训练好的模型权重
- 建议使用 HTTPS 协议传输图片数据

## 开发

```bash
# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/

# 运行开发服务器
python app/main.py
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系我们。