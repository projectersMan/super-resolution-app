#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试bicubic插值功能
"""

import requests
import base64
import time
from PIL import Image
import io

def create_test_image():
    """创建一个简单的测试图片"""
    img = Image.new('RGB', (50, 50), color='red')
    # 添加一些细节
    for x in range(10, 40):
        for y in range(10, 40):
            if (x + y) % 10 < 5:
                img.putpixel((x, y), (0, 255, 0))  # 绿色
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()

def test_interpolation_methods():
    """测试不同的插值方法"""
    base_url = "http://localhost:5001"
    
    # 创建测试图片
    test_image_data = create_test_image()
    
    methods = [
        ('lanczos', 'Lanczos插值'),
        ('bicubic', 'Bicubic双立方插值')
    ]
    
    scale_factors = [2, 3, 4]
    
    print("🧪 开始测试不同插值方法...\n")
    
    for method, method_name in methods:
        print(f"📋 测试 {method_name}:")
        
        for scale in scale_factors:
            print(f"  🔄 {scale}倍放大测试...")
            
            # 准备请求数据
            files = {'image': ('test.png', test_image_data, 'image/png')}
            data = {
                'method': method,
                'scale_factor': str(scale)
            }
            
            start_time = time.time()
            
            try:
                response = requests.post(f"{base_url}/upscale", files=files, data=data)
                result = response.json()
                
                if result.get('success'):
                    processing_time = time.time() - start_time
                    print(f"    ✅ 成功! 处理时间: {processing_time:.3f}秒")
                    print(f"       原始大小: {result.get('original_size')} bytes")
                    print(f"       结果大小: {result.get('result_size')} bytes")
                    print(f"       使用方法: {result.get('method')}")
                    print(f"       放大倍数: {result.get('scale_factor')}x")
                else:
                    print(f"    ❌ 失败: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                print(f"    ❌ 请求失败: {e}")
            
            print()
        
        print()

def main():
    print("🚀 Bicubic插值功能测试\n")
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(2)
    
    try:
        # 检查服务器状态
        response = requests.get("http://localhost:5001/health")
        if response.status_code == 200:
            print("✅ 服务器运行正常\n")
        else:
            print("❌ 服务器状态异常")
            return
    except:
        print("❌ 无法连接到服务器")
        return
    
    # 测试插值方法
    test_interpolation_methods()
    
    print("🎉 测试完成!")

if __name__ == "__main__":
    main()