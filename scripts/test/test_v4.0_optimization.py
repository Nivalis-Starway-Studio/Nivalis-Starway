#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v4.0 优化验证脚本 / v4.0 Optimization Verification Script
验证图表自适应和文件结构整理是否正确实现
"""

import os
import sys
import re

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} [文件不存在]")
        return False

def check_directory_exists(dirpath, description):
    """检查目录是否存在"""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ {description}: {dirpath} [目录不存在]")
        return False

def check_code_pattern(filepath, pattern, description):
    """检查代码中是否包含指定模式"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(pattern, content, re.MULTILINE):
                print(f"✓ {description}")
                return True
            else:
                print(f"✗ {description} [未找到模式]")
                return False
    except Exception as e:
        print(f"✗ {description} [读取文件失败: {e}]")
        return False

def main():
    """主测试函数"""
    print("=" * 80)
    print("v4.0 优化验证测试 / v4.0 Optimization Verification Test")
    print("=" * 80)
    
    results = []
    
    # 测试1: 项目文件结构整理
    print("\n【测试1】项目文件结构整理")
    print("-" * 80)
    
    # 检查docs目录结构
    results.append(check_directory_exists("docs", "docs目录存在"))
    results.append(check_directory_exists("docs/archive", "docs/archive目录存在"))
    results.append(check_file_exists("docs/README.md", "docs/README.md存在"))
    results.append(check_file_exists("docs/CHANGELOG.md", "docs/CHANGELOG.md存在"))
    results.append(check_file_exists("docs/BUILD_README.md", "docs/BUILD_README.md存在"))
    results.append(check_file_exists("docs/PROJECT_STRUCTURE.md", "docs/PROJECT_STRUCTURE.md存在"))
    results.append(check_file_exists("docs/OPTIMIZATION_v4.0.md", "docs/OPTIMIZATION_v4.0.md存在"))
    
    # 检查scripts目录结构
    results.append(check_directory_exists("scripts", "scripts目录存在"))
    results.append(check_directory_exists("scripts/build", "scripts/build目录存在"))
    results.append(check_directory_exists("scripts/run", "scripts/run目录存在"))
    results.append(check_directory_exists("scripts/test", "scripts/test目录存在"))
    
    # 检查打包脚本
    results.append(check_file_exists("scripts/build/build_exe.py", "打包脚本build_exe.py存在"))
    results.append(check_file_exists("scripts/build/build_exe.bat", "打包脚本build_exe.bat存在"))
    results.append(check_file_exists("scripts/build/README.md", "打包脚本README.md存在"))
    
    # 检查运行脚本
    results.append(check_file_exists("scripts/run/run_app.bat", "运行脚本run_app.bat存在"))
    results.append(check_file_exists("scripts/run/run_app.sh", "运行脚本run_app.sh存在"))
    results.append(check_file_exists("scripts/run/README.md", "运行脚本README.md存在"))
    
    # 检查根目录文档
    results.append(check_file_exists("README.md", "根目录README.md存在"))
    results.append(check_file_exists("CHANGELOG.md", "根目录CHANGELOG.md存在"))
    results.append(check_file_exists("QUICKSTART.md", "快速开始指南存在"))
    
    # 检查旧文件是否被移除
    old_files = [
        "CHANGES.md",
        "CHANGES_SUMMARY.md", 
        "CHART_OPTIMIZATION.md",
        "FINAL_VERIFICATION.md",
        "OPTIMIZATION_SUMMARY.md",
        "build_exe.py",
        "build_exe.bat",
        "run_app.bat",
        "run_app.sh",
        "test_chart_optimization.py"
    ]
    
    all_moved = True
    for old_file in old_files:
        if os.path.exists(old_file):
            print(f"✗ 旧文件未移除: {old_file}")
            all_moved = False
    
    if all_moved:
        print(f"✓ 所有旧文件已正确移除或归档")
        results.append(True)
    else:
        results.append(False)
    
    # 测试2: 图表自适应代码检查
    print("\n【测试2】图表自适应代码检查")
    print("-" * 80)
    
    class_detail_view_path = "tools/class-manager-app/ui/class_detail_view.py"
    
    # 检查窗口自适应代码
    results.append(check_code_pattern(
        class_detail_view_path,
        r"screen_width\s*=\s*chart_window\.winfo_screenwidth\(\)",
        "窗口自适应：获取屏幕宽度"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"window_width\s*=\s*int\(screen_width\s*\*\s*0\.9\)",
        "窗口自适应：窗口占屏幕90%"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"x_offset\s*=.*window_width.*//\s*2",
        "窗口自适应：计算居中位置"
    ))
    
    # 检查图表尺寸自适应代码
    results.append(check_code_pattern(
        class_detail_view_path,
        r"available_width_inches\s*=\s*\(window_width\s*-\s*80\)\s*/\s*dpi",
        "图表自适应：计算可用宽度（英寸）"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"line_area_height\s*=\s*window_height\s*\*\s*0\.6",
        "图表自适应：折线图区域占60%"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"line_height_per_row\s*=\s*max\(.*line_area_height.*dpi.*line_chart_rows",
        "图表自适应：动态计算每行高度"
    ))
    
    # 检查柱状图优化代码
    results.append(check_code_pattern(
        class_detail_view_path,
        r"bar_chart_height\s*=\s*max\(.*window_height\s*\*\s*0\.25.*dpi",
        "柱状图优化：高度占25%"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"ax_bar\.tick_params\(axis='x',\s*rotation=0",
        "柱状图优化：x轴标签不旋转"
    ))
    
    # 检查区域划分
    results.append(check_code_pattern(
        class_detail_view_path,
        r"line_frame\.pack\(fill=tk\.BOTH,\s*expand=True",
        "区域划分：折线图区域expand=True"
    ))
    
    results.append(check_code_pattern(
        class_detail_view_path,
        r"bar_frame\.pack\(fill=tk\.X.*\)\s*#.*不使用expand",
        "区域划分：柱状图区域不使用expand"
    ))
    
    # 测试3: 代码语法检查
    print("\n【测试3】Python代码语法检查")
    print("-" * 80)
    
    try:
        import py_compile
        py_compile.compile(class_detail_view_path, doraise=True)
        print(f"✓ {class_detail_view_path} 语法检查通过")
        results.append(True)
    except py_compile.PyCompileError as e:
        print(f"✗ {class_detail_view_path} 语法错误: {e}")
        results.append(False)
    
    # 测试4: 文档完整性检查
    print("\n【测试4】文档完整性检查")
    print("-" * 80)
    
    # 检查README.md包含v4.0更新说明
    results.append(check_code_pattern(
        "README.md",
        r"v4\.0.*优化|自适应屏幕分辨率",
        "README.md包含v4.0更新说明"
    ))
    
    # 检查CHANGELOG.md包含v4.0版本
    results.append(check_code_pattern(
        "CHANGELOG.md",
        r"\[v4\.0\].*2024",
        "CHANGELOG.md包含v4.0版本记录"
    ))
    
    # 检查.gitignore是否更新
    results.append(check_code_pattern(
        ".gitignore",
        r"# Build output.*构建输出|# IDE.*开发工具",
        ".gitignore包含中文注释和优化配置"
    ))
    
    # 统计结果
    print("\n" + "=" * 80)
    print("测试结果统计 / Test Results Summary")
    print("=" * 80)
    
    total = len(results)
    passed = sum(results)
    failed = total - passed
    
    print(f"总测试项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 恭喜！所有测试通过！v4.0优化已正确实现。")
        return 0
    else:
        print(f"\n⚠️  警告：有 {failed} 项测试失败，请检查上述输出。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
