"""
演示脚本 / Demo script for classroom manager
"""

from data.store import ClassDataStore
from utils.week_utils import get_current_week, format_week_label


def demo_basic_operations():
    """演示基本操作 / Demo basic operations"""
    print("=" * 60)
    print("课堂管理系统演示 / Classroom Manager Demo")
    print("=" * 60)
    
    # 创建数据存储
    store = ClassDataStore()
    
    # 显示当前周数
    current_week = get_current_week()
    print(f"\n📅 当前周数: 第{current_week}周")
    print(f"   (基准日期: 2025年11月13日为第1周)")
    
    # 显示所有班级
    print(f"\n📚 班级列表:")
    for classroom in store.get_all_classrooms():
        student_count = len(classroom.get_all_students())
        print(f"   - {classroom.name} ({classroom.class_id}): {student_count}名学生")
    
    # 选择一个班级详细展示
    class_id = "1A"
    classroom = store.get_classroom(class_id)
    print(f"\n👥 {classroom.name} 学生详情:")
    print("-" * 60)
    print(f"{'学生名字':<10} {'第1周':<8} {'第2周':<8} {'第3周':<8} {'累计币':<8}")
    print("-" * 60)
    
    for student in classroom.get_all_students():
        week1 = student.week_coins.get(1, 0)
        week2 = student.week_coins.get(2, 0)
        week3 = student.week_coins.get(3, 0)
        cumulative = student.cumulative_coins
        print(f"{student.name:<10} {week1:<8} {week2:<8} {week3:<8} {cumulative:<8}")
    
    # 显示统计信息
    stats = store.get_classroom_stats(class_id, weeks=[1, 2, 3, 4])
    print("-" * 60)
    print(f"统计: 学生数={stats['student_count']}, ", end="")
    print(f"第1周总币={stats['week_totals'][1]}, ", end="")
    print(f"第2周总币={stats['week_totals'][2]}, ", end="")
    print(f"第3周总币={stats['week_totals'][3]}, ", end="")
    print(f"累计总币={stats['total_cumulative']}")
    
    # 演示修改周币
    print(f"\n✏️  演示：修改张三第4周的币数")
    student_name = "张三"
    week_num = 4
    new_coins = 8
    
    student = classroom.get_student_by_name(student_name)
    old_coins = student.week_coins.get(week_num, 0)
    old_cumulative = student.cumulative_coins
    
    print(f"   修改前: 第{week_num}周={old_coins}, 累计币={old_cumulative}")
    
    # 执行更新
    store.update_student_week_coins(class_id, student_name, week_num, new_coins)
    
    # 重新获取学生数据
    student = classroom.get_student_by_name(student_name)
    new_cumulative = student.cumulative_coins
    
    print(f"   修改后: 第{week_num}周={new_coins}, 累计币={new_cumulative}")
    print(f"   ✅ 累计币自动增加了 {new_cumulative - old_cumulative} 币")
    print(f"   ✅ 数据已自动保存到Excel文件")
    
    # 验证Excel文件
    print(f"\n💾 Excel文件信息:")
    import os
    excel_path = store.excel_store.file_path
    if os.path.exists(excel_path):
        size_kb = os.path.getsize(excel_path) / 1024
        print(f"   文件路径: {excel_path}")
        print(f"   文件大小: {size_kb:.2f} KB")
        print(f"   ✅ 数据持久化成功")
    else:
        print(f"   ❌ Excel文件未找到")
    
    print("\n" + "=" * 60)
    print("演示完成 / Demo completed")
    print("=" * 60)
    print("\n💡 提示:")
    print("   1. 运行 'python3 main.py' 启动GUI应用")
    print("   2. 登录账号: xigua / 123456")
    print("   3. 双击表格中的周币单元格可直接编辑")
    print("   4. 修改后累计币会自动更新")
    print("=" * 60)


if __name__ == "__main__":
    demo_basic_operations()
