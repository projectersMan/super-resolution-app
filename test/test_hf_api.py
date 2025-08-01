#!/usr/bin/env python3
# test_hf_api.py - 测试Hugging Face超分辨率模型

import requests
import os
import json
import base64
from PIL import Image
import io

# 从环境变量读取API Token
HF_API_TOKEN = os.getenv('HF_API_TOKEN', 'your_token_here')

def test_super_resolution_models():
    """测试多个超分辨率模型的可用性"""
    print("=== Hugging Face 超分辨率模型测试 ===")
    print()
    
    if HF_API_TOKEN == 'your_token_here':
        print("❌ API Token未配置")
        print("请设置环境变量: export HF_API_TOKEN=your_actual_token")
        return False
    
    # 测试模型列表
    models = [
        "Salesforce/blip-image-captioning-base",
        "microsoft/DiT-XL-2-256", 
        "runwayml/stable-diffusion-v1-5"
    ]
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    available_models = []
    
    for model in models:
        print(f"测试模型: {model}")
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        
        try:
            # 发送HEAD请求检查模型可用性
            response = requests.head(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {model} - 可用")
                available_models.append(model)
            elif response.status_code == 404:
                print(f"❌ {model} - 不存在或不支持Inference API")
            elif response.status_code == 401:
                print(f"❌ {model} - 认证失败")
            else:
                print(f"⚠️  {model} - 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {model} - 连接失败: {e}")
        
        print()
    
    print("=== 测试总结 ===")
    if available_models:
        print(f"✅ 找到 {len(available_models)} 个可用模型:")
        for model in available_models:
            print(f"  - {model}")
    else:
        print("❌ 没有找到可用的模型")
    
    return len(available_models) > 0

def create_test_image():
    """创建测试图像"""
    # 创建一个简单的测试图像
    img = Image.new('RGB', (64, 64), color='red')
    
    # 保存为字节流
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def test_image_processing():
    """测试图像处理功能"""
    print("\n=== 图像处理测试 ===")
    
    if HF_API_TOKEN == 'your_token_here':
        print("❌ 需要配置API Token才能测试图像处理")
        return False
    
    # 使用一个已知可用的图像分类模型进行测试
    api_url = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    
    try:
        # 创建测试图像
        test_image = create_test_image()
        
        # 发送请求
        response = requests.post(api_url, headers=headers, data=test_image, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 图像处理测试成功")
            print(f"测试结果: {result[:2] if isinstance(result, list) else result}")
            return True
        else:
            print(f"❌ 图像处理失败，状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 图像处理异常: {e}")
        return False

if __name__ == "__main__":
    model_test_result = test_super_resolution_models()
    image_test_result = test_image_processing()
    
    print("\n=== 最终分析 ===")
    if model_test_result and image_test_result:
        print("✅ 所有测试通过，API功能正常")
    elif model_test_result:
        print("⚠️  模型可用但图像处理有问题")
    elif image_test_result:
        print("⚠️  图像处理正常但超分辨率模型不可用")
    else:
        print("❌ 所有测试失败，建议检查网络和Token配置")