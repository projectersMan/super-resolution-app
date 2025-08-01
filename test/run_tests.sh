#!/bin/bash

# run_tests.sh - 运行所有测试脚本

echo "=== 超分辨率项目测试套件 ==="
echo

# 激活conda环境
echo "激活conda环境..."
source ../activate_env.sh
echo

# 加载环境变量
if [ -f "../.env" ]; then
    echo "加载环境变量..."
    export $(cat ../.env | grep -v '^#' | xargs)
    echo "✅ 环境变量已加载"
else
    echo "⚠️  .env文件不存在，请先配置环境变量"
fi
echo

# 运行测试脚本
echo "开始运行测试..."
echo

echo "1. 测试API连接..."
python3 test_api_connection.py
echo

echo "2. 测试Hugging Face API..."
python3 test_hf_api.py
echo

echo "3. 测试Real-ESRGAN模型..."
python3 test_real_esrgan.py
echo

echo "4. 测试Stable Diffusion Upscaler..."
python3 test_stable_diffusion_upscaler.py
echo

echo "=== 测试完成 ==="