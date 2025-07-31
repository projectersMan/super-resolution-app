#!/bin/bash

# run.sh - 启动超分辨率应用

echo "=== 超分辨率应用启动脚本 ==="
echo

# 检查并释放端口5001
echo "检查端口5001占用情况..."
PORT_PID=$(lsof -ti:5001)
if [ ! -z "$PORT_PID" ]; then
    echo "发现端口5001被进程 $PORT_PID 占用，正在释放..."
    kill -9 $PORT_PID
    sleep 2
    echo "✅ 端口5001已释放"
else
    echo "✅ 端口5001未被占用"
fi
echo

# 激活conda环境
echo "激活conda环境..."
source ./activate_env.sh
echo

# 加载.env文件中的环境变量
if [ -f ".env" ]; then
    echo "加载.env文件中的环境变量..."
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ 环境变量已加载"
else
    echo "⚠️  .env文件不存在"
fi
echo

# 检查HF_API_TOKEN环境变量
echo "检查环境变量配置..."
if [ -z "$HF_API_TOKEN" ]; then
    echo "⚠️  警告: HF_API_TOKEN 环境变量未设置"
    echo "请设置您的Hugging Face API Token:"
    echo "export HF_API_TOKEN=your_huggingface_token_here"
    echo
    echo "或者创建.env文件:"
    echo "cp .env.example .env"
    echo "# 然后编辑.env文件填入您的Token"
    echo
    read -p "是否要临时设置Token? (y/n): " set_token
    if [[ $set_token == "y" || $set_token == "Y" ]]; then
        read -p "请输入您的Hugging Face Token: " temp_token
        export HF_API_TOKEN=$temp_token
        echo "✅ 临时Token已设置"
    else
        echo "⚠️  继续运行但API功能可能不可用"
    fi
else
    echo "✅ HF_API_TOKEN 已配置"
fi
echo

# 进入应用目录
cd super_resolution_app

# 启动应用
echo "启动超分辨率应用..."
echo "应用将在 http://localhost:5001 启动"
echo "按 Ctrl+C 停止应用"
echo
python app.py