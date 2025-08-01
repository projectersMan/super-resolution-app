import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import logging
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Hugging Face配置
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-x4-upscaler"
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

# 支持的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file_data):
    """验证图片文件是否有效"""
    assert file_data, "图片数据为空"
    
    # 尝试打开图片验证格式
    img = Image.open(io.BytesIO(file_data))
    assert img.format.lower() in ['png', 'jpeg', 'jpg', 'gif', 'bmp', 'webp'], f"不支持的图片格式: {img.format}"
    
    # 检查图片尺寸
    width, height = img.size
    assert width > 0 and height > 0, "无效的图片尺寸"
    assert width <= 4096 and height <= 4096, "图片尺寸过大，最大支持4096x4096"
    
    logger.info(f"图片验证通过: {img.format}, 尺寸: {width}x{height}")
    return True

def upscale_image(image_data, max_retries=3):
    """使用Hugging Face API进行超分辨率处理"""
    assert HF_API_TOKEN, "HF_API_TOKEN环境变量未设置"
    assert image_data, "图片数据为空"
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/octet-stream",
        "User-Agent": "AI-Upscaler/1.0"
    }
    
    for attempt in range(max_retries):
        start_time = time.time()
        logger.info(f"开始第 {attempt + 1} 次API调用...")
        
        response = requests.post(
            HF_API_URL,
            headers=headers,
            data=image_data,
            timeout=120
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"API调用完成，耗时: {elapsed_time:.2f}秒，状态码: {response.status_code}")
        
        if response.status_code == 200:
            assert response.content, "API返回空内容"
            logger.info(f"超分处理成功，返回数据大小: {len(response.content)} bytes")
            return response.content
        elif response.status_code == 503 and attempt < max_retries - 1:
            wait_time = 2 ** attempt
            logger.warning(f"模型加载中，等待 {wait_time} 秒后重试...")
            time.sleep(wait_time)
            continue
        else:
            error_msg = f"API调用失败: {response.status_code} - {response.text}"
            logger.error(error_msg)
            assert False, error_msg

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    start_time = time.time()
    
    # 验证请求
    assert 'image' in request.files, "请选择图片文件"
    
    file = request.files['image']
    assert file.filename, "未选择图片"
    assert allowed_file(file.filename), f"不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # 验证文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    assert file_size <= MAX_FILE_SIZE, f"图片文件过大，请选择小于{MAX_FILE_SIZE // (1024*1024)}MB的图片"
    assert file_size > 0, "图片文件为空"
    
    logger.info(f"接收到文件: {file.filename}, 大小: {file_size} bytes")
    
    # 读取并验证图片数据
    image_data = file.read()
    validate_image(image_data)
    
    # 调用AI超分
    result = upscale_image(image_data)
    
    # 转换为base64返回给前端
    encoded_image = base64.b64encode(result).decode('utf-8')
    
    total_time = time.time() - start_time
    logger.info(f"处理完成，总耗时: {total_time:.2f}秒")
    
    return jsonify({
        'success': True,
        'image': f'data:image/png;base64,{encoded_image}',
        'processing_time': round(total_time, 2),
        'original_size': file_size,
        'result_size': len(result)
    })

@app.errorhandler(AssertionError)
def handle_assertion_error(e):
    """处理断言错误"""
    error_msg = str(e) if str(e) else "请求参数错误"
    logger.warning(f"断言错误: {error_msg}")
    return jsonify({'error': error_msg}), 400

@app.errorhandler(Exception)
def handle_general_error(e):
    """处理一般错误"""
    logger.error(f"服务器错误: {str(e)}", exc_info=True)
    return jsonify({'error': '服务器内部错误，请稍后重试'}), 500

@app.route('/health')
def health():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'hf_token_configured': bool(HF_API_TOKEN)
    })

@app.route('/info')
def info():
    """应用信息接口"""
    return jsonify({
        'name': 'AI图像超分辨率应用',
        'version': '1.0.0',
        'model': 'stabilityai/stable-diffusion-x4-upscaler',
        'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024),
        'supported_formats': list(ALLOWED_EXTENSIONS)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
