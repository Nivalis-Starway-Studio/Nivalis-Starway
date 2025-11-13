"""
Excel 数据持久化模块
Excel data persistence module for classroom data
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

from .models import Classroom, Student


class ExcelStorage:
    """Excel 数据存储管理 / Excel data storage manager"""

    def __init__(self, filepath: str = None):
        """
        初始化 Excel 存储
        / Initialize Excel storage
        
        Args:
            filepath: Excel 文件路径 / Path to Excel file
        """
        if not OPENPYXL_AVAILABLE:
            print("警告：openpyxl 未安装。请运行 pip install openpyxl 来启用 Excel 功能")
            print("Warning: openpyxl is not installed. Run pip install openpyxl to enable Excel features")
            self.available = False
            return
        
        self.available = True
        if filepath is None:
            # 默认保存在项目目录的 data 文件夹 / Default save in project data folder
            self.filepath = Path(__file__).parent.parent / "classroom_data.xlsx"
        else:
            self.filepath = Path(filepath)
        
        # 确保文件目录存在 / Ensure directory exists
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def save_classrooms(self, classrooms: Dict[str, Classroom]) -> bool:
        """
        保存班级数据到 Excel
        / Save classroom data to Excel
        
        Args:
            classrooms: 班级字典 / Dictionary of classrooms
            
        Returns:
            是否保存成功 / Whether save was successful
        """
        if not self.available:
            return False
        
        try:
            wb = Workbook()
            wb.remove(wb.active)  # 移除默认工作表 / Remove default sheet
            
            # 创建班级总览工作表 / Create overview sheet
            overview_sheet = wb.create_sheet("班级总览", 0)
            self._setup_overview_sheet(overview_sheet, classrooms)
            
            # 为每个班级创建工作表 / Create sheet for each classroom
            for idx, (class_id, classroom) in enumerate(classrooms.items(), 1):
                sheet = wb.create_sheet(classroom.name, idx)
                self._setup_classroom_sheet(sheet, classroom)
            
            wb.save(self.filepath)
            print(f"数据已保存到: {self.filepath}")
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False

    def load_classrooms(self) -> Dict[str, Classroom]:
        """
        从 Excel 加载班级数据
        / Load classroom data from Excel
        
        Returns:
            班级字典 / Dictionary of classrooms
        """
        if not self.available or not self.filepath.exists():
            return {}
        
        try:
            wb = load_workbook(self.filepath)
            classrooms = {}
            
            # 跳过班级总览工作表 / Skip overview sheet
            for sheet_name in wb.sheetnames:
                if sheet_name == "班级总览":
                    continue
                
                sheet = wb[sheet_name]
                classroom = self._parse_classroom_sheet(sheet)
                if classroom:
                    classrooms[classroom.class_id] = classroom
            
            wb.close()
            print(f"数据已从 {self.filepath} 加载")
            return classrooms
        except Exception as e:
            print(f"加载失败: {e}")
            return {}

    def _setup_overview_sheet(self, sheet, classrooms: Dict[str, Classroom]) -> None:
        """
        设置班级总览工作表
        / Setup overview sheet
        """
        # 标题 / Title
        sheet['A1'] = "班级管理系统 - 数据总览"
        title_font = Font(name="宋体", size=14, bold=True)
        sheet['A1'].font = title_font
        
        # 列标题 / Column headers
        headers = ["班级编号", "班级名称", "学生数", "本周总币", "累计总币", "最后更新"]
        for col, header in enumerate(headers, 1):
            cell = sheet.cell(row=3, column=col)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # 数据行 / Data rows
        for row, (class_id, classroom) in enumerate(classrooms.items(), 4):
            stats = self._calculate_stats(classroom)
            sheet.cell(row=row, column=1).value = class_id
            sheet.cell(row=row, column=2).value = classroom.name
            sheet.cell(row=row, column=3).value = len(classroom.students)
            sheet.cell(row=row, column=4).value = stats['total_weekly']
            sheet.cell(row=row, column=5).value = stats['total_cumulative']
            sheet.cell(row=row, column=6).value = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 列宽 / Column width
        sheet.column_dimensions['A'].width = 12
        sheet.column_dimensions['B'].width = 20
        sheet.column_dimensions['C'].width = 10
        sheet.column_dimensions['D'].width = 12
        sheet.column_dimensions['E'].width = 12
        sheet.column_dimensions['F'].width = 18

    def _setup_classroom_sheet(self, sheet, classroom: Classroom) -> None:
        """
        设置班级数据工作表
        / Setup classroom data sheet
        """
        # 班级信息 / Classroom info
        sheet['A1'] = f"班级: {classroom.name}"
        sheet['A1'].font = Font(size=12, bold=True)
        
        # 列标题 / Column headers
        headers = ["学生姓名", "本周币数", "累计币数"]
        for col, header in enumerate(headers, 1):
            cell = sheet.cell(row=3, column=col)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # 学生数据 / Student data
        for row, student in enumerate(classroom.students, 4):
            sheet.cell(row=row, column=1).value = student.name
            sheet.cell(row=row, column=2).value = student.weekly_coins
            sheet.cell(row=row, column=3).value = student.cumulative_coins
            
            # 居中对齐 / Center align
            for col in range(1, 4):
                sheet.cell(row=row, column=col).alignment = Alignment(horizontal="center")
        
        # 列宽 / Column width
        sheet.column_dimensions['A'].width = 20
        sheet.column_dimensions['B'].width = 12
        sheet.column_dimensions['C'].width = 12

    def _parse_classroom_sheet(self, sheet) -> Classroom:
        """
        解析班级工作表
        / Parse classroom sheet
        
        Args:
            sheet: Worksheet 对象 / Worksheet object
            
        Returns:
            Classroom 对象 / Classroom object or None
        """
        try:
            # 获取班级信息 / Get classroom info
            title = sheet['A1'].value
            if not title or "班级:" not in str(title):
                return None
            
            classroom_name = str(title).replace("班级:", "").strip()
            class_id = f"class_{sheet.title}"
            
            classroom = Classroom(name=classroom_name, class_id=class_id)
            
            # 解析学生数据 / Parse student data
            for row in range(4, sheet.max_row + 1):
                name_cell = sheet.cell(row=row, column=1).value
                if not name_cell:
                    break
                
                weekly_coins = sheet.cell(row=row, column=2).value or 0
                cumulative_coins = sheet.cell(row=row, column=3).value or 0
                
                student = Student(
                    name=str(name_cell),
                    weekly_coins=int(weekly_coins),
                    cumulative_coins=int(cumulative_coins)
                )
                classroom.add_student(student)
            
            return classroom
        except Exception as e:
            print(f"解析工作表出错: {e}")
            return None

    def _calculate_stats(self, classroom: Classroom) -> Dict[str, int]:
        """
        计算班级统计信息
        / Calculate classroom statistics
        """
        total_weekly = sum(s.weekly_coins for s in classroom.students)
        total_cumulative = sum(s.cumulative_coins for s in classroom.students)
        
        return {
            'total_weekly': total_weekly,
            'total_cumulative': total_cumulative,
            'student_count': len(classroom.students)
        }
