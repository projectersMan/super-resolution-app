#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Stable Diffusion X4 Upscaler 模型
验证本地环境是否可以调用 Hugging Face Inference API
"""

import requests
import os
import json
from PIL import Image
import io
import base64

def test_model_availability(model_name, api_token=None):
    """测试模型是否可用"""
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"模型 {model_name} 状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 模型可用")
            return True
        elif response.status_code == 404:
            print("❌ 模型不存在或不支持 Inference API")
        elif response.status_code == 401:
            print("❌ 需要有效的 API Token")
        else:
            print(f"❌ 其他错误: {response.text}")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def create_test_image():
    """创建一个简单的测试图像"""
    from PIL import Image, ImageDraw
    
    # 创建一个 64x64 的小图像
    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    
    # 画一个简单的图案
    draw.rectangle([10, 10, 54, 54], fill='blue', outline='red', width=2)
    draw.ellipse([20, 20, 44, 44], fill='yellow')
    
    return img

def test_upscale_api(model_name, api_token=None):
    """测试图像超分 API"""
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Content-Type": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    
    # 创建测试图像
    test_img = create_test_image()
    
    # 将图像转换为 base64
    buffer = io.BytesIO()
    test_img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # 准备请求数据
    data = {
        "inputs": img_base64,
        "parameters": {
            "prompt": "high quality, detailed"
        }
    }
    
    try:
        print(f"\n测试 {model_name} 超分功能...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API 调用成功!")
            # 检查响应内容
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                print("✅ 返回了图像数据")
                # 保存结果图像
                with open('upscaled_result.png', 'wb') as f:
                    f.write(response.content)
                print("✅ 超分结果已保存为 upscaled_result.png")
            else:
                print(f"响应内容类型: {content_type}")
                print(f"响应内容: {response.text[:500]}")
        else:
            print(f"❌ API 调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def main():
    print("=== 测试 Stable Diffusion X4 Upscaler 模型 ===")
    
    # 从环境变量获取 API Token
    api_token = os.environ.get('HF_API_TOKEN')
    if api_token:
        print(f"✅ 找到 API Token: {api_token[:10]}...")
    else:
        print("⚠️  未找到 HF_API_TOKEN 环境变量")
    
    # 测试模型
    model_name = "stabilityai/stable-diffusion-x4-upscaler"
    
    print(f"\n1. 测试模型可用性: {model_name}")
    is_available = test_model_availability(model_name, api_token)
    
    if is_available:
        print(f"\n2. 测试超分功能")
        test_upscale_api(model_name, api_token)
    else:
        print("\n❌ 模型不可用，跳过功能测试")
    
    print("\n=== 分析结果 ===")
    if is_available:
        print("✅ 模型在 Hugging Face Inference API 上可用")
        print("✅ 本地环境可以调用 Hugging Face API")
        print("📝 结论: 不需要部署到 Render 就可以使用超分功能")
        print("💡 建议: 确保本地有正确的 HF_API_TOKEN 环境变量")
    else:
        print("❌ 模型在本地测试中不可用")
        print("📝 可能的原因:")
        print("   - 模型不支持 Inference API")
        print("   - 需要有效的 API Token")
        print("   - 网络连接问题")
        print("💡 建议: 部署到 Render 可能提供更稳定的网络环境")

if __name__ == "__main__":
    main()