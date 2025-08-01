#!/usr/bin/env python3
"""
部署测试脚本
用于验证应用程序的所有功能是否正常工作
"""

import requests
import time
import os
from PIL import Image
import io
import base64

def test_health_endpoint():
    """测试健康检查接口"""
    try:
        response = requests.get('http://127.0.0.1:5001/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_info_endpoint():
    """测试应用信息接口"""
    try:
        response = requests.get('http://127.0.0.1:5001/info')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 应用信息获取成功: {data}")
            return True
        else:
            print(f"❌ 应用信息获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 应用信息获取异常: {e}")
        return False

def create_test_image():
    """创建一个测试图片"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_upscale_endpoint():
    """测试图片超分接口"""
    try:
        # 创建测试图片
        test_img = create_test_image()
        
        # 准备文件上传
        files = {'image': ('test.png', test_img, 'image/png')}
        
        print("🔄 开始测试图片超分功能...")
        response = requests.post('http://127.0.0.1:5001/upscale', files=files, timeout=180)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 图片超分测试成功")
                if 'processing_time' in data:
                    print(f"   处理时间: {data['processing_time']} 秒")
                if 'original_size' in data:
                    print(f"   原始大小: {data['original_size']} bytes")
                if 'result_size' in data:
                    print(f"   结果大小: {data['result_size']} bytes")
                return True
            else:
                print(f"❌ 图片超分失败: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 图片超分请求失败: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误信息: {error_data.get('error', '未知错误')}")
            except:
                print(f"   响应内容: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 图片超分测试异常: {e}")
        return False

def test_invalid_file():
    """测试无效文件上传"""
    try:
        # 创建一个文本文件而不是图片
        files = {'image': ('test.txt', io.StringIO('not an image'), 'text/plain')}
        
        response = requests.post('http://127.0.0.1:5001/upscale', files=files)
        
        if response.status_code == 400:
            print("✅ 无效文件验证正常工作")
            return True
        else:
            print(f"❌ 无效文件验证失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无效文件测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始部署测试...\n")
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(2)
    
    tests = [
        ("健康检查", test_health_endpoint),
        ("应用信息", test_info_endpoint),
        ("无效文件验证", test_invalid_file),
        ("图片超分功能", test_upscale_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️ {test_name} 测试失败")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用程序已准备好部署。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查配置。")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)