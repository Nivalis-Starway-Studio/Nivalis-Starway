#!/usr/bin/env python3
"""
测试脚本 - 验证应用功能
Test script - Verify application functionality
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试所有必要的导入"""
    print("测试导入...")
    
    try:
        import tkinter as tk
        print("✓ tkinter 导入成功")
    except ImportError as e:
        print(f"✗ tkinter 导入失败: {e}")
        return False
    
    try:
        from openpyxl import Workbook
        print("✓ openpyxl 导入成功")
    except ImportError as e:
        print(f"✗ openpyxl 导入失败: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib 导入成功")
    except ImportError as e:
        print(f"✗ matplotlib 导入失败: {e}")
        return False
    
    try:
        from data.models import Student, Classroom
        print("✓ 数据模型导入成功")
    except ImportError as e:
        print(f"✗ 数据模型导入失败: {e}")
        return False
    
    try:
        from data.store import ClassDataStore
        print("✓ 数据存储导入成功")
    except ImportError as e:
        print(f"✗ 数据存储导入失败: {e}")
        return False
    
    try:
        from ui.login_view import LoginView
        print("✓ 登录视图导入成功")
    except ImportError as e:
        print(f"✗ 登录视图导入失败: {e}")
        return False
    
    try:
        from ui.main_view import MainView
        print("✓ 主视图导入成功")
    except ImportError as e:
        print(f"✗ 主视图导入失败: {e}")
        return False
    
    try:
        from ui.class_detail_view import ClassDetailView
        print("✓ 班级详情视图导入成功")
    except ImportError as e:
        print(f"✗ 班级详情视图导入失败: {e}")
        return False
    
    return True

def test_basic_functionality():
    """测试基本功能"""
    print("\n测试基本功能...")
    
    try:
        from data.models import Student, Classroom
        
        # 测试学生模型
        student = Student(name="测试学生", student_id="test_001")
        print(f"✓ 学生模型创建成功: {student.name}")
        
        # 测试班级模型
        classroom = Classroom(name="测试班级", class_id="class_001")
        classroom.add_student(student)
        print(f"✓ 班级模型创建成功: {classroom.name}, 学生数: {len(classroom.get_all_students())}")
        
        # 测试数据存储
        from data.store import ClassDataStore
        store = ClassDataStore()
        store.add_classroom("测试班级2")
        print("✓ 数据存储功能正常")
        
        return True
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 班级管理系统功能测试 ===")
    
    if not test_imports():
        print("\n❌ 导入测试失败，请检查依赖库安装")
        return False
    
    if not test_basic_functionality():
        print("\n❌ 基本功能测试失败")
        return False
    
    print("\n✅ 所有测试通过！应用可以正常运行。")
    print("\n启动应用请运行: python3 main.py")
    print("登录账号: xigua / 123456")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)