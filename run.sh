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
    echo "请参考 SETUP_TOKEN.md 文档配置您的Token"
    echo "应用将启动但AI超分功能需要配置Token后才能使用"
else
    echo "✅ HF_API_TOKEN 已配置"
fi
echo

# 启动应用
echo "启动超分辨率应用..."
echo "应用将在 http://localhost:5001 启动"
echo "按 Ctrl+C 停止应用"
echo
python app.py