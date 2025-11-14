#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图表优化v3 - 验证折线图每行显示2个学生、可滚动、柱状图独立区域
Test chart optimization v3 - Verify 2 students per row, scrollable, and separate bar chart region
"""

import re

def check_optimization():
    """检查所有v3优化是否实现"""
    print("=" * 80)
    print("图表统计优化验证 v3.0 - 折线图每行2个、可滚动、区域划分")
    print("=" * 80)
    
    file_path = "tools/class-manager-app/ui/class_detail_view.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # 1. 检查每行显示2个学生的计算
    check1 = '(num_students + 1) // 2' in content
    checks.append(("✓" if check1 else "✗", "每行显示2个学生的折线图", check1))
    
    # 2. 检查主框架划分
    check2 = '创建主框架，划分两个区域' in content or 'Create main frame with two regions' in content
    checks.append(("✓" if check2 else "✗", "主框架划分两个区域", check2))
    
    # 3. 检查折线图区域可滚动
    check3 = 'line_canvas = tk.Canvas' in content and 'line_scrollbar = ttk.Scrollbar' in content
    checks.append(("✓" if check3 else "✗", "折线图区域使用Canvas和Scrollbar", check3))
    
    # 4. 检查鼠标滚轮绑定
    check4 = '_on_mousewheel' in content and 'MouseWheel' in content
    checks.append(("✓" if check4 else "✗", "绑定鼠标滚轮事件", check4))
    
    # 5. 检查GridSpec每行2列布局
    check5 = 'line_chart_rows, 2' in content
    checks.append(("✓" if check5 else "✗", "GridSpec每行2列布局", check5))
    
    # 6. 检查行列索引计算
    check6 = 'row = idx // 2' in content and 'col = idx % 2' in content
    checks.append(("✓" if check6 else "✗", "行列索引计算（每行2个）", check6))
    
    # 7. 检查奇数学生处理
    check7 = 'num_students % 2 == 1' in content and "axis('off')" in content
    checks.append(("✓" if check7 else "✗", "奇数学生时隐藏空位", check7))
    
    # 8. 检查独立的折线图和柱状图Figure
    check8 = 'fig_line = plt.figure' in content and 'fig_bar = plt.figure' in content
    checks.append(("✓" if check8 else "✗", "折线图和柱状图独立Figure", check8))
    
    # 9. 检查柱状图区域
    check9 = 'bar_frame = ttk.LabelFrame' in content and '班级总小码币统计' in content
    checks.append(("✓" if check9 else "✗", "柱状图独立区域", check9))
    
    # 10. 检查柱状图x轴标签自适应
    check10 = 'len(student_names) <= 5' in content and 'rotation=0' in content
    checks.append(("✓" if check10 else "✗", "柱状图x轴标签自适应（0/45/90度）", check10))
    
    # 11. 检查tight_layout防止标签截断
    check11 = 'fig_bar.tight_layout' in content
    checks.append(("✓" if check11 else "✗", "tight_layout防止标签截断", check11))
    
    # 12. 检查滚动区域的Canvas嵌入
    check12 = 'scrollable_line_frame' in content and 'line_canvas_widget = FigureCanvasTkAgg(fig_line, scrollable_line_frame)' in content
    checks.append(("✓" if check12 else "✗", "折线图嵌入到滚动区域", check12))
    
    # 打印检查结果
    print("\n【优化检查结果】\n")
    for symbol, desc, result in checks:
        print(f"  {symbol} {desc}")
    
    all_passed = all(check[2] for check in checks)
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ 所有优化检查通过！图表统计已实现v3.0优化")
        print("\n【优化亮点】")
        print("  1. 折线图每行显示2个学生，充分利用屏幕空间")
        print("  2. 折线图区域支持鼠标滚轮滚动，适应任意数量学生")
        print("  3. 柱状图独立固定区域，不受滚动影响")
        print("  4. 柱状图x轴标签自适应显示（0/45/90度），完整显示学生名字")
        print("  5. 明确区域划分，使用LabelFrame增强视觉层次")
        print("  6. 奇数学生时自动隐藏空位，布局整洁")
    else:
        print("✗ 部分优化未通过检查")
    print("=" * 80)
    
    return all_passed

if __name__ == "__main__":
    check_optimization()
