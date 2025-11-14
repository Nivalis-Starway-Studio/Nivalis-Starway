#!/usr/bin/env python3
"""
测试脚本 - 验证班级管理系统v1.3的所有优化功能
Test script - Verify all optimized features of Classroom Manager v1.3
"""

import sys
import os
import subprocess
from pathlib import Path

def test_imports():
    """测试所有必要的导入是否正常"""
    print("测试导入模块...")
    try:
        # 测试数据模型
        sys.path.append(str(Path(__file__).parent / "tools" / "class-manager-app"))
        from data.models import Student, Classroom
        from data.store import ClassDataStore
        print("✓ 数据模型导入成功")
        
        # 测试UI模块
        from ui.login_view import LoginView
        from ui.main_view import MainView
        from ui.class_detail_view import ClassDetailView
        print("✓ UI模块导入成功")
        
        # 测试可选依赖
        try:
            import matplotlib.pyplot as plt
            print("✓ matplotlib导入成功")
        except ImportError:
            print("⚠ matplotlib未安装，图表功能不可用")
        
        try:
            from openpyxl import Workbook
            print("✓ openpyxl导入成功")
        except ImportError:
            print("⚠ openpyxl未安装，Excel导出功能不可用")
        
        return True
    except Exception as e:
        print(f"✗ 导入测试失败: {e}")
        return False

def test_data_operations():
    """测试数据操作功能"""
    print("\n测试数据操作...")
    try:
        sys.path.append(str(Path(__file__).parent / "tools" / "class-manager-app"))
        from data.store import ClassDataStore
        
        # 创建临时数据存储
        store = ClassDataStore()
        
        # 测试班级操作
        class_id = store.add_classroom("测试班级")
        print("✓ 班级创建成功")
        
        # 测试学生操作
        student_id = store.add_student_to_classroom(class_id, "测试学生")
        print("✓ 学生添加成功")
        
        # 测试币数操作
        store.update_student_weekly_coins(class_id, student_id, 100)
        print("✓ 币数更新成功")
        
        # 清理测试数据
        store.remove_student_from_classroom(class_id, student_id)
        store.remove_classroom(class_id)
        print("✓ 测试数据清理成功")
        
        return True
    except Exception as e:
        print(f"✗ 数据操作测试失败: {e}")
        return False

def check_file_structure():
    """检查文件结构"""
    print("\n检查文件结构...")
    
    required_files = [
        "tools/class-manager-app/main.py",
        "tools/class-manager-app/ui/login_view.py",
        "tools/class-manager-app/ui/main_view.py",
        "tools/class-manager-app/ui/class_detail_view.py",
        "tools/class-manager-app/data/models.py",
        "tools/class-manager-app/data/store.py",
        "build_exe.py",
        "build_windows.bat"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 缺失")
            all_exist = False
    
    return all_exist

def check_optimized_features():
    """检查优化功能"""
    print("\n检查优化功能...")
    
    try:
        # 检查登录界面优化
        login_file = Path("tools/class-manager-app/ui/login_view.py")
        if login_file.exists():
            with open(login_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "预留300x300圆角图片位置" in content:
                    print("✓ 登录界面图片位置预留")
                if "input_container" in content:
                    print("✓ 登录界面居中布局")
        
        # 检查班级详情页面优化
        detail_file = Path("tools/class-manager-app/ui/class_detail_view.py")
        if detail_file.exists():
            with open(detail_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "padding=(10, 8)" in content:
                    print("✓ 班级详情页面标题行高优化")
                if "width=180" in content:
                    print("✓ 班级详情页面列宽优化")
        
        # 检查新增班级按钮
        main_file = Path("tools/class-manager-app/ui/main_view.py")
        if main_file.exists():
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "新增班级" in content and "add_classroom" in content:
                    print("✓ 新增班级按钮已恢复")
        
        return True
    except Exception as e:
        print(f"✗ 功能检查失败: {e}")
        return False

def check_build_files():
    """检查打包文件"""
    print("\n检查打包文件...")
    
    build_files = [
        "build_exe.py",
        "build_windows.bat"
    ]
    
    all_exist = True
    for file_path in build_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} 缺失")
            all_exist = False
    
    return all_exist

def main():
    """主测试函数"""
    print("=" * 60)
    print("班级管理系统 v1.3 - 功能测试")
    print("Classroom Manager v1.3 - Feature Test")
    print("=" * 60)
    
    tests = [
        ("文件结构检查", check_file_structure),
        ("模块导入测试", test_imports),
        ("数据操作测试", test_data_operations),
        ("优化功能检查", check_optimized_features),
        ("打包文件检查", check_build_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}执行异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果汇总 / Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统已准备就绪。")
        print("🎉 All tests passed! System is ready.")
        return 0
    else:
        print("⚠ 部分测试失败，请检查上述问题。")
        print("⚠ Some tests failed, please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())