@echo off
REM 班级管理系统 - 应用启动脚本
REM Classroom Manager Application - Startup Script

setlocal enabledelayedexpansion

REM 获取脚本目录
set "SCRIPT_DIR=%~dp0"

REM 进入项目目录
cd /d "%SCRIPT_DIR%"

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
    echo 安装依赖...
    pip install -r requirements.txt -q
) else (
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
)

REM 运行应用
echo 启动班级管理系统...
python tools/class-manager-app/main.py

pause
