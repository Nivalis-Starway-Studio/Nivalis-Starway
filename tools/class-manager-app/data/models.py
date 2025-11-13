"""
数据模型定义
Data models for the classroom manager application
"""

from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime, timedelta


@dataclass
class Student:
    """学生模型 / Student model"""
    name: str
    weekly_coins: int = 0
    cumulative_coins: int = 0
    weekly_history: Dict[int, int] = field(default_factory=dict)  # week_number -> coins
    student_id: str = field(default="")
    
    def __post_init__(self):
        """初始化后处理 / Post-init processing"""
        if not self.student_id:
            self.student_id = f"stu_{datetime.now().timestamp()}"


@dataclass
class Classroom:
    """课堂模型 / Classroom model"""
    name: str
    class_id: str
    students: List[Student] = field(default_factory=list)

    def add_student(self, student: Student) -> None:
        """添加学生 / Add a student to the classroom"""
        if not student.student_id:
            student.student_id = f"stu_{len(self.students)}_{datetime.now().timestamp()}"
        self.students.append(student)

    def remove_student(self, student_id: str) -> bool:
        """删除学生 / Remove a student by ID"""
        for i, student in enumerate(self.students):
            if student.student_id == student_id:
                self.students.pop(i)
                return True
        return False

    def remove_student_by_name(self, name: str) -> bool:
        """按名字删除学生 / Remove a student by name"""
        for i, student in enumerate(self.students):
            if student.name == name:
                self.students.pop(i)
                return True
        return False

    def get_student_by_name(self, name: str) -> Student:
        """按名字获取学生 / Get a student by name"""
        for student in self.students:
            if student.name == name:
                return student
        return None

    def get_student_by_id(self, student_id: str) -> Student:
        """按ID获取学生 / Get a student by ID"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def get_all_students(self) -> List[Student]:
        """获取所有学生 / Get all students"""
        return self.students
