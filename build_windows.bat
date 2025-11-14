@echo off
REM Windows批处理脚本 - 打包班级管理系统为exe文件
REM Windows batch script - Package classroom manager app as exe file

echo ============================================
echo 班级管理系统 - Windows打包脚本
echo Classroom Manager - Windows Build Script
echo ============================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    echo Error: Python not found, please install Python first
    pause
    exit /b 1
)

REM 检查是否在虚拟环境中
if not defined VIRTUAL_ENV (
    echo 创建虚拟环境...
    python -m venv venv
    echo 激活虚拟环境...
    call venv\Scripts\activate.bat
) else (
    echo 已在虚拟环境中
    echo Already in virtual environment
)

REM 安装依赖
echo 安装依赖包...
echo Installing dependencies...
pip install PyInstaller matplotlib openpyxl pillow

REM 运行打包脚本
echo 开始打包...
echo Starting build...
python build_exe.py

REM 检查打包结果
if exist "dist\ClassManagerApp.exe" (
    echo.
    echo ============================================
    echo ✓ 打包成功!
    echo ✓ Build successful!
    echo ============================================
    echo 文件位置: dist\ClassManagerApp.exe
    echo File location: dist\ClassManagerApp.exe
    echo.
    echo 使用方法:
    echo Usage:
    echo   双击运行: dist\ClassManagerApp.exe
    echo   Double click: dist\ClassManagerApp.exe
    echo.
    echo 登录凭证:
    echo Login credentials:
    echo   账号: xigua
    echo   Username: xigua
    echo   密码: 123456
    echo   Password: 123456
    echo ============================================
) else (
    echo.
    echo ✗ 打包失败，请检查错误信息
    echo ✗ Build failed, please check error messages
)

pause