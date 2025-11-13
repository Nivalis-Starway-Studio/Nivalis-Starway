"""
数据存储和业务逻辑
Data store and business logic for classroom management
"""

from typing import List, Dict
from .models import Classroom, Student
from .excel_store import ExcelDataStore


class ClassDataStore:
    """课堂数据存储和管理 / Classroom data store and management"""

    def __init__(self):
        """初始化数据存储 / Initialize the data store"""
        self.classrooms: Dict[str, Classroom] = {}
        self.excel_store = ExcelDataStore()
        self._load_data()

    def _load_data(self) -> None:
        """
        加载数据（优先从Excel加载，如果不存在则加载示例数据）
        / Load data (from Excel if exists, otherwise load sample data)
        """
        loaded_classrooms = self.excel_store.load_classrooms()
        
        if loaded_classrooms:
            self.classrooms = loaded_classrooms
        else:
            self._load_sample_data()
            self.save_data()

    def _load_sample_data(self) -> None:
        """加载示例数据 / Load sample data with seven classes"""
        # 一年级 / Grade 1
        class1 = Classroom(name="一年级A班", class_id="1A")
        class1.add_student(Student(name="张三", cumulative_coins=50, week_coins={1: 5, 2: 3}))
        class1.add_student(Student(name="李四", cumulative_coins=45, week_coins={1: 2, 2: 4}))
        class1.add_student(Student(name="王五", cumulative_coins=38, week_coins={1: 3}))
        class1.add_student(Student(name="赵六", cumulative_coins=42, week_coins={}))
        self.classrooms["1A"] = class1

        # 一年级B班 / Grade 1 Class B
        class2 = Classroom(name="一年级B班", class_id="1B")
        class2.add_student(Student(name="周七", cumulative_coins=35, week_coins={1: 2}))
        class2.add_student(Student(name="吴八", cumulative_coins=48, week_coins={1: 4, 2: 3}))
        class2.add_student(Student(name="郑九", cumulative_coins=30, week_coins={2: 1}))
        class2.add_student(Student(name="孙十", cumulative_coins=55, week_coins={}))
        self.classrooms["1B"] = class2

        # 二年级A班 / Grade 2 Class A
        class3 = Classroom(name="二年级A班", class_id="2A")
        class3.add_student(Student(name="李雨", cumulative_coins=60, week_coins={1: 3}))
        class3.add_student(Student(name="王雪", cumulative_coins=45, week_coins={}))
        class3.add_student(Student(name="张风", cumulative_coins=70, week_coins={1: 5, 2: 4}))
        self.classrooms["2A"] = class3

        # 二年级B班 / Grade 2 Class B
        class4 = Classroom(name="二年级B班", class_id="2B")
        class4.add_student(Student(name="陈月", cumulative_coins=50, week_coins={1: 2}))
        class4.add_student(Student(name="刘星", cumulative_coins=65, week_coins={1: 4, 2: 3}))
        class4.add_student(Student(name="黄光", cumulative_coins=40, week_coins={}))
        self.classrooms["2B"] = class4

        # 三年级A班 / Grade 3 Class A
        class5 = Classroom(name="三年级A班", class_id="3A")
        class5.add_student(Student(name="林火", cumulative_coins=55, week_coins={1: 1}))
        class5.add_student(Student(name="何水", cumulative_coins=62, week_coins={1: 3, 2: 2}))
        class5.add_student(Student(name="胡土", cumulative_coins=48, week_coins={}))
        class5.add_student(Student(name="冯金", cumulative_coins=58, week_coins={2: 2}))
        self.classrooms["3A"] = class5

        # 三年级B班 / Grade 3 Class B
        class6 = Classroom(name="三年级B班", class_id="3B")
        class6.add_student(Student(name="杜木", cumulative_coins=72, week_coins={1: 4}))
        class6.add_student(Student(name="卢布", cumulative_coins=40, week_coins={1: 1}))
        class6.add_student(Student(name="荣耀", cumulative_coins=51, week_coins={2: 2}))
        self.classrooms["3B"] = class6

        # 四年级A班 / Grade 4 Class A
        class7 = Classroom(name="四年级A班", class_id="4A")
        class7.add_student(Student(name="蒋云", cumulative_coins=80, week_coins={}))
        class7.add_student(Student(name="乐天", cumulative_coins=95, week_coins={1: 5, 2: 3}))
        class7.add_student(Student(name="许诺", cumulative_coins=68, week_coins={1: 3}))
        class7.add_student(Student(name="包容", cumulative_coins=55, week_coins={2: 1}))
        self.classrooms["4A"] = class7

    def get_all_classrooms(self) -> List[Classroom]:
        """获取所有课堂 / Get all classrooms"""
        return list(self.classrooms.values())

    def get_classroom(self, class_id: str) -> Classroom:
        """按ID获取课堂 / Get a classroom by ID"""
        return self.classrooms.get(class_id)

    def save_data(self) -> bool:
        """
        保存数据到Excel
        / Save data to Excel
        """
        return self.excel_store.save_classrooms(self.classrooms)

    def update_student_week_coins(
        self, class_id: str, student_name: str, week_num: int, new_coins: int
    ) -> bool:
        """
        更新学生指定周的币数，并自动更新累计币
        / Update student's coins for a specific week and auto-update cumulative
        
        Args:
            class_id: 班级ID / Class ID
            student_name: 学生名字 / Student name
            week_num: 周数 / Week number
            new_coins: 新币数 / New coin amount
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return False

        student = classroom.get_student_by_name(student_name)
        if not student:
            return False

        # 获取旧的币数 / Get old coin amount
        old_coins = student.week_coins.get(week_num, 0)
        
        # 更新周币 / Update week coins
        if new_coins > 0:
            student.week_coins[week_num] = new_coins
        else:
            # 如果新币数为0，从字典中删除
            if week_num in student.week_coins:
                del student.week_coins[week_num]
        
        # 自动更新累计币 / Auto-update cumulative coins
        coin_diff = new_coins - old_coins
        student.cumulative_coins += coin_diff
        
        # 保存到Excel / Save to Excel
        self.save_data()
        
        return True

    def get_classroom_stats(self, class_id: str, weeks: List[int] = None) -> Dict:
        """
        获取课堂统计信息 / Get classroom statistics
        
        Args:
            class_id: 班级ID / Class ID
            weeks: 要统计的周数列表 / List of weeks to include in stats
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return None

        student_count = len(classroom.get_all_students())
        total_cumulative = sum(
            s.cumulative_coins for s in classroom.get_all_students()
        )
        
        # 计算各周的总币数 / Calculate total coins for each week
        week_totals = {}
        if weeks:
            for week_num in weeks:
                week_total = sum(
                    s.week_coins.get(week_num, 0) 
                    for s in classroom.get_all_students()
                )
                week_totals[week_num] = week_total

        return {
            "student_count": student_count,
            "total_cumulative": total_cumulative,
            "week_totals": week_totals,
        }
