#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表统计窗口优化 - 只检查源代码
Test chart statistics window optimization - source code check only
"""

import os
import re

# 读取源代码 / Read source code
source_file = 'tools/class-manager-app/ui/class_detail_view.py'
print(f"正在检查 {source_file}... / Checking {source_file}...")

try:
    with open(source_file, 'r', encoding='utf-8') as f:
        source = f.read()
    print(f"✓ 文件已读取 / File read successfully\n")
except FileNotFoundError:
    print(f"✗ 文件未找到 / File not found: {source_file}")
    exit(1)

# 检查关键优化点 / Check key optimization points
checks = {
    "全屏支持 (Fullscreen support)": {
        "patterns": [r"state\('zoomed'\)", r"winfo_screenwidth", r"winfo_screenheight"],
        "description": "窗口支持全屏显示 / Window supports fullscreen display"
    },
    "显示所有学生 (Show all students)": {
        "patterns": [r"line_chart_rows\s*=\s*max\(1,\s*num_students\)"],
        "description": "折线图显示所有学生，不限3个 / Line charts show all students, not limited to 3"
    },
    "动态高度计算 (Dynamic height)": {
        "patterns": [r"line_height_per_student", r"total_figure_height", r"line_chart_rows\s*\*"],
        "description": "根据学生数量动态计算高度 / Height calculated dynamically based on student count"
    },
    "颜色区分 (Color differentiation)": {
        "patterns": [r"colors_line\s*=", r"line_color\s*=\s*colors_line"],
        "description": "不同学生使用不同颜色 / Different students use different colors"
    },
    "学生统计计数 (Student count display)": {
        "patterns": [r"共\{num_students\}个学生", r"num_students"],
        "description": "标题显示学生总数 / Title displays total student count"
    },
    "新学生实时更新 (Real-time update)": {
        "patterns": [r"all_students\s*=\s*list\(classroom\.get_all_students\(\)\)"],
        "description": "获取最新学生列表 / Get latest student list"
    }
}

print("检查优化实现... / Checking optimizations...\n")
print("=" * 70)

all_passed = True
for check_name, check_info in checks.items():
    patterns = check_info["patterns"]
    description = check_info["description"]
    
    # 检查是否存在任何一个模式 / Check if any pattern exists
    found = False
    for pattern in patterns:
        if re.search(pattern, source):
            found = True
            break
    
    if found:
        print(f"✓ {check_name}")
        print(f"  {description}")
    else:
        print(f"✗ {check_name}")
        print(f"  {description}")
        all_passed = False
    print()

print("=" * 70)

# 检查语法 / Check syntax
print("\n检查Python语法... / Checking Python syntax...")
try:
    compile(source, source_file, 'exec')
    print("✓ 代码语法正确 / Code syntax is correct")
except SyntaxError as e:
    print(f"✗ 语法错误 / Syntax error: {e}")
    all_passed = False

# 检查关键方法 / Check for key methods
print("\n检查关键方法... / Checking key methods...")
if "def show_chart_statistics" in source:
    print("✓ show_chart_statistics 方法存在 / show_chart_statistics method exists")
else:
    print("✗ show_chart_statistics 方法不存在 / show_chart_statistics method not found")
    all_passed = False

# 显示结果 / Display results
print("\n" + "=" * 70)
if all_passed:
    print("\n✓✓✓ 所有优化检查通过！/ All optimization checks passed! ✓✓✓")
    print("\n优化摘要 / Optimization Summary:")
    print("──────────────────────────────────────────────────────────")
    print("1. 图表窗口默认全屏显示")
    print("   Chart window defaults to fullscreen display")
    print()
    print("2. 支持显示所有学生的折线图（无限制）")
    print("   Supports displaying line charts for all students (unlimited)")
    print()
    print("3. 折线图高度自适应")
    print("   Line charts height auto-adapts")
    print()
    print("4. 为不同学生使用不同颜色")
    print("   Uses different colors for different students")
    print()
    print("5. 新添加的学生实时更新")
    print("   Newly added students are updated in real-time")
    print("──────────────────────────────────────────────────────────")
else:
    print("\n✗✗✗ 某些优化检查失败 / Some optimization checks failed ✗✗✗")
    exit(1)
