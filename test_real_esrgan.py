#!/usr/bin/env python3
# test_real_esrgan.py - 测试项目中实际使用的Real-ESRGAN模型

import requests
import os
import json
from PIL import Image
import io
import base64

# 使用项目中实际使用的模型
HF_API_URL = "https://api-inference.huggingface.co/models/ai-forever/Real-ESRGAN"
HF_API_TOKEN = os.getenv('HF_API_TOKEN', 'your_token_here')

def test_real_esrgan_model():
    """测试Real-ESRGAN模型可用性"""
    print("=== Real-ESRGAN 模型测试 ===")
    print(f"模型URL: {HF_API_URL}")
    print()
    
    if HF_API_TOKEN == 'your_token_here':
        print("❌ API Token未配置")
        print("请设置环境变量: export HF_API_TOKEN=your_actual_token")
        return False
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    
    print("1. 测试模型可用性...")
    try:
        response = requests.head(HF_API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Real-ESRGAN模型可用")
            return True
        elif response.status_code == 404:
            print("❌ Real-ESRGAN模型不存在或不支持Inference API")
            print("💡 这可能是因为该模型未部署到Inference Providers")
            return False
        elif response.status_code == 401:
            print("❌ 认证失败，请检查API Token")
            return False
        else:
            print(f"⚠️  未知状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_without_token():
    """测试无token访问"""
    print("\n2. 测试无token访问...")
    try:
        response = requests.head(HF_API_URL, timeout=10)
        
        if response.status_code == 401:
            print("✅ 正常返回401，需要认证")
        elif response.status_code == 404:
            print("❌ 返回404，模型不存在")
        else:
            print(f"⚠️  状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")

def create_test_image():
    """创建测试图像"""
    # 创建一个小的测试图像
    img = Image.new('RGB', (32, 32), color='blue')
    
    # 保存为字节流
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

def test_super_resolution():
    """测试图像超分功能"""
    print("\n3. 测试图像超分功能...")
    
    if HF_API_TOKEN == 'your_token_here':
        print("❌ 需要配置API Token")
        return False
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    
    try:
        # 创建测试图像
        test_image = create_test_image()
        
        # 发送超分请求
        response = requests.post(HF_API_URL, headers=headers, data=test_image, timeout=60)
        
        if response.status_code == 200:
            print("✅ 超分处理成功")
            print(f"响应大小: {len(response.content)} bytes")
            return True
        elif response.status_code == 404:
            print("❌ 模型不支持此操作")
            return False
        elif response.status_code == 503:
            print("⚠️  模型正在加载中，请稍后重试")
            return False
        else:
            print(f"❌ 处理失败，状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 处理异常: {e}")
        return False

def analyze_deployment_necessity():
    """分析部署必要性"""
    print("\n=== 部署必要性分析 ===")
    
    model_available = test_real_esrgan_model()
    test_without_token()
    processing_works = test_super_resolution() if model_available else False
    
    print("\n📊 分析结果:")
    
    if model_available and processing_works:
        print("✅ Real-ESRGAN模型在本地完全可用")
        print("✅ 不是必须部署到Render才能看到效果")
        print("\n💡 建议:")
        print("- 本地开发完全可行")
        print("- 部署到Render主要为了生产环境稳定性")
    elif model_available:
        print("⚠️  模型可访问但处理功能有问题")
        print("💡 可能需要调试API调用方式")
    else:
        print("❌ Real-ESRGAN模型在本地不可用")
        print("✅ 建议部署到Render以获得更好的API访问")
        print("\n💡 可能的原因:")
        print("- 模型未部署到Inference Providers")
        print("- 网络连接问题")
        print("- API Token权限不足")
        print("\n🔧 解决方案:")
        print("- 部署到Render获得更稳定的网络")
        print("- 或者尝试修复本地API配置")
    
    return model_available and processing_works

if __name__ == "__main__":
    analyze_deployment_necessity()