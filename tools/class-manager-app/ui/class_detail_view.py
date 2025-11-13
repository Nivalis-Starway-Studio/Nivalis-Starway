"""
班级详情视图 / Class detail view for managing student coins and 3-week display
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta


class ClassDetailView(tk.Frame):
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
        self.configure(bg="white", padx=20, pady=20)

        self.current_class_id = None
        self.selected_student = None

        # 标题 / Title
        self.title_label = ttk.Label(
            self, text="班级详情", font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 20))

        # 上部控制区域 / Top control area
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=(0, 15))

        back_button = ttk.Button(top_frame, text="返回主菜单", command=self.back_to_main)
        back_button.pack(side=tk.LEFT)

        # 全屏切换 / Toggle fullscreen
        fullscreen_button = ttk.Button(top_frame, text="切换全屏", command=self.toggle_fullscreen)
        fullscreen_button.pack(side=tk.LEFT, padx=(10, 0))

        # 统计信息 / Statistics
        self.stats_label = ttk.Label(top_frame, text="", font=("Arial", 10))
        self.stats_label.pack(side=tk.LEFT, expand=True, padx=(20, 0))

        # 学生管理按钮 / Student management buttons
        management_frame = ttk.Frame(top_frame)
        management_frame.pack(side=tk.RIGHT)

        add_student_button = ttk.Button(
            management_frame, text="添加学生", command=self.add_student
        )
        add_student_button.pack(side=tk.LEFT, padx=5)

        edit_student_button = ttk.Button(
            management_frame, text="修改名字", command=self.edit_student_name
        )
        edit_student_button.pack(side=tk.LEFT, padx=5)

        delete_student_button = ttk.Button(
            management_frame, text="删除学生", command=self.delete_student
        )
        delete_student_button.pack(side=tk.LEFT, padx=5)

        # 学生列表表格 - 3周显示 / Student roster treeview - 3 weeks display
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 创建Treeview / Create Treeview with 4 columns (3 weeks + total)
        columns = ("name", "week_minus2", "week_minus1", "week_0", "total")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=12,
        )

        # 定义列 / Define columns
        self.tree.heading("name", text="学生名字")
        
        # 获取周的日期范围 / Get week date ranges (上上周、上一周、本周、总计)
        week_labels = self._get_week_labels()
        self.tree.heading("week_minus2", text=f"上上周\n{week_labels[0]}")
        self.tree.heading("week_minus1", text=f"上一周\n{week_labels[1]}")
        self.tree.heading("week_0", text=f"本周\n{week_labels[2]}")
        self.tree.heading("total", text="总小码币\n累计")

        self.tree.column("name", width=150, anchor="w")
        self.tree.column("week_minus2", width=100, anchor="center")
        self.tree.column("week_minus1", width=100, anchor="center")
        self.tree.column("week_0", width=100, anchor="center")
        self.tree.column("total", width=100, anchor="center")

        # 绑定行选择事件和右键菜单 / Bind row selection and right-click menu
        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)
        self.tree.bind("<Button-3>", self.show_student_context_menu)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 滚动条 / Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # 中部控制区域 - 币数调整 / Middle control area - Coin adjustment
        control_frame = ttk.LabelFrame(self, text="币数管理", padding="10")
        control_frame.pack(fill=tk.X, pady=10)

        # 学生选择显示 / Student selection display
        student_frame = ttk.Frame(control_frame)
        student_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(student_frame, text="选中学生：").pack(side=tk.LEFT)
        self.student_display = ttk.Label(
            student_frame, text="无", foreground="blue", font=("Arial", 11, "bold")
        )
        self.student_display.pack(side=tk.LEFT, padx=(10, 0))

        # 币数调整输入 / Coin adjustment input
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="本周币数：").pack(side=tk.LEFT, padx=(0, 10))
        self.coins_var = tk.StringVar(value="0")
        self.coins_spinbox = ttk.Spinbox(
            input_frame,
            from_=0,
            to=100,
            textvariable=self.coins_var,
            width=10,
        )
        self.coins_spinbox.pack(side=tk.LEFT, padx=(0, 10))

        # 更新按钮 / Update button
        update_button = ttk.Button(
            input_frame, text="更新本周币", command=self.update_student_coins
        )
        update_button.pack(side=tk.LEFT, padx=5)

        # 编辑历史币数按钮 / Edit historical coins button
        edit_history_button = ttk.Button(
            input_frame, text="编辑历史币数", command=self.edit_historical_coins
        )
        edit_history_button.pack(side=tk.LEFT, padx=5)

        # 重置周币按钮 / Reset weekly coins button
        reset_button = ttk.Button(
            input_frame, text="重置全班周币", command=self.reset_weekly_coins
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def show_student_context_menu(self, event) -> None:
        """
        显示学生右键菜单 - 仅在学生名字列有效
        / Show student context menu - only in student name column
        """
        # 获取点击位置的行和列 / Get row and column at click position
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        # 只在名字列（#1 是第一个数据列，显示为 name）显示菜单 / Only show menu on name column
        if item and column == "#1":
            self.tree.selection_set(item)
            values = self.tree.item(item, "values")
            student_name = values[0]
            
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="修改学生姓名", command=lambda: self.edit_student_name())
            context_menu.add_command(label="删除学生", command=lambda: self.delete_student())
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

    def _get_week_labels(self) -> list:
        """
        获取3周的标签 / Get labels for 3 weeks (上上周、上一周、本周)
        返回: [上上周, 上一周, 本周]的日期范围
        """
        labels = []
        current_date = datetime.now()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        
        # 获取上上周 / Get week before last week
        prev_prev_week_start = start_of_week - timedelta(weeks=2)
        prev_prev_week_end = prev_prev_week_start + timedelta(days=6)
        labels.append(f"{prev_prev_week_start.strftime('%m/%d')}-{prev_prev_week_end.strftime('%m/%d')}")
        
        # 获取上一周 / Get last week
        prev_week_start = start_of_week - timedelta(weeks=1)
        prev_week_end = prev_week_start + timedelta(days=6)
        labels.append(f"{prev_week_start.strftime('%m/%d')}-{prev_week_end.strftime('%m/%d')}")
        
        # 获取本周 / Get this week
        this_week_end = start_of_week + timedelta(days=6)
        labels.append(f"{start_of_week.strftime('%m/%d')}-{this_week_end.strftime('%m/%d')}")
        
        return labels

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
        刷新学生表格数据（显示3周+总计）
        / Refresh the student table with 3 weeks data plus total
        """
        if not self.current_class_id:
            return

        # 清空现有行 / Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 加载学生数据 / Load student data
        classroom = self.controller.data_store.get_classroom(self.current_class_id)
        for student in classroom.get_all_students():
            # 获取3周的币数（上上周、上一周、本周）/ Get coins for 3 weeks
            current_week = self.controller.data_store.current_week
            week_minus2 = student.weekly_history.get(current_week - 2, 0)
            week_minus1 = student.weekly_history.get(current_week - 1, 0)
            week_0 = student.weekly_coins  # 本周使用当前的weekly_coins

            # 计算总小码币数量 / Calculate total coins
            total = student.cumulative_coins + week_0

            self.tree.insert(
                "",
                "end",
                values=(
                    student.name,
                    week_minus2,
                    week_minus1,
                    week_0,
                    total,
                ),
                tags=("student_row",)
            )

    def on_row_selected(self, event) -> None:
        """
        处理表格行选择事件
        / Handle table row selection
        """
        selection = self.tree.selection()
        if not selection:
            self.selected_student = None
            self.student_display.config(text="无")
            self.coins_var.set("0")
            return

        item = selection[0]
        values = self.tree.item(item, "values")
        self.selected_student = values[0]  # 学生名字 / Student name
        # 新列结构: name, week_minus2, week_minus1, week_0, total
        # 索引:    0    1            2             3      4
        weekly_coins = int(values[3])  # 本周币数 / This week coins (index 3: week_0)

        self.student_display.config(text=self.selected_student)
        self.coins_var.set(str(weekly_coins))

    def update_student_coins(self) -> None:
        """
        更新选中学生的周币
        / Update the selected student's weekly coins
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

        # 确认更新 / Confirm update
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

    def edit_historical_coins(self) -> None:
        """
        编辑学生的历史周币 / Edit student's historical coins
        """
        if not self.selected_student:
            messagebox.showwarning("未选择学生", "请先在表格中选择一个学生。")
            return

        classroom = self.controller.data_store.get_classroom(self.current_class_id)
        student = classroom.get_student_by_name(self.selected_student)
        
        if not student:
            messagebox.showerror("错误", "学生信息加载失败")
            return

        # 创建编辑对话框 / Create edit dialog
        dialog = tk.Toplevel(self)
        dialog.title(f"编辑 {self.selected_student} 的币数历史")
        dialog.geometry("400x300")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        # 获取当前周数 / Get current week
        current_week = self.controller.data_store.current_week
        
        # 创建输入框 / Create input fields
        ttk.Label(dialog, text="周数管理", font=("Arial", 12, "bold")).pack(pady=(10, 20))
        
        input_vars = {}
        weeks_info = [
            (current_week - 2, "上上周"),
            (current_week - 1, "上一周"),
            (current_week, "本周"),
        ]
        
        for week_num, week_label in weeks_info:
            frame = ttk.Frame(dialog)
            frame.pack(fill=tk.X, padx=20, pady=5)
            
            ttk.Label(frame, text=f"{week_label} ({week_num}周)：", width=15).pack(side=tk.LEFT)
            
            coin_value = student.weekly_history.get(week_num, 0)
            if week_num == current_week:
                coin_value = student.weekly_coins
            
            var = tk.StringVar(value=str(coin_value))
            input_vars[week_num] = var
            
            spinbox = ttk.Spinbox(
                frame,
                from_=0,
                to=100,
                textvariable=var,
                width=10,
            )
            spinbox.pack(side=tk.LEFT, padx=(10, 0))

        # 按钮 / Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def confirm():
            try:
                # 更新历史周币 / Update historical coins
                for week_num, var in input_vars.items():
                    new_coins = int(var.get())
                    if new_coins < 0:
                        messagebox.showerror("输入错误", "币数不能为负数。")
                        return
                    
                    if week_num == current_week:
                        # 本周更新weekly_coins / Update current week coins
                        student.weekly_coins = new_coins
                    else:
                        # 历史周更新到weekly_history / Update historical coins
                        student.weekly_history[week_num] = new_coins
                
                self.controller.data_store.save_to_storage()
                dialog.destroy()
                self.refresh_student_table()
                self.update_statistics()
                messagebox.showinfo("成功", "学生币数历史已更新。")
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的数字。")

        ttk.Button(button_frame, text="确定", command=confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def reset_weekly_coins(self) -> None:
        """
        重置全班周币，并累加到累计币
        / Reset all students' weekly coins and add to cumulative
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
        / Update classroom statistics
        """
        stats = self.controller.data_store.get_classroom_stats(self.current_class_id)
        if stats:
            stats_text = (
                f"学生数: {stats['student_count']} | "
                f"本周总币: {stats['total_weekly']} | "
                f"累计总币: {stats['total_cumulative']}"
            )
            self.stats_label.config(text=stats_text)

    def add_student(self) -> None:
        """
        添加新学生到班级 / Add a new student to classroom
        """
        dialog = tk.Toplevel(self)
        dialog.title("添加学生")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(dialog, text="学生名字：").pack(pady=(10, 0), padx=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5, padx=10, fill=tk.X)
        name_entry.focus()

        def confirm():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("输入错误", "学生名字不能为空。")
                return
            
            # 检查学生是否已存在 / Check if student already exists
            classroom = self.controller.data_store.get_classroom(self.current_class_id)
            if classroom.get_student_by_name(name):
                messagebox.showwarning("输入错误", f"学生 {name} 已存在于班级中。")
                return
            
            self.controller.data_store.add_student_to_classroom(
                self.current_class_id, name
            )
            dialog.destroy()
            self.refresh_student_table()
            self.update_statistics()
            messagebox.showinfo("成功", f"学生 {name} 已添加到班级。")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="确定", command=confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def edit_student_name(self) -> None:
        """
        修改学生名字 / Edit student name
        """
        if not self.selected_student:
            messagebox.showwarning("未选择学生", "请先在表格中选择一个学生。")
            return

        dialog = tk.Toplevel(self)
        dialog.title("修改学生名字")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(dialog, text="新名字：").pack(pady=(10, 0), padx=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, self.selected_student)
        name_entry.pack(pady=5, padx=10, fill=tk.X)
        name_entry.focus()

        def confirm():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("输入错误", "学生名字不能为空。")
                return
            
            if new_name == self.selected_student:
                dialog.destroy()
                return
            
            # 检查新名字是否已存在 / Check if new name already exists
            classroom = self.controller.data_store.get_classroom(self.current_class_id)
            if classroom.get_student_by_name(new_name):
                messagebox.showwarning("输入错误", f"学生 {new_name} 已存在于班级中。")
                return
            
            if self.controller.data_store.update_student_name(
                self.current_class_id, self.selected_student, new_name
            ):
                dialog.destroy()
                self.selected_student = None
                self.student_display.config(text="无")
                self.coins_var.set("0")
                self.refresh_student_table()
                messagebox.showinfo("成功", f"学生名字已修改为 {new_name}。")
            else:
                messagebox.showerror("失败", "修改学生名字失败。")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="确定", command=confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_student(self) -> None:
        """
        删除学生 / Delete a student
        """
        if not self.selected_student:
            messagebox.showwarning("未选择学生", "请先在表格中选择一个学生。")
            return

        if messagebox.askyesno(
            "确认删除",
            f"确定要删除学生 {self.selected_student} 吗？\n此操作不可撤销。",
        ):
            if self.controller.data_store.remove_student_from_classroom(
                self.current_class_id, self.selected_student
            ):
                self.selected_student = None
                self.student_display.config(text="无")
                self.coins_var.set("0")
                self.refresh_student_table()
                self.update_statistics()
                messagebox.showinfo("成功", "学生已删除。")
            else:
                messagebox.showerror("失败", "删除学生失败。")

    def toggle_fullscreen(self) -> None:
        """
        切换全屏模式 / Toggle fullscreen mode
        """
        current_state = self.controller.state()
        if current_state == 'zoomed':
            self.controller.state('normal')
        else:
            self.controller.state('zoomed')

    def back_to_main(self) -> None:
        """
        返回主视图
        / Return to main view
        """
        self.selected_student = None
        self.coins_var.set("0")
        self.student_display.config(text="无")
        self.controller.show_frame("MainView")

    def reset(self) -> None:
        """重置班级详情视图 / Reset class detail view"""
        self.selected_student = None
        self.coins_var.set("0")
        self.student_display.config(text="无")
