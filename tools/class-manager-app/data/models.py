"""
数据模型定义
Data models for the classroom manager application
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Student:
    """学生模型 / Student model"""
    name: str
    cumulative_coins: int = 0
    week_coins: Dict[int, int] = field(default_factory=dict)  # 周数 -> 币数


@dataclass
class Classroom:
    """课堂模型 / Classroom model"""
    name: str
    class_id: str
    students: List[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        """添加学生 / Add a student to the classroom"""
        self.students.append(student)

    def get_student_by_name(self, name: str) -> Student:
        """按名字获取学生 / Get a student by name"""
        for student in self.students:
            if student.name == name:
                return student
        return None

    def get_all_students(self) -> List[Student]:
        """获取所有学生 / Get all students"""
        return self.students
