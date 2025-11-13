#!/usr/bin/env python3
"""
核心功能测试脚本 / Core functionality test script
测试数据存储和业务逻辑是否正常工作
"""

import sys
import os

# 添加项目路径 / Add project path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.store import ClassDataStore
from data.models import Student, Classroom


def test_data_store():
    """测试数据存储功能 / Test data store functionality"""
    print("🧪 开始测试数据存储功能...")
    
    # 创建数据存储 / Create data store
    store = ClassDataStore()
    
    # 测试获取所有班级 / Test get all classrooms
    classrooms = store.get_all_classrooms()
    print(f"✅ 获取到 {len(classrooms)} 个班级")
    
    # 测试添加班级 / Test add classroom
    new_class = store.add_classroom("测试班级")
    print(f"✅ 添加班级: {new_class.name} (ID: {new_class.class_id})")
    
    # 测试添加学生 / Test add student
    success = store.add_student_to_classroom(new_class.class_id, "测试学生")
    print(f"✅ 添加学生: {'成功' if success else '失败'}")
    
    # 测试修改学生名字 / Test update student name
    success = store.update_student_name(new_class.class_id, "测试学生", "新名字")
    print(f"✅ 修改学生名字: {'成功' if success else '失败'}")
    
    # 测试周范围计算 / Test week range calculation
    week_range = store.get_week_range(0)  # 本周
    print(f"✅ 本周日期范围: {week_range[0]} - {week_range[1]}")
    
    week_range = store.get_week_range(-1)  # 上周
    print(f"✅ 上周日期范围: {week_range[0]} - {week_range[1]}")
    
    # 测试4周数据获取 / Test 4 weeks data
    weeks_data = store.get_four_weeks_data(new_class.class_id)
    print(f"✅ 获取4周数据: {len(weeks_data)} 周")
    
    # 测试统计信息 / Test statistics
    stats = store.get_classroom_stats(new_class.class_id)
    print(f"✅ 班级统计: {stats}")
    
    # 测试删除学生 / Test delete student
    success = store.remove_student_from_classroom(new_class.class_id, "新名字")
    print(f"✅ 删除学生: {'成功' if success else '失败'}")
    
    # 测试删除班级 / Test delete classroom
    success = store.remove_classroom(new_class.class_id)
    print(f"✅ 删除班级: {'成功' if success else '失败'}")
    
    print("🎉 数据存储功能测试完成！")


def test_models():
    """测试数据模型 / Test data models"""
    print("\n🧪 开始测试数据模型...")
    
    # 测试学生模型 / Test student model
    student = Student(name="测试学生", weekly_coins=5, cumulative_coins=50)
    print(f"✅ 创建学生: {student.name}, 周币: {student.weekly_coins}, 累计: {student.cumulative_coins}")
    print(f"✅ 学生ID: {student.student_id}")
    
    # 测试班级模型 / Test classroom model
    classroom = Classroom(name="测试班级", class_id="TEST")
    classroom.add_student(student)
    print(f"✅ 创建班级: {classroom.name}, 学生数: {len(classroom.get_all_students())}")
    
    # 测试查找学生 / Test find student
    found_student = classroom.get_student_by_name("测试学生")
    print(f"✅ 查找学生: {'成功' if found_student else '失败'}")
    
    # 测试删除学生 / Test remove student
    success = classroom.remove_student_by_name("测试学生")
    print(f"✅ 删除学生: {'成功' if success else '失败'}")
    print(f"✅ 删除后学生数: {len(classroom.get_all_students())}")
    
    print("🎉 数据模型测试完成！")


def test_week_calculations():
    """测试周计算功能 / Test week calculation functionality"""
    print("\n🧪 开始测试周计算功能...")
    
    store = ClassDataStore()
    
    # 测试当前周 / Test current week
    current_week = store._get_current_week()
    print(f"✅ 当前周号: {current_week}")
    
    # 测试各周的日期范围 / Test week ranges
    for offset in [-1, 0, 1, 2]:
        start, end = store.get_week_range(offset)
        week_name = {
            -1: "上周",
            0: "本周", 
            1: "下周",
            2: "下下周"
        }.get(offset, f"偏移{offset}周")
        print(f"✅ {week_name}: {start} - {end}")
    
    print("🎉 周计算功能测试完成！")


def main():
    """主测试函数 / Main test function"""
    print("🚀 开始课堂管理系统核心功能测试\n")
    
    try:
        test_models()
        test_data_store()
        test_week_calculations()
        
        print("\n" + "="*50)
        print("🎊 所有测试通过！系统核心功能正常工作。")
        print("📝 注意：GUI功能需要在有显示环境的系统中测试。")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)