#!/usr/bin/env python3
"""
应用启动器 - 适用于PyInstaller打包
Application launcher - Optimized for PyInstaller
"""

import sys
import os

# 添加当前目录到Python路径 / Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 对于PyInstaller打包，调整路径 / For PyInstaller packaging, adjust paths
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # 运行打包后的exe / Running packaged exe
    sys.path.insert(0, os.path.join(sys._MEIPASS, 'tools', 'class-manager-app'))

from main import main

if __name__ == "__main__":
    main()
