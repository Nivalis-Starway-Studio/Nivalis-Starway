#!/bin/bash
# 班级管理系统 - 应用启动脚本
# Classroom Manager Application - Startup Script

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 进入项目目录
cd "$SCRIPT_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    echo "激活虚拟环境..."
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt -q
else
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 运行应用
echo "启动班级管理系统..."
python3 tools/class-manager-app/main.py
