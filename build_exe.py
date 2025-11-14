#!/usr/bin/env python3
"""
打包脚本 - 将班级管理系统打包成exe可执行文件
Build script - Package classroom manager app as exe executable
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    """主打包函数 / Main build function"""
    
    # 项目路径 / Project paths
    project_root = Path(__file__).parent
    app_dir = project_root / "tools" / "class-manager-app"
    main_file = app_dir / "main.py"
    output_dir = project_root / "dist"
    build_dir = project_root / "build"
    
    # 验证主文件存在 / Verify main file exists
    if not main_file.exists():
        print(f"错误: 找不到主文件 {main_file}")
        return 1
    
    print("=" * 60)
    print("班级管理系统 - 打包为exe")
    print("=" * 60)
    
    # 清理之前的构建文件 / Clean previous build files
    print("清理之前的构建文件...")
    for directory in [output_dir, build_dir]:
        if directory.exists():
            shutil.rmtree(directory)
            print(f"  已删除: {directory}")
    
    # 获取Python解释器路径 / Get Python interpreter path
    python_exe = sys.executable
    
    # PyInstaller命令 / PyInstaller command
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--onefile",  # 生成单一exe文件 / Generate single exe file
        "--windowed",  # 无控制台窗口 / No console window
        "--name", "ClassManagerApp",  # 应用名称 / App name
        "--add-data", f"{app_dir}{os.pathsep}tools/class-manager-app",  # 添加数据文件 / Add data files
        "--distpath", str(output_dir),  # 输出目录 / Output directory
        "--workpath", str(build_dir),  # 构建工作目录 / Build work directory
        "--specpath", str(project_root),  # spec文件位置 / Spec file location
        str(main_file),
    ]
    
    # 如果icon文件存在，添加icon参数 / Add icon parameter if it exists
    icon_file = project_root / "tools" / "class-manager-app" / "assets" / "icon.ico"
    if icon_file.exists():
        cmd.insert(-1, "--icon")
        cmd.insert(-1, str(icon_file))
    
    print("\n执行PyInstaller命令...")
    print(f"命令: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, cwd=str(project_root))
        
        if result.returncode == 0:
            # 在Linux上，生成的是可执行文件，不是.exe
            # 在Windows上，生成的是.exe文件
            exe_file = output_dir / "ClassManagerApp.exe"
            bin_file = output_dir / "ClassManagerApp"
            
            # 检查是否存在Windows版本（.exe）或Linux版本
            executable_file = None
            if exe_file.exists():
                executable_file = exe_file
                file_type = "Windows EXE"
            elif bin_file.exists():
                executable_file = bin_file
                file_type = "Linux Executable"
            
            if executable_file:
                print("\n" + "=" * 60)
                print("✓ 打包成功!")
                print("=" * 60)
                print(f"文件位置: {executable_file}")
                print(f"文件类型: {file_type}")
                print(f"文件大小: {executable_file.stat().st_size / (1024*1024):.2f} MB")
                print("\n使用方法:")
                if file_type == "Windows EXE":
                    print(f"  双击运行: {executable_file}")
                else:
                    print(f"  在Linux上运行: {executable_file}")
                    print(f"  或在终端中运行: ./{executable_file.name}")
                print("\n登录凭证:")
                print("  账号: xigua")
                print("  密码: 123456")
                
                # 如果在Linux上，还要提示如何在Windows上打包
                if file_type == "Linux Executable":
                    print("\n" + "=" * 60)
                    print("注意: 这是Linux版本的可执行文件")
                    print("要生成Windows版本的.exe文件，请在Windows系统上运行此脚本")
                    print("或使用以下命令（需要安装Windows版Python）:")
                    print("  python build_exe.py")
                    print("=" * 60)
                
                return 0
            else:
                print("\n✗ 打包失败: 找不到生成的可执行文件")
                return 1
        else:
            print(f"\n✗ PyInstaller执行失败，返回码: {result.returncode}")
            return 1
            
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
