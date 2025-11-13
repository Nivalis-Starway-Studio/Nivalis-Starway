"""
测试新功能 / Test new features
"""

import os
from data.store import ClassDataStore
from utils.week_utils import get_current_week, get_week_date_range, format_week_label


def test_week_utils():
    """测试周数工具 / Test week utilities"""
    print("=== 测试周数工具 / Testing Week Utils ===")
    current_week = get_current_week()
    print(f"当前周数 / Current week: {current_week}")
    
    for week in range(1, 5):
        label = format_week_label(week)
        print(f"第{week}周标签 / Week {week} label: {label}")
    
    print()


def test_data_persistence():
    """测试数据持久化 / Test data persistence"""
    print("=== 测试数据持久化 / Testing Data Persistence ===")
    
    # 创建数据存储实例
    store = ClassDataStore()
    
    # 检查班级数量
    classrooms = store.get_all_classrooms()
    print(f"班级数量 / Number of classrooms: {len(classrooms)}")
    
    # 显示第一个班级的学生数据
    class1 = store.get_classroom("1A")
    if class1:
        print(f"\n班级: {class1.name}")
        for student in class1.get_all_students():
            print(f"  学生: {student.name}")
            print(f"    累计币 / Cumulative coins: {student.cumulative_coins}")
            print(f"    周币记录 / Week coins: {student.week_coins}")
    
    # 测试更新周币
    print("\n测试更新周币 / Testing update week coins...")
    success = store.update_student_week_coins("1A", "张三", 3, 7)
    if success:
        print("✓ 周币更新成功 / Week coins updated successfully")
        student = class1.get_student_by_name("张三")
        print(f"  第3周币数 / Week 3 coins: {student.week_coins.get(3, 0)}")
        print(f"  累计币 / Cumulative coins: {student.cumulative_coins}")
    
    # 检查Excel文件是否创建
    excel_path = store.excel_store.file_path
    print(f"\nExcel文件路径 / Excel file path: {excel_path}")
    if os.path.exists(excel_path):
        print(f"✓ Excel文件已创建 / Excel file created")
        print(f"  文件大小 / File size: {os.path.getsize(excel_path)} bytes")
    else:
        print("✗ Excel文件不存在 / Excel file not found")
    
    # 测试统计信息
    print("\n测试统计信息 / Testing statistics...")
    stats = store.get_classroom_stats("1A", weeks=[1, 2, 3, 4])
    if stats:
        print(f"  学生数 / Student count: {stats['student_count']}")
        print(f"  累计总币 / Total cumulative: {stats['total_cumulative']}")
        print(f"  各周总币 / Week totals: {stats['week_totals']}")
    
    print()


def test_reload_from_excel():
    """测试从Excel重新加载 / Test reload from Excel"""
    print("=== 测试从Excel重新加载 / Testing Reload from Excel ===")
    
    # 创建新的数据存储实例（会从Excel加载）
    store2 = ClassDataStore()
    
    class1 = store2.get_classroom("1A")
    if class1:
        student = class1.get_student_by_name("张三")
        print(f"学生: {student.name}")
        print(f"  第3周币数 / Week 3 coins: {student.week_coins.get(3, 0)}")
        print(f"  累计币 / Cumulative coins: {student.cumulative_coins}")
        
        if student.week_coins.get(3, 0) == 7:
            print("✓ 数据持久化成功 / Data persistence successful")
        else:
            print("✗ 数据未正确加载 / Data not loaded correctly")
    
    print()


if __name__ == "__main__":
    test_week_utils()
    test_data_persistence()
    test_reload_from_excel()
    print("=== 所有测试完成 / All tests completed ===")
