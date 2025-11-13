"""
主视图 / Main hub view for classroom selection
"""

import tkinter as tk
from tkinter import ttk, messagebox


class MainView(ttk.Frame):
    """主视图框架 / Main view frame for displaying all classrooms"""

    def __init__(self, parent, controller, **kwargs):
        """
        初始化主视图
        / Initialize the main view
        
        Args:
            parent: 父级窗口 / Parent window
            controller: 应用控制器 / Application controller
        """
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)
        self.configure(padding="20")

        # 标题 / Title
        title_label = ttk.Label(
            self, text="课堂管理系统 - 班级选择", font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # 说明文本 / Description
        description_label = ttk.Label(self, text="请选择要管理的班级：")
        description_label.pack(fill=tk.X, pady=(0, 15))

        # 班级选择区域 / Classroom selection area
        selection_frame = ttk.Frame(self)
        selection_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.selected_class_var = tk.StringVar()

        # 创建班级按钮 / Create classroom buttons
        self.class_buttons = {}
        button_row = 0
        button_col = 0
        max_cols = 3

        classrooms = self.controller.data_store.get_all_classrooms()
        for classroom in classrooms:
            # 创建按钮 / Create button for each classroom
            button = ttk.Button(
                selection_frame,
                text=f"{classroom.name}\n({len(classroom.students)}名学生)",
                command=lambda class_id=classroom.class_id: self.on_class_selected(
                    class_id
                ),
                width=20,
            )
            button.grid(row=button_row, column=button_col, padx=5, pady=5, sticky="nsew")
            self.class_buttons[classroom.class_id] = button

            button_col += 1
            if button_col >= max_cols:
                button_col = 0
                button_row += 1

        # 配置网格权重 / Configure grid weights
        for i in range(button_row + 1):
            selection_frame.rowconfigure(i, weight=1)
        for j in range(max_cols):
            selection_frame.columnconfigure(j, weight=1)

        # 底部控制区域 / Bottom control area
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, pady=(20, 0))

        # 当前选择显示 / Current selection display
        self.selection_display = ttk.Label(
            control_frame, text="未选择班级", foreground="blue", font=("Arial", 12)
        )
        self.selection_display.pack(side=tk.LEFT, expand=True)

        # 按钮容器 / Button container
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)

        # 进入班级详情 / Enter class detail
        detail_button = ttk.Button(
            button_frame, text="进入班级", command=self.enter_class_detail
        )
        detail_button.pack(side=tk.LEFT, padx=5)

        # 退出登录 / Logout
        logout_button = ttk.Button(
            button_frame, text="退出登录", command=self.logout
        )
        logout_button.pack(side=tk.LEFT, padx=5)

    def on_class_selected(self, class_id: str) -> None:
        """
        处理班级选择
        / Handle classroom selection
        
        Args:
            class_id: 班级ID / Classroom ID
        """
        self.selected_class_var.set(class_id)
        classroom = self.controller.data_store.get_classroom(class_id)
        self.selection_display.config(
            text=f"已选择: {classroom.name} ({len(classroom.students)}名学生)"
        )
        messagebox.showinfo(
            "班级已选择", f"已选择班级: {classroom.name}\n\n点击'进入班级'按钮查看详情。"
        )

    def enter_class_detail(self) -> None:
        """
        进入班级详情视图
        / Enter the class detail view
        """
        class_id = self.selected_class_var.get()
        if not class_id:
            messagebox.showwarning("未选择班级", "请先选择一个班级。")
            return

        self.controller.set_current_classroom(class_id)
        self.controller.show_frame("ClassDetailView")

    def logout(self) -> None:
        """
        退出登录，返回登录视图
        / Logout and return to login view
        """
        self.selected_class_var.set("")
        self.selection_display.config(text="未选择班级")
        self.controller.show_frame("LoginView")

    def reset(self) -> None:
        """重置主视图 / Reset main view"""
        self.selected_class_var.set("")
        self.selection_display.config(text="未选择班级")
