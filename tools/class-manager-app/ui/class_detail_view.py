"""
班级详情视图 / Class detail view for managing student coins
"""

import tkinter as tk
from tkinter import ttk, messagebox
from utils.week_utils import get_current_week


class ClassDetailView(ttk.Frame):
    """班级详情视图框架 / Class detail view frame"""

    def __init__(self, parent, controller, **kwargs):
        """
        初始化班级详情视图
        / Initialize the class detail view
        
        Args:
            parent: 父级窗口 / Parent window
            controller: 应用控制器 / Application controller
        """
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.configure(padding="20")

        self.current_class_id = None
        self.current_week = get_current_week()
        self.displayed_weeks = []

        # 标题 / Title
        self.title_label = ttk.Label(
            self, text="班级详情", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 10))

        # 当前周数显示 / Current week display
        self.week_info_label = ttk.Label(
            self, 
            text=f"当前是第 {self.current_week} 周", 
            font=("Arial", 11),
            foreground="blue"
        )
        self.week_info_label.pack(pady=(0, 10))

        # 上部控制区域 / Top control area
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="返回主菜单", command=self.back_to_main)
        back_button.pack(side=tk.LEFT)

        # 统计信息 / Statistics
        self.stats_label = ttk.Label(top_frame, text="", font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT, expand=True, padx=(20, 0))

        # 学生列表表格 / Student roster treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 创建Treeview，显示4周的数据
        # Create Treeview showing 4 weeks of data
        self.displayed_weeks = self._get_displayed_weeks()
        columns = ["name"] + [f"week{w}" for w in self.displayed_weeks] + ["cumulative"]
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        # 定义列 / Define columns
        self.tree.heading("name", text="学生名字")
        for week_num in self.displayed_weeks:
            week_col = f"week{week_num}"
            week_label = f"第{week_num}周"
            if week_num == self.current_week:
                week_label += " (当前)"
            self.tree.heading(week_col, text=week_label)
        self.tree.heading("cumulative", text="累计币")

        # 设置列宽 / Set column widths
        self.tree.column("name", width=120, anchor="w")
        for week_num in self.displayed_weeks:
            self.tree.column(f"week{week_num}", width=80, anchor="center")
        self.tree.column("cumulative", width=100, anchor="center")

        # 绑定双击事件用于编辑 / Bind double-click for editing
        self.tree.bind("<Double-1>", self.on_cell_double_click)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 滚动条 / Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # 说明标签 / Instruction label
        instruction_label = ttk.Label(
            self,
            text="💡 提示：双击周币单元格可直接编辑，修改后累计币会自动更新",
            font=("Arial", 9),
            foreground="gray"
        )
        instruction_label.pack(pady=5)

    def _get_displayed_weeks(self) -> list:
        """
        获取要显示的4周周数
        / Get 4 weeks to display
        
        Returns:
            周数列表 / List of week numbers
        """
        # 显示当前周及前3周（如果当前周<4，则从第1周开始）
        # Display current week and previous 3 weeks
        if self.current_week <= 4:
            return list(range(1, 5))
        else:
            return list(range(self.current_week - 3, self.current_week + 1))

    def load_classroom_data(self, class_id: str) -> None:
        """
        加载班级数据并刷新表格
        / Load classroom data and refresh the table
        
        Args:
            class_id: 班级ID / Classroom ID
        """
        self.current_class_id = class_id
        classroom = self.controller.data_store.get_classroom(class_id)

        if not classroom:
            messagebox.showerror("错误", "班级数据加载失败")
            return

        # 更新标题 / Update title
        self.title_label.config(text=f"班级详情 - {classroom.name}")

        # 刷新表格 / Refresh table
        self.refresh_student_table()

        # 更新统计信息 / Update statistics
        self.update_statistics()

    def refresh_student_table(self) -> None:
        """
        刷新学生表格数据
        / Refresh the student table with current data
        """
        if not self.current_class_id:
            return

        # 清空现有行 / Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 加载学生数据 / Load student data
        classroom = self.controller.data_store.get_classroom(self.current_class_id)
        for student in classroom.get_all_students():
            # 构建行数据 / Build row data
            row_values = [student.name]
            
            # 添加各周币数 / Add week coins
            for week_num in self.displayed_weeks:
                coins = student.week_coins.get(week_num, 0)
                row_values.append(coins)
            
            # 添加累计币 / Add cumulative coins
            row_values.append(student.cumulative_coins)
            
            self.tree.insert("", "end", values=tuple(row_values))

    def on_cell_double_click(self, event) -> None:
        """
        处理单元格双击事件，弹出编辑对话框
        / Handle cell double-click event, show edit dialog
        """
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        item = self.tree.identify_row(event.y)
        
        if not item:
            return

        # 获取列索引 / Get column index
        col_idx = int(column.replace("#", "")) - 1
        
        # 只有周币列可以编辑（不包括名字和累计币）
        # Only week coin columns are editable
        if col_idx < 1 or col_idx > len(self.displayed_weeks):
            return

        # 获取学生名字和周数 / Get student name and week number
        values = self.tree.item(item, "values")
        student_name = values[0]
        week_num = self.displayed_weeks[col_idx - 1]
        current_coins = values[col_idx]

        # 弹出编辑对话框 / Show edit dialog
        self.show_edit_dialog(student_name, week_num, current_coins, item, col_idx)

    def show_edit_dialog(self, student_name: str, week_num: int, current_coins, item, col_idx) -> None:
        """
        显示编辑对话框
        / Show edit dialog
        
        Args:
            student_name: 学生名字 / Student name
            week_num: 周数 / Week number
            current_coins: 当前币数 / Current coin amount
            item: 树节点ID / Tree item ID
            col_idx: 列索引 / Column index
        """
        dialog = tk.Toplevel(self)
        dialog.title(f"编辑 {student_name} 第{week_num}周的币数")
        dialog.geometry("350x150")
        dialog.transient(self)
        dialog.grab_set()

        # 居中对话框 / Center dialog
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # 标签 / Label
        ttk.Label(
            dialog,
            text=f"学生：{student_name}\n第{week_num}周币数",
            font=("Arial", 11)
        ).pack(pady=15)

        # 输入框 / Entry
        coins_var = tk.StringVar(value=str(current_coins))
        entry = ttk.Entry(dialog, textvariable=coins_var, width=15, font=("Arial", 12))
        entry.pack(pady=10)
        entry.focus()
        entry.select_range(0, tk.END)

        # 按钮框架 / Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=15)

        def on_confirm():
            try:
                new_coins = int(coins_var.get())
                if new_coins < 0:
                    messagebox.showerror("输入错误", "币数不能为负数。", parent=dialog)
                    return
                
                # 更新数据 / Update data
                success = self.controller.data_store.update_student_week_coins(
                    self.current_class_id, student_name, week_num, new_coins
                )
                
                if success:
                    # 刷新表格和统计 / Refresh table and stats
                    self.refresh_student_table()
                    self.update_statistics()
                    dialog.destroy()
                else:
                    messagebox.showerror("更新失败", "更新币数失败。", parent=dialog)
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数字。", parent=dialog)

        def on_cancel():
            dialog.destroy()

        # 绑定回车键确认 / Bind Enter key to confirm
        entry.bind("<Return>", lambda e: on_confirm())
        entry.bind("<Escape>", lambda e: on_cancel())

        ttk.Button(button_frame, text="确认", command=on_confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.LEFT, padx=5)

    def update_statistics(self) -> None:
        """
        更新班级统计信息
        / Update classroom statistics
        """
        stats = self.controller.data_store.get_classroom_stats(
            self.current_class_id, 
            weeks=self.displayed_weeks
        )
        if stats:
            # 构建统计文本 / Build stats text
            stats_parts = [f"学生数: {stats['student_count']}"]
            
            # 添加各周总币数 / Add week totals
            for week_num in self.displayed_weeks:
                week_total = stats['week_totals'].get(week_num, 0)
                stats_parts.append(f"第{week_num}周: {week_total}")
            
            stats_parts.append(f"累计总币: {stats['total_cumulative']}")
            
            stats_text = " | ".join(stats_parts)
            self.stats_label.config(text=stats_text)

    def back_to_main(self) -> None:
        """
        返回主视图
        / Return to main view
        """
        self.controller.show_frame("MainView")

    def reset(self) -> None:
        """重置班级详情视图 / Reset class detail view"""
        pass
