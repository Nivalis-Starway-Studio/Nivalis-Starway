"""
班级详情视图 / Class detail view for managing student coins and 4-week display
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib
    matplotlib.use('TkAgg')  # 设置matplotlib后端
    CHART_AVAILABLE = True
except ImportError:
    CHART_AVAILABLE = False


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

        # 图表统计按钮 / Chart statistics button
        chart_button = ttk.Button(top_frame, text="图表统计", command=self.show_chart_statistics)
        chart_button.pack(side=tk.RIGHT, padx=(0, 10))

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

        # 学生列表表格 - 3周显示+总计 / Student roster treeview - 3 weeks + total display
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 创建Treeview / Create Treeview with 5 columns (name + 3 weeks + total)
        columns = ("name", "week_minus2", "week_minus1", "week_0", "total")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15,
        )

        # 通过样式配置增加行高和标题行高 / Increase row height and heading height through style configuration
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # 设置数据行高为40像素
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), 
                       padding=(10, 8))  # 设置标题字体和内边距，增加标题行高度

        # 定义列 / Define columns
        self.tree.heading("name", text="学生名字")
        
        # 获取周的日期范围 / Get week date ranges
        week_labels = self._get_week_labels()
        self.tree.heading("week_minus2", text=f"上上周 {week_labels[0]}")
        self.tree.heading("week_minus1", text=f"上周 {week_labels[1]}")
        self.tree.heading("week_0", text=f"本周 {week_labels[2]}")
        self.tree.heading("total", text="总小码币/累计")

        self.tree.column("name", width=120, anchor="w")
        self.tree.column("week_minus2", width=180, anchor="center")
        self.tree.column("week_minus1", width=180, anchor="center")
        self.tree.column("week_0", width=180, anchor="center")
        self.tree.column("total", width=140, anchor="center")

        # 绑定行选择事件和右键菜单 / Bind row selection and right-click menu
        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)
        self.tree.bind("<Button-3>", self.show_student_context_menu)
        self.tree.bind("<Double-Button-1>", self.on_cell_double_click)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 滚动条 / Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=scrollbar.set)

        # 中部控制区域 - 币数调整 / Middle control area - Coin adjustment
        control_frame = ttk.LabelFrame(self, text="币数管理（本周）", padding="10")
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

        # 更新按钮 / Update button
        update_button = ttk.Button(
            input_frame, text="更新周币", command=self.update_student_coins
        )
        update_button.pack(side=tk.LEFT, padx=5)

        # 说明文字 / Description
        desc_label = ttk.Label(control_frame, text="提示：未选中学生时，将更新全班学生；选中学生时，仅更新该学生。", 
                              font=("Arial", 9), foreground="gray")
        desc_label.pack(pady=(10, 0))

    def show_student_context_menu(self, event) -> None:
        """
        显示学生右键菜单（仅在人名列有效）
        / Show student context menu (only effective in name column)
        """
        # 获取点击位置的学生 / Get student at click position
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item:  # 允许在任何列右键点击以选中学生
            self.tree.selection_set(item)  # 选中该行
            values = self.tree.item(item, "values")
            student_name = values[0]
            
            # 更新选中学生状态 / Update selected student state
            self.selected_student = student_name
            self.student_display.config(text=self.selected_student)
            try:
                weekly_coins = int(values[3])
            except (TypeError, ValueError):
                weekly_coins = 0
            self.coins_var.set(str(weekly_coins))

            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(
                label="修改学生姓名", command=lambda: self.edit_student_name()
            )
            context_menu.add_command(
                label="删除学生", command=lambda: self.delete_student()
            )

            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()

    def _get_week_labels(self) -> list:
        """
        获取三周的标签（上上周、上周、本周）
        / Get labels for three weeks (two previous weeks and current week)
        """
        labels = []
        current_date = datetime.now()
        start_of_week = current_date - timedelta(days=current_date.weekday())

        # 上上周
        week_minus2_start = start_of_week - timedelta(weeks=2)
        week_minus2_end = week_minus2_start + timedelta(days=6)
        labels.append(
            f"{week_minus2_start.strftime('%m/%d')}-{week_minus2_end.strftime('%m/%d')}"
        )

        # 上周
        week_minus1_start = start_of_week - timedelta(weeks=1)
        week_minus1_end = week_minus1_start + timedelta(days=6)
        labels.append(
            f"{week_minus1_start.strftime('%m/%d')}-{week_minus1_end.strftime('%m/%d')}"
        )

        # 本周
        week_0_end = start_of_week + timedelta(days=6)
        labels.append(f"{start_of_week.strftime('%m/%d')}-{week_0_end.strftime('%m/%d')}")

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
        / Refresh the student table with 3 weeks + total data
        """
        if not self.current_class_id:
            return

        # 清空现有行 / Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 加载学生数据 / Load student data
        classroom = self.controller.data_store.get_classroom(self.current_class_id)
        data_store = self.controller.data_store
        for student in classroom.get_all_students():
            # 获取3周的币数 / Get coins for 3 weeks
            week_minus2 = data_store.get_student_week_value(student, -2)
            week_minus1 = data_store.get_student_week_value(student, -1)
            week_0 = data_store.get_student_week_value(student, 0)

            # 计算总小码币数量 / Calculate total coins
            total = data_store.get_student_total(student)

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
        week_value = values[3]
        try:
            weekly_coins = int(week_value)
        except (TypeError, ValueError):
            weekly_coins = 0

        self.student_display.config(text=self.selected_student)
        self.coins_var.set(str(weekly_coins))

    def on_cell_double_click(self, event) -> None:
        """
        处理单元格双击事件 - 编辑币数
        / Handle cell double-click event - Edit coins
        """
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not item:
            return

        values = self.tree.item(item, "values")
        student_name = values[0]

        # 定义列索引对应的周偏移量
        column_map = {"#2": -2, "#3": -1, "#4": 0}  # 上上周、上周、本周
        index_map = {"#2": 1, "#3": 2, "#4": 3}

        if column in column_map:
            week_offset = column_map[column]
            value_index = index_map[column]
            try:
                current_value = int(values[value_index])
            except (TypeError, ValueError):
                current_value = 0

            # 弹出输入对话框
            new_value = simpledialog.askinteger(
                "修改小码币",
                f"修改 {student_name} 的小码币数量\n（当前: {current_value}）",
                initialvalue=current_value,
                minvalue=0,
                maxvalue=1000,
            )

            if new_value is not None:
                # 更新数据
                if self._update_week_coins(student_name, week_offset, new_value):
                    self.refresh_student_table()
                    self.update_statistics()
                    messagebox.showinfo("更新成功", f"已更新 {student_name} 的小码币数量")
                else:
                    messagebox.showerror("更新失败", "未能更新小码币，请重试。")

    def _update_week_coins(
        self, student_name: str, week_offset: int, coins: int
    ) -> bool:
        """
        更新指定周的币数
        / Update coins for specified week

        Args:
            student_name: 学生名字
            week_offset: 周偏移量（-2=上上周，-1=上周，0=本周）
            coins: 币数

        Returns:
            bool: 是否更新成功 / Whether the update succeeded
        """
        return self.controller.data_store.update_student_week_coins(
            self.current_class_id, student_name, week_offset, coins
        )

    def update_student_coins(self) -> None:
        """
        更新学生周币 - 支持全班更新和单个学生更新
        / Update student weekly coins - supports both class-wide and individual updates
        """
        try:
            new_coins = int(self.coins_var.get())
            if new_coins < 0:
                messagebox.showerror("输入错误", "币数不能为负数。")
                return
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字。")
            return

        if not self.selected_student:
            # 更新全班学生 / Update all students in class
            classroom = self.controller.data_store.get_classroom(self.current_class_id)
            if messagebox.askyesno(
                "确认全班更新",
                f"确认为班级 {classroom.name} 的所有学生添加 {new_coins} 小码币到本周列?\n"
                f"每个学生的总小码币也将相应增加。",
            ):
                data_store = self.controller.data_store
                for student in classroom.get_all_students():
                    # 获取当前本周币数
                    current_weekly = data_store.get_student_week_value(student, 0)
                    # 更新本周币数
                    data_store.update_student_week_coins(self.current_class_id, student.name, 0, current_weekly + new_coins)
                
                self.refresh_student_table()
                self.update_statistics()
                messagebox.showinfo("更新成功", f"已为全班所有学生添加 {new_coins} 小码币。")
        else:
            # 更新单个学生 / Update individual student
            if messagebox.askyesno(
                "确认更新",
                f"确认将 {self.selected_student} 的周币更新为 {new_coins}?",
            ):
                self.controller.data_store.update_student_weekly_coins(
                    self.current_class_id, self.selected_student, new_coins
                )
                self.refresh_student_table()
                self.update_statistics()
                messagebox.showinfo("更新成功", f"学生 {self.selected_student} 的币数已成功更新。")

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

    def show_chart_statistics(self) -> None:
        """
        显示图表统计窗口 - 包含折线图和柱状图
        / Show chart statistics window - includes line charts and bar chart
        """
        if not CHART_AVAILABLE:
            messagebox.showerror("功能不可用", "图表统计功能需要安装matplotlib库。")
            return
            
        if not self.current_class_id:
            messagebox.showerror("错误", "请先加载班级数据。")
            return
            
        # 创建新窗口 / Create new window
        chart_window = tk.Toplevel(self)
        chart_window.title("班级小码币统计图表")
        
        # ============ 获取屏幕尺寸并自适应窗口 / Get screen size and adapt window ============
        screen_width = chart_window.winfo_screenwidth()
        screen_height = chart_window.winfo_screenheight()
        
        # 窗口占屏幕的90%（留出边距）/ Window takes 90% of screen (leave margins)
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # 计算窗口居中位置 / Calculate centered position
        x_offset = (screen_width - window_width) // 2
        y_offset = (screen_height - window_height) // 2
        
        chart_window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
        chart_window.state('zoomed')  # 最大化窗口 / Maximize window
        
        chart_window.transient(self.winfo_toplevel())
        chart_window.grab_set()
        
        # 重新加载班级数据以获取最新的学生列表（包括新添加的学生）
        # / Reload classroom data to get the latest student list (including newly added students)
        data_store = self.controller.data_store
        classroom = data_store.get_classroom(self.current_class_id)
        
        # 准备数据 / Prepare data
        student_names = []
        total_coins = []
        all_students = list(classroom.get_all_students())
        
        for student in all_students:
            student_names.append(student.name)
            total_coins.append(data_store.get_student_total(student))
        
        # 设置中文字体 / Set Chinese font
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 计算需要的行数 - 每行显示2个学生的折线图 / Calculate rows needed - 2 students per row
        num_students = len(student_names)
        line_chart_rows = max(1, (num_students + 1) // 2)  # 每行2个学生 / 2 students per row
        
        # ============ 创建主框架，划分两个区域 / Create main frame with two regions ============
        main_frame = ttk.Frame(chart_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ============ 上方区域：折线图（可滚动）/ Top region: Line charts (scrollable) ============
        line_frame = ttk.LabelFrame(main_frame, text="学生小码币变化趋势", padding=10)
        line_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建Canvas和Scrollbar用于滚动 / Create Canvas and Scrollbar for scrolling
        line_canvas = tk.Canvas(line_frame, bg='white')
        line_scrollbar = ttk.Scrollbar(line_frame, orient="vertical", command=line_canvas.yview)
        scrollable_line_frame = ttk.Frame(line_canvas)
        
        scrollable_line_frame.bind(
            "<Configure>",
            lambda e: line_canvas.configure(scrollregion=line_canvas.bbox("all"))
        )
        
        line_canvas.create_window((0, 0), window=scrollable_line_frame, anchor="nw")
        line_canvas.configure(yscrollcommand=line_scrollbar.set)
        
        line_canvas.pack(side="left", fill="both", expand=True)
        line_scrollbar.pack(side="right", fill="y")
        
        # 绑定鼠标滚轮事件 / Bind mouse wheel event
        def _on_mousewheel(event):
            line_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        line_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ============ 根据屏幕尺寸自适应计算图表大小 / Adaptively calculate chart size based on screen ============
        # 计算可用宽度（转换为英寸，DPI通常为100）/ Calculate available width (convert to inches, DPI usually 100)
        dpi = 100
        available_width_inches = (window_width - 80) / dpi  # 减去边距 / Minus margins
        
        # 每行高度根据屏幕高度自适应，确保每行的折线图完整显示 / Row height adapts to screen height, ensuring complete display
        # 折线图区域占窗口高度的60%，柱状图占25%，其他控件占15%
        line_area_height = window_height * 0.6  # 折线图区域更大 / Line chart area larger
        line_height_per_row = max(3.0, line_area_height / dpi / max(1, line_chart_rows))
        total_line_height = line_chart_rows * line_height_per_row
        
        # 创建折线图Figure，宽度自适应屏幕 / Create line chart figure with adaptive width
        fig_line = plt.figure(figsize=(available_width_inches, total_line_height))
        
        # 使用GridSpec布局，每行2列 / Use GridSpec layout with 2 columns per row
        line_gs = fig_line.add_gridspec(
            line_chart_rows, 2,
            hspace=0.35,
            wspace=0.25,
            left=0.06,
            right=0.98,
            top=0.95,
            bottom=0.05
        )
        
        # 使用颜色列表为不同学生的折线图着色 / Use color list to color different students' line charts
        colors_line = ['#2E7D32', '#1565C0', '#D32F2F', '#F57C00', '#7B1FA2', '#00796B', '#C2185B']
        
        for idx, student in enumerate(all_students):
            row = idx // 2  # 行索引 / Row index
            col = idx % 2   # 列索引 / Column index
            
            ax = fig_line.add_subplot(line_gs[row, col])
            
            # 获取三周数据 / Get three weeks data
            week_minus2 = data_store.get_student_week_value(student, -2)
            week_minus1 = data_store.get_student_week_value(student, -1)
            week_0 = data_store.get_student_week_value(student, 0)
            
            weeks = ['上上周', '上周', '本周']
            coins = [week_minus2, week_minus1, week_0]
            
            # 为每个学生选择不同的颜色 / Select different color for each student
            line_color = colors_line[idx % len(colors_line)]
            
            # 绘制折线图 / Plot line chart
            ax.plot(weeks, coins, marker='o', linewidth=2.5, markersize=8, color=line_color)
            ax.fill_between(range(len(weeks)), coins, alpha=0.2, color=line_color)
            ax.set_title(f'{student.name} - 小码币变化趋势', fontsize=11, fontweight='bold')
            ax.set_ylabel('小码币数量', fontsize=9)
            ax.grid(True, alpha=0.3)
            ax.set_ylim(bottom=0)
            
            # 在每个点上显示数值 / Show values on each point
            for i, coin in enumerate(coins):
                ax.text(i, coin, str(coin), ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # 如果学生数量是奇数，隐藏最后一个空位 / If odd number of students, hide last empty subplot
        if num_students % 2 == 1:
            last_ax = fig_line.add_subplot(line_gs[line_chart_rows - 1, 1])
            last_ax.axis('off')
        
        fig_line.suptitle(f'学生小码币变化趋势 (共{num_students}个学生)', 
                         fontsize=14, fontweight='bold')
        
        # 将折线图嵌入到滚动区域 / Embed line chart in scrollable area
        line_canvas_widget = FigureCanvasTkAgg(fig_line, scrollable_line_frame)
        line_canvas_widget.draw()
        line_canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # ============ 下方区域：柱状图（固定较小高度）/ Bottom region: Bar chart (fixed smaller height) ============
        bar_frame = ttk.LabelFrame(main_frame, text="班级总小码币统计", padding=10)
        bar_frame.pack(fill=tk.X, padx=5, pady=5)  # 不使用expand，让柱状图区域更小
        
        # 创建柱状图Figure，高度更小且自适应屏幕 / Create bar chart figure with smaller adaptive height
        bar_chart_height = max(3.0, (window_height * 0.25) / dpi)  # 柱状图区域占25%，更小 / Bar chart area takes 25%, smaller
        fig_bar = plt.figure(figsize=(available_width_inches, bar_chart_height))
        
        ax_bar = fig_bar.add_subplot(111)
        
        # 准备数据 / Prepare bar chart data
        colors_bar = ['#2E7D32', '#388E3C', '#43A047', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', 
                      '#1565C0', '#1976D2', '#1E88E5', '#2196F3', '#42A5F5', '#64B5F6',
                      '#D32F2F', '#E53935', '#F44336', '#EF5350', '#E57373', '#EF9A9A',
                      '#F57C00', '#FB8C00', '#FF6F00', '#FFA726', '#FFB74D', '#FFCC80']
        bar_colors = [colors_bar[i % len(colors_bar)] for i in range(len(student_names))]
        
        bars = ax_bar.bar(student_names, total_coins, color=bar_colors, edgecolor='black', linewidth=1.5)
        ax_bar.set_title(f'{classroom.name} - 各学生总小码币统计', fontsize=12, fontweight='bold', pad=15)
        ax_bar.set_ylabel('总小码币数量', fontsize=10)
        ax_bar.set_xlabel('学生名字', fontsize=10)
        ax_bar.grid(True, alpha=0.3, axis='y')
        
        # 在柱子上显示数值 / Show values on bars
        for bar in bars:
            height = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # x轴标签正常显示（不旋转）/ x-axis labels displayed normally (no rotation)
        ax_bar.tick_params(axis='x', rotation=0, labelsize=9)
        
        # 调整布局，确保标签不被截断 / Adjust layout to prevent label cutoff
        fig_bar.tight_layout(rect=[0, 0.03, 1, 0.97])
        
        # 将柱状图嵌入到固定区域 / Embed bar chart in fixed area
        bar_canvas_widget = FigureCanvasTkAgg(fig_bar, bar_frame)
        bar_canvas_widget.draw()
        bar_canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加关闭按钮 / Add close button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)
        close_button = ttk.Button(button_frame, text="关闭", command=chart_window.destroy)
        close_button.pack()

    def reset(self) -> None:
        """重置班级详情视图 / Reset class detail view"""
        self.selected_student = None
        self.coins_var.set("0")
        self.student_display.config(text="无")
