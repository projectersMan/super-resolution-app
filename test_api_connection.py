#!/usr/bin/env python3
# test_api_connection.py - 测试Hugging Face API连接

import requests
import os
import json

# 从环境变量读取API Token
HF_API_TOKEN = os.getenv('HF_API_TOKEN', 'your_token_here')

def test_hf_api_connection():
    """测试Hugging Face API基本连接性"""
    print("=== Hugging Face API 连接测试 ===")
    print()
    
    # 1. 测试API Token有效性
    print("1. 测试API Token有效性...")
    if HF_API_TOKEN == 'your_token_here':
        print("❌ API Token未配置")
        print("请设置环境变量: export HF_API_TOKEN=your_actual_token")
        return False
    
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}"
    }
    
    try:
        # 测试用户信息API
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ API Token有效，用户: {user_info.get('name', 'Unknown')}")
        else:
            print(f"❌ API Token无效，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Token验证失败: {e}")
        return False
    
    # 2. 测试网络连接
    print("\n2. 测试网络连接...")
    try:
        response = requests.get("https://api-inference.huggingface.co", timeout=10)
        print(f"✅ 网络连接正常，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    
    # 3. 测试简单的文本分类模型
    print("\n3. 测试简单的API调用...")
    try:
        api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        data = {"inputs": "I love this!"}
        
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API调用成功")
            print(f"测试结果: {result}")
        else:
            print(f"❌ API调用失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        return False
    
    print("\n=== 测试总结 ===")
    print("✅ 所有测试通过，Hugging Face API连接正常")
    return True

def analyze_deployment_necessity():
    """分析是否需要部署到Render"""
    print("\n=== 部署必要性分析 ===")
    
    if test_hf_api_connection():
        print("\n📊 分析结果:")
        print("✅ 本地环境可以正常访问Hugging Face API")
        print("✅ 不是必须部署到Render才能看到效果")
        print("\n💡 建议:")
        print("- 本地开发和测试完全可行")
        print("- 部署到Render主要是为了生产环境的稳定性")
        print("- 如果需要分享给他人使用，建议部署到Render")
    else:
        print("\n📊 分析结果:")
        print("❌ 本地环境无法正常访问Hugging Face API")
        print("✅ 建议部署到Render以获得更稳定的网络环境")
        print("\n💡 可能的问题:")
        print("- API Token配置问题")
        print("- 网络连接问题")
        print("- 防火墙或代理设置")

if __name__ == "__main__":
    analyze_deployment_necessity()