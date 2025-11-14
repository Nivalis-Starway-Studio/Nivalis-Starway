@echo off
REM 班级管理系统 - Windows打包脚本
REM Classroom Manager Application - Windows Build Script

echo.
echo ============================================================
echo 班级管理系统 - 打包为exe
echo ============================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误: 找不到Python，请先安装Python 3.8+
    echo 访问: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python已安装

REM 创建虚拟环境
if not exist "venv" (
    echo.
    echo 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境已创建
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 升级pip
echo.
echo 升级pip...
python -m pip install --upgrade pip -q

REM 安装依赖
echo.
echo 安装依赖库...
pip install pyinstaller openpyxl matplotlib -q
if errorlevel 1 (
    echo ✗ 依赖安装失败
    pause
    exit /b 1
)
echo ✓ 依赖已安装

REM 运行打包脚本
echo.
echo 开始打包...
python build_exe.py

REM 检查是否成功
if exist "dist\ClassManagerApp.exe" (
    echo.
    echo ============================================================
    echo ✓ 打包成功！
    echo ============================================================
    echo 文件位置: dist\ClassManagerApp.exe
    echo.
    echo 下一步:
    echo 1. 您可以直接运行: dist\ClassManagerApp.exe
    echo 2. 或将ClassManagerApp.exe复制到其他位置使用
    echo.
    echo 登录凭证:
    echo   账号: xigua
    echo   密码: 123456
    echo ============================================================
    echo.
    pause
) else (
    echo.
    echo ✗ 打包失败，请检查错误信息
    echo.
    pause
    exit /b 1
)
