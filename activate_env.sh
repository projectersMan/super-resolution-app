#!/bin/bash

# activate_env.sh - 检查并激活hfdemo项目环境

# 项目名称（与文件夹名称一致）
PROJECT_NAME="hfdemo"

# 检查conda是否安装
if ! command -v conda &> /dev/null; then
    echo "错误: conda未安装或未在PATH中"
    exit 1
fi

# 检查项目环境是否存在
if conda info --envs | grep -q "^${PROJECT_NAME} "; then
    echo "激活conda环境: ${PROJECT_NAME}"
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate ${PROJECT_NAME}
    
    # 验证环境是否激活成功
    if [[ "$CONDA_DEFAULT_ENV" == "$PROJECT_NAME" ]]; then
        echo "环境激活成功: $CONDA_DEFAULT_ENV"
        
        # 检查requirements.txt是否存在并安装依赖
        if [ -f "super_resolution_app/requirements.txt" ]; then
            echo "检查并安装依赖..."
            pip install -r super_resolution_app/requirements.txt
        fi
        
        return 0 2>/dev/null || exit 0
    else
        echo "错误: 环境激活失败"
        return 1 2>/dev/null || exit 1
    fi
else
    echo "错误: conda环境 '${PROJECT_NAME}' 不存在"
    echo "请先创建环境: conda create -n ${PROJECT_NAME} python=3.9"
    return 1 2>/dev/null || exit 1
fi
