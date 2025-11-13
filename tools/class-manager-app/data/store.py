"""
数据存储和业务逻辑
Data store and business logic for classroom management
"""

from typing import List, Dict
from .models import Classroom, Student


class ClassDataStore:
    """课堂数据存储和管理 / Classroom data store and management"""

    def __init__(self):
        """初始化数据存储 / Initialize the data store"""
        self.classrooms: Dict[str, Classroom] = {}
        self._load_sample_data()

    def _load_sample_data(self) -> None:
        """加载示例数据 / Load sample data with seven classes"""
        # 一年级 / Grade 1
        class1 = Classroom(name="一年级A班", class_id="1A")
        class1.add_student(Student(name="张三", weekly_coins=0, cumulative_coins=50))
        class1.add_student(Student(name="李四", weekly_coins=5, cumulative_coins=45))
        class1.add_student(Student(name="王五", weekly_coins=3, cumulative_coins=38))
        class1.add_student(Student(name="赵六", weekly_coins=0, cumulative_coins=42))
        self.classrooms["1A"] = class1

        # 一年级B班 / Grade 1 Class B
        class2 = Classroom(name="一年级B班", class_id="1B")
        class2.add_student(Student(name="周七", weekly_coins=2, cumulative_coins=35))
        class2.add_student(Student(name="吴八", weekly_coins=4, cumulative_coins=48))
        class2.add_student(Student(name="郑九", weekly_coins=1, cumulative_coins=30))
        class2.add_student(Student(name="孙十", weekly_coins=0, cumulative_coins=55))
        self.classrooms["1B"] = class2

        # 二年级A班 / Grade 2 Class A
        class3 = Classroom(name="二年级A班", class_id="2A")
        class3.add_student(Student(name="李雨", weekly_coins=3, cumulative_coins=60))
        class3.add_student(Student(name="王雪", weekly_coins=0, cumulative_coins=45))
        class3.add_student(Student(name="张风", weekly_coins=5, cumulative_coins=70))
        self.classrooms["2A"] = class3

        # 二年级B班 / Grade 2 Class B
        class4 = Classroom(name="二年级B班", class_id="2B")
        class4.add_student(Student(name="陈月", weekly_coins=2, cumulative_coins=50))
        class4.add_student(Student(name="刘星", weekly_coins=4, cumulative_coins=65))
        class4.add_student(Student(name="黄光", weekly_coins=0, cumulative_coins=40))
        self.classrooms["2B"] = class4

        # 三年级A班 / Grade 3 Class A
        class5 = Classroom(name="三年级A班", class_id="3A")
        class5.add_student(Student(name="林火", weekly_coins=1, cumulative_coins=55))
        class5.add_student(Student(name="何水", weekly_coins=3, cumulative_coins=62))
        class5.add_student(Student(name="胡土", weekly_coins=0, cumulative_coins=48))
        class5.add_student(Student(name="冯金", weekly_coins=2, cumulative_coins=58))
        self.classrooms["3A"] = class5

        # 三年级B班 / Grade 3 Class B
        class6 = Classroom(name="三年级B班", class_id="3B")
        class6.add_student(Student(name="杜木", weekly_coins=4, cumulative_coins=72))
        class6.add_student(Student(name="卢布", weekly_coins=1, cumulative_coins=40))
        class6.add_student(Student(name="荣耀", weekly_coins=2, cumulative_coins=51))
        self.classrooms["3B"] = class6

        # 四年级A班 / Grade 4 Class A
        class7 = Classroom(name="四年级A班", class_id="4A")
        class7.add_student(Student(name="蒋云", weekly_coins=0, cumulative_coins=80))
        class7.add_student(Student(name="乐天", weekly_coins=5, cumulative_coins=95))
        class7.add_student(Student(name="许诺", weekly_coins=3, cumulative_coins=68))
        class7.add_student(Student(name="包容", weekly_coins=1, cumulative_coins=55))
        self.classrooms["4A"] = class7

    def get_all_classrooms(self) -> List[Classroom]:
        """获取所有课堂 / Get all classrooms"""
        return list(self.classrooms.values())

    def get_classroom(self, class_id: str) -> Classroom:
        """按ID获取课堂 / Get a classroom by ID"""
        return self.classrooms.get(class_id)

    def update_student_weekly_coins(
        self, class_id: str, student_name: str, new_weekly_coins: int
    ) -> bool:
        """
        更新学生周币 / Update student's weekly coins
        不改变累计币 / Does not change cumulative coins
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return False

        student = classroom.get_student_by_name(student_name)
        if not student:
            return False

        # 更新周币 / Update weekly coins
        old_weekly = student.weekly_coins
        student.weekly_coins = max(0, new_weekly_coins)
        return True

    def reset_weekly_coins(self, class_id: str) -> bool:
        """
        重置课堂所有学生的周币，并更新累计币
        / Reset all students' weekly coins and update cumulative coins
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return False

        for student in classroom.get_all_students():
            # 周币加到累计币 / Add weekly to cumulative
            student.cumulative_coins += student.weekly_coins
            # 重置周币为0 / Reset weekly to 0
            student.weekly_coins = 0

        return True

    def get_student_coins(self, class_id: str, student_name: str) -> Dict[str, int]:
        """
        获取学生的币数信息 / Get student's coin information
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return None

        student = classroom.get_student_by_name(student_name)
        if not student:
            return None

        return {
            "weekly_coins": student.weekly_coins,
            "cumulative_coins": student.cumulative_coins,
        }

    def get_classroom_stats(self, class_id: str) -> Dict[str, int]:
        """
        获取课堂统计信息 / Get classroom statistics
        """
        classroom = self.get_classroom(class_id)
        if not classroom:
            return None

        total_weekly = sum(s.weekly_coins for s in classroom.get_all_students())
        total_cumulative = sum(
            s.cumulative_coins for s in classroom.get_all_students()
        )
        student_count = len(classroom.get_all_students())

        return {
            "total_weekly": total_weekly,
            "total_cumulative": total_cumulative,
            "student_count": student_count,
        }
