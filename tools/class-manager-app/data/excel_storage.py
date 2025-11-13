"""
Excel数据持久化存储
Excel data persistence storage using CSV format
"""

import csv
import os
from typing import Dict, List
from .models import Classroom, Student


class ExcelStorage:
    """Excel数据存储管理器 / Excel data storage manager"""

    def __init__(self, data_dir: str = None):
        """
        初始化Excel存储
        / Initialize Excel storage

        Args:
            data_dir: 数据目录路径 / Data directory path
        """
        if data_dir is None:
            # 默认使用程序同级目录下的data文件夹
            self.data_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "storage_data"
            )
        else:
            self.data_dir = data_dir

        # 创建数据目录
        os.makedirs(self.data_dir, exist_ok=True)

        self.classrooms_file = os.path.join(self.data_dir, "classrooms.csv")
        self.students_file = os.path.join(self.data_dir, "students.csv")
        self.weekly_history_file = os.path.join(self.data_dir, "weekly_history.csv")

    def save_classrooms(self, classrooms: Dict[str, Classroom]) -> None:
        """
        保存所有班级数据到CSV
        / Save all classroom data to CSV
        """
        # 保存班级信息
        with open(self.classrooms_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["class_id", "name"])
            for classroom in classrooms.values():
                writer.writerow([classroom.class_id, classroom.name])

        # 保存学生信息
        with open(self.students_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "class_id",
                    "student_id",
                    "name",
                    "weekly_coins",
                    "cumulative_coins",
                ]
            )
            for classroom in classrooms.values():
                for student in classroom.students:
                    writer.writerow(
                        [
                            classroom.class_id,
                            student.student_id,
                            student.name,
                            student.weekly_coins,
                            student.cumulative_coins,
                        ]
                    )

        # 保存周历史数据
        with open(self.weekly_history_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["class_id", "student_id", "week_number", "coins"])
            for classroom in classrooms.values():
                for student in classroom.students:
                    for week_number, coins in student.weekly_history.items():
                        writer.writerow(
                            [classroom.class_id, student.student_id, week_number, coins]
                        )

    def load_classrooms(self) -> Dict[str, Classroom]:
        """
        从CSV加载所有班级数据
        / Load all classroom data from CSV
        """
        classrooms = {}

        # 检查文件是否存在
        if not os.path.exists(self.classrooms_file):
            return classrooms

        # 加载班级信息
        with open(self.classrooms_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                class_id = row["class_id"]
                name = row["name"]
                classrooms[class_id] = Classroom(name=name, class_id=class_id)

        # 加载学生信息
        if os.path.exists(self.students_file):
            with open(self.students_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    class_id = row["class_id"]
                    if class_id in classrooms:
                        student = Student(
                            name=row["name"],
                            student_id=row["student_id"],
                            weekly_coins=int(row["weekly_coins"]),
                            cumulative_coins=int(row["cumulative_coins"]),
                        )
                        classrooms[class_id].add_student(student)

        # 加载周历史数据
        if os.path.exists(self.weekly_history_file):
            with open(self.weekly_history_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    class_id = row["class_id"]
                    student_id = row["student_id"]
                    week_number = int(row["week_number"])
                    coins = int(row["coins"])

                    if class_id in classrooms:
                        student = classrooms[class_id].get_student_by_id(student_id)
                        if student:
                            student.weekly_history[week_number] = coins

        return classrooms

    def export_classroom_to_excel(self, classroom: Classroom, filepath: str) -> None:
        """
        导出单个班级数据到CSV
        / Export single classroom data to CSV

        Args:
            classroom: 班级对象
            filepath: 导出文件路径
        """
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # 写入表头
            writer.writerow(
                [
                    "学生ID",
                    "学生姓名",
                    "本周小码币",
                    "累计小码币",
                    "总计",
                ]
            )

            # 写入学生数据
            for student in classroom.students:
                total = student.cumulative_coins + student.weekly_coins
                writer.writerow(
                    [
                        student.student_id,
                        student.name,
                        student.weekly_coins,
                        student.cumulative_coins,
                        total,
                    ]
                )
