"""
测试响应式布局 - 模拟不同屏幕尺寸
Test Responsive Layout - Simulate Different Screen Sizes
"""

def test_screen_adaptive():
    """测试屏幕自适应逻辑"""
    
    # 模拟不同的屏幕高度
    test_cases = [
        (1920, 720, "150%缩放的1920x1080 (你的笔记本)"),
        (1920, 800, "小屏幕或高DPI场景"),
        (1920, 1080, "标准1080p"),
        (2560, 1440, "2K显示器"),
        (3840, 2160, "4K显示器"),
    ]
    
    print("=" * 60)
    print("屏幕自适应测试结果")
    print("=" * 60)
    
    for width, height, desc in test_cases:
        print(f"\n场景: {desc}")
        print(f"分辨率: {width}x{height}")
        
        # Treeview高度计算
        if height <= 800:
            tree_height = 8
        elif height <= 1080:
            tree_height = 12
        else:
            tree_height = 15
        
        tree_pixels = tree_height * 35  # rowheight = 35
        print(f"  - Treeview: {tree_height}行 x 35px = {tree_pixels}px")
        
        # 图表窗口大小
        chart_width = int(width * 0.85)
        chart_height = int(height * 0.85)
        print(f"  - 图表窗口: {chart_width}x{chart_height}")
        
        # 折线图高度
        if height <= 800:
            line_height_per_row = 3.0
        elif height <= 1080:
            line_height_per_row = 3.5
        else:
            line_height_per_row = 4.0
        
        # 柱状图高度
        if height <= 800:
            bar_chart_height = 3.0
        elif height <= 1080:
            bar_chart_height = 3.5
        else:
            bar_chart_height = 4.0
        
        print(f"  - 折线图每行: {line_height_per_row}英寸 = {int(line_height_per_row * 100)}px")
        print(f"  - 柱状图高度: {bar_chart_height}英寸 = {int(bar_chart_height * 100)}px")
        
        # 可用性评估
        remaining_height = height - tree_pixels - 200  # 减去Treeview和其他控件
        if remaining_height > 150:
            status = "✅ 良好"
        else:
            status = "⚠️  紧凑"
        print(f"  - 布局状态: {status} (剩余约{remaining_height}px给控制区域)")
    
    print("\n" + "=" * 60)
    print("所有场景测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_screen_adaptive()
