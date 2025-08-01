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

def upscale_image(image_data, method='lanczos', scale_factor=2):
    """使用本地PIL进行图像超分辨率处理"""
    assert image_data, "图片数据为空"
    assert method in ['lanczos', 'bicubic'], "插值方法必须是lanczos或bicubic"
    assert scale_factor in [2, 3, 4], "放大倍数必须是2、3或4"
    
    try:
        # 打开原始图片
        img = Image.open(io.BytesIO(image_data))
        original_size = img.size
        logger.info(f"原始图片尺寸: {original_size}，使用{method}插值，{scale_factor}倍放大")
        
        # 根据选择的插值方法进行放大
        new_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)
        
        if method == 'bicubic':
            upscaled_img = img.resize(new_size, Image.Resampling.BICUBIC)
            logger.info("使用双立方插值进行图像放大")
        else:  # lanczos
            upscaled_img = img.resize(new_size, Image.Resampling.LANCZOS)
            logger.info("使用Lanczos插值进行图像放大")
        
        # 应用图像增强
        from PIL import ImageFilter, ImageEnhance
        
        # 轻微锐化
        upscaled_img = upscaled_img.filter(ImageFilter.SHARPEN)
        
        # 增强对比度
        enhancer = ImageEnhance.Contrast(upscaled_img)
        upscaled_img = enhancer.enhance(1.05)
        
        # 转换为字节数据
        output_buffer = io.BytesIO()
        # 保持原始格式，如果是JPEG则使用高质量
        if img.format == 'JPEG':
            upscaled_img.save(output_buffer, format='JPEG', quality=95, optimize=True)
        else:
            upscaled_img.save(output_buffer, format='PNG', optimize=True)
        
        result_data = output_buffer.getvalue()
        logger.info(f"超分处理成功，新尺寸: {new_size}，输出大小: {len(result_data)} bytes")
        return result_data
        
    except Exception as e:
        error_msg = f"本地图像处理失败: {str(e)}"
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
    
    # 获取插值方法和放大倍数参数
    method = request.form.get('method', 'lanczos').lower()
    scale_factor = int(request.form.get('scale_factor', 2))
    
    logger.info(f"使用插值方法: {method}, 放大倍数: {scale_factor}")
    
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
    
    # 调用本地超分处理，传入插值方法和放大倍数
    result = upscale_image(image_data, method=method, scale_factor=scale_factor)
    
    # 转换为base64返回给前端
    encoded_image = base64.b64encode(result).decode('utf-8')
    
    total_time = time.time() - start_time
    logger.info(f"处理完成，总耗时: {total_time:.2f}秒")
    
    return jsonify({
        'success': True,
        'image': f'data:image/png;base64,{encoded_image}',
        'processing_time': round(total_time, 2),
        'original_size': file_size,
        'result_size': len(result),
        'method': method,
        'scale_factor': scale_factor
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
        'processing_method': 'PIL本地处理',
        'supported_interpolation': ['lanczos', 'bicubic'],
        'supported_scale_factors': [2, 3, 4],
        'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024),
        'supported_formats': list(ALLOWED_EXTENSIONS),
        'features': {
            'lanczos_interpolation': '高质量Lanczos插值算法',
            'bicubic_interpolation': '双立方插值算法',
            'image_enhancement': '自动锐化和对比度增强',
            'multiple_scale_factors': '支持2倍、3倍、4倍放大'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
