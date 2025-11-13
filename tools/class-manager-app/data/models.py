"""
数据模型定义
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Student:
    """学生模型"""
    name: str
    weekly_coins: int = 0
    cumulative_coins: int = 0


@dataclass
class Classroom:
    """课堂模型"""
    name: str
    class_id: str
    students: List[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        """添加学生到班级"""
        self.students.append(student)

    def get_student_by_name(self, name: str) -> Student:
        """按名字获取学生"""
        for student in self.students:
            if student.name == name:
                return student
        return None

    def get_all_students(self) -> List[Student]:
        """获取所有学生"""
        return self.students
