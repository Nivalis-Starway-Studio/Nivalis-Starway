"""
班级详情视图
"""

import tkinter as tk
from tkinter import ttk, messagebox


class ClassDetailView(ttk.Frame):
    """班级详情视图框架"""

    def __init__(self, parent, controller, **kwargs):
        """
        初始化班级详情视图
        
        Args:
            parent: 父级窗口
            controller: 应用控制器
        """
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(padding="20")

        self.current_class_id = None
        self.selected_student = None

        # 标题
        self.title_label = ttk.Label(
            self, text="班级详情", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        # 上部控制区域
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="返回主菜单", command=self.back_to_main)
        back_button.pack(side=tk.LEFT)

        # 统计信息
        self.stats_label = ttk.Label(top_frame, text="", font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT, expand=True, padx=(20, 0))

        # 学生列表表格
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 创建表格视图
        columns = ("name", "weekly", "cumulative")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        # 定义列
        self.tree.heading("name", text="学生名字")
        self.tree.heading("weekly", text="周币")
        self.tree.heading("cumulative", text="累计币")

        self.tree.column("name", width=200, anchor="w")
        self.tree.column("weekly", width=100, anchor="center")
        self.tree.column("cumulative", width=100, anchor="center")

        # 绑定行选择事件
        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # 中部控制区域 - 币数调整
        control_frame = ttk.LabelFrame(self, text="币数管理", padding="10")
        control_frame.pack(fill=tk.X, pady=10)

        # 学生选择显示
        student_frame = ttk.Frame(control_frame)
        student_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(student_frame, text="选中学生：").pack(side=tk.LEFT)
        self.student_display = ttk.Label(
            student_frame, text="无", foreground="blue", font=("Arial", 11, "bold")
        )
        self.student_display.pack(side=tk.LEFT, padx=(10, 0))

        # 币数调整输入
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="新周币数：").pack(side=tk.LEFT, padx=(0, 10))
        self.coins_var = tk.StringVar(value="0")
        self.coins_spinbox = ttk.Spinbox(
            input_frame,
            from_=0,
            to=100,
            textvariable=self.coins_var,
            width=10,
        )
        self.coins_spinbox.pack(side=tk.LEFT, padx=(0, 10))

        # 更新按钮
        update_button = ttk.Button(
            input_frame, text="更新周币", command=self.update_student_coins
        )
        update_button.pack(side=tk.LEFT, padx=5)

        # 重置周币按钮
        reset_button = ttk.Button(
            input_frame, text="重置全班周币", command=self.reset_weekly_coins
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def load_classroom_data(self, class_id: str) -> None:
        """
        加载班级数据并刷新表格
        
        Args:
            class_id: 班级ID
        """
        self.current_class_id = class_id
        classroom = self.controller.data_store.get_classroom(class_id)

        if not classroom:
            messagebox.showerror("错误", "班级数据加载失败")
            return

        # 更新标题
        self.title_label.config(text=f"班级详情 - {classroom.name}")

        # 刷新表格
        self.refresh_student_table()

        # 更新统计信息
        self.update_statistics()

    def refresh_student_table(self) -> None:
        """
        刷新学生表格数据
        """
        if not self.current_class_id:
            return

        # 清空现有行
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 加载学生数据
        classroom = self.controller.data_store.get_classroom(self.current_class_id)
        for student in classroom.get_all_students():
            self.tree.insert(
                "",
                "end",
                values=(
                    student.name,
                    student.weekly_coins,
                    student.cumulative_coins,
                ),
            )

    def on_row_selected(self, event) -> None:
        """
        处理表格行选择事件
        """
        selection = self.tree.selection()
        if not selection:
            self.selected_student = None
            self.student_display.config(text="无")
            self.coins_var.set("0")
            return

        item = selection[0]
        values = self.tree.item(item, "values")
        self.selected_student = values[0]  # 学生名字
        weekly_coins = int(values[1])

        self.student_display.config(text=self.selected_student)
        self.coins_var.set(str(weekly_coins))

    def update_student_coins(self) -> None:
        """
        更新选中学生的周币
        """
        if not self.selected_student:
            messagebox.showwarning("未选择学生", "请先在表格中选择一个学生。")
            return

        try:
            new_coins = int(self.coins_var.get())
            if new_coins < 0:
                messagebox.showerror("输入错误", "币数不能为负数。")
                return
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字。")
            return

        # 确认更新
        if messagebox.askyesno(
            "确认更新",
            f"确认将 {self.selected_student} 的周币更新为 {new_coins}?",
        ):
            self.controller.data_store.update_student_weekly_coins(
                self.current_class_id, self.selected_student, new_coins
            )
            self.refresh_student_table()
            self.update_statistics()
            messagebox.showinfo("更新成功", "学生币数已成功更新。")

    def reset_weekly_coins(self) -> None:
        """
        重置全班周币，并累加到累计币
        """
        classroom = self.controller.data_store.get_classroom(self.current_class_id)

        if messagebox.askyesno(
            "确认重置",
            f"确认重置班级 {classroom.name} 的所有周币?\n\n周币将被加入累计币中。",
        ):
            self.controller.data_store.reset_weekly_coins(self.current_class_id)
            self.refresh_student_table()
            self.update_statistics()
            messagebox.showinfo("重置成功", "周币已重置，并已累加到累计币中。")

    def update_statistics(self) -> None:
        """
        更新班级统计信息
        """
        stats = self.controller.data_store.get_classroom_stats(self.current_class_id)
        if stats:
            stats_text = (
                f"学生数: {stats['student_count']} | "
                f"本周总币: {stats['total_weekly']} | "
                f"累计总币: {stats['total_cumulative']}"
            )
            self.stats_label.config(text=stats_text)

    def back_to_main(self) -> None:
        """
        返回主视图
        """
        self.selected_student = None
        self.coins_var.set("0")
        self.student_display.config(text="无")
        self.controller.show_frame("MainView")

    def reset(self) -> None:
        """重置班级详情视图"""
        self.selected_student = None
        self.coins_var.set("0")
        self.student_display.config(text="无")
