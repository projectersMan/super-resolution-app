import os
import io
import base64
import requests
from flask import Flask, render_template, request, jsonify
from PIL import Image
import logging
from datetime import datetime
import time

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face配置 - 使用支持Inference API的RealESRGAN模型
HF_API_URL = "https://api-inference.huggingface.co/models/ai-forever/Real-ESRGAN"
HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")

def upscale_image_with_hf(image_data, max_retries=3):
    """使用Hugging Face API进行超分辨率处理"""
    import time

    for attempt in range(max_retries):
        try:
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            # 创建会话并配置重试策略
            session = requests.Session()
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            headers = {
                "Authorization": f"Bearer {HF_API_TOKEN}",
                "Content-Type": "application/octet-stream",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }

            logger.info(f"尝试第 {attempt + 1} 次调用 Hugging Face API...")

            # 发送请求到Hugging Face
            response = session.post(
                HF_API_URL,
                headers=headers,
                data=image_data,
                timeout=(30, 180),  # (连接超时, 读取超时)
                stream=False
            )

            if response.status_code == 200:
                logger.info("Hugging Face API调用成功")
                return response.content
            elif response.status_code == 503:
                logger.warning(f"模型正在加载中，状态码: {response.status_code}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 递增等待时间
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
            else:
                logger.error(f"HF API Error: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # 短暂等待后重试
                    continue

        except requests.exceptions.ConnectionError as e:
            logger.error(f"连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                logger.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
        except requests.exceptions.Timeout as e:
            logger.error(f"请求超时 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(10)
                continue
        except Exception as e:
            logger.error(f"未知错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue

    logger.error(f"所有 {max_retries} 次尝试都失败了")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    start_time = time.time()
    try:
        # 检查是否有文件上传
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # 验证文件大小 (限制为5MB)
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        
        if file_length > 5 * 1024 * 1024:
            return jsonify({'error': 'Image size too large. Maximum 5MB allowed.'}), 400
        
        # 读取图片
        image_bytes = file.read()
        
        # 调用Hugging Face API进行超分
        upscaled_image = upscale_image_with_hf(image_bytes)
        
        if upscaled_image:
            # 将结果转换为base64编码以便前端显示
            encoded_image = base64.b64encode(upscaled_image).decode('utf-8')
            
            processing_time = time.time() - start_time
            logger.info(f"Image upscaled successfully in {processing_time:.2f} seconds")
            
            return jsonify({
                'success': True,
                'upscaled_image': f'image/jpeg;base64,{encoded_image}',
                'processing_time': round(processing_time, 2)
            })
        else:
            return jsonify({'error': 'Failed to upscale image. Please try again.'}), 500
            
    except Exception as e:
        logger.error(f"Error in upscale route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/info')
def info():
    return jsonify({
        'app_name': 'AI Super Resolution',
        'description': 'Image upscaling using Hugging Face AI models',
        'model': 'microsoft/swin2SR-classical-sr-x2-64'
    })

@app.route('/test-api')
def test_api():
    """测试Hugging Face API连接"""
    try:
        import requests
        headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

        # 简单的GET请求测试API连接
        response = requests.get(
            "https://api-inference.huggingface.co/models/microsoft/swin2SR-classical-sr-x2-64",
            headers=headers,
            timeout=10
        )

        return jsonify({
            'api_status': 'connected',
            'status_code': response.status_code,
            'token_valid': bool(HF_API_TOKEN),
            'response_headers': dict(response.headers)
        })
    except Exception as e:
        return jsonify({
            'api_status': 'error',
            'error': str(e),
            'token_valid': bool(HF_API_TOKEN)
        }), 500

if __name__ == '__main__':
    # Render部署配置
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)