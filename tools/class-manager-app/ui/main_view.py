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
        self.configure(padding="20", background="white")
        self.frames_dict = {}

        # 标题 / Title
        title_label = ttk.Label(
            self, text="课堂管理系统 - 班级选择", font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # 说明文本 / Description
        description_label = ttk.Label(self, text="请选择要管理的班级：")
        description_label.pack(fill=tk.X, pady=(0, 15))

        # 班级管理按钮 / Classroom management buttons
        management_frame = ttk.Frame(self)
        management_frame.pack(fill=tk.X, pady=(0, 10))

        add_class_button = ttk.Button(
            management_frame, text="添加班级", command=self.add_classroom
        )
        add_class_button.pack(side=tk.LEFT, padx=5)

        edit_class_button = ttk.Button(
            management_frame, text="修改班级", command=self.edit_classroom
        )
        edit_class_button.pack(side=tk.LEFT, padx=5)

        delete_class_button = ttk.Button(
            management_frame, text="删除班级", command=self.delete_classroom
        )
        delete_class_button.pack(side=tk.LEFT, padx=5)

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
            
            # 绑定右键菜单 / Bind right-click menu
            button.bind("<Button-3>", lambda e, cid=classroom.class_id: self.show_context_menu(e, cid))
            
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

        # 全屏切换 / Toggle fullscreen
        fullscreen_button = ttk.Button(
            button_frame, text="切换全屏", command=self.toggle_fullscreen
        )
        fullscreen_button.pack(side=tk.LEFT, padx=5)

    def show_context_menu(self, event, class_id: str) -> None:
        """
        显示班级右键菜单 / Show classroom context menu
        """
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="修改班级名字", command=lambda: self.edit_classroom_by_id(class_id))
        context_menu.add_command(label="删除班级", command=lambda: self.delete_classroom_by_id(class_id))
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def edit_classroom_by_id(self, class_id: str) -> None:
        """
        根据ID修改班级名字 / Edit classroom name by ID
        """
        self.selected_class_var.set(class_id)
        classroom = self.controller.data_store.get_classroom(class_id)
        self.selection_display.config(
            text=f"已选择: {classroom.name} ({len(classroom.students)}名学生)"
        )
        self.edit_classroom()

    def delete_classroom_by_id(self, class_id: str) -> None:
        """
        根据ID删除班级 / Delete classroom by ID
        """
        self.selected_class_var.set(class_id)
        classroom = self.controller.data_store.get_classroom(class_id)
        self.selection_display.config(
            text=f"已选择: {classroom.name} ({len(classroom.students)}名学生)"
        )
        self.delete_classroom()

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

    def toggle_fullscreen(self) -> None:
        """
        切换全屏模式 / Toggle fullscreen mode
        """
        current_state = self.controller.state()
        if current_state == 'zoomed':
            self.controller.state('normal')
        else:
            self.controller.state('zoomed')

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
        self.refresh_classrooms()

    def refresh_classrooms(self) -> None:
        """
        刷新班级按钮显示 / Refresh classroom buttons display
        """
        for item in self.frames_dict.values():
            item.destroy()
        
        self.frames_dict = {}
        selection_frame = self.winfo_children()[2]
        for widget in selection_frame.winfo_children():
            widget.destroy()
        
        selection_frame.rowconfigure(0, weight=1)
        selection_frame.columnconfigure(0, weight=1)
        
        button_row = 0
        button_col = 0
        max_cols = 3

        classrooms = self.controller.data_store.get_all_classrooms()
        self.class_buttons = {}
        for classroom in classrooms:
            button = ttk.Button(
                selection_frame,
                text=f"{classroom.name}\n({len(classroom.students)}名学生)",
                command=lambda class_id=classroom.class_id: self.on_class_selected(
                    class_id
                ),
                width=20,
            )
            button.grid(row=button_row, column=button_col, padx=5, pady=5, sticky="nsew")
            
            # 绑定右键菜单 / Bind right-click menu
            button.bind("<Button-3>", lambda e, cid=classroom.class_id: self.show_context_menu(e, cid))
            
            self.class_buttons[classroom.class_id] = button

            button_col += 1
            if button_col >= max_cols:
                button_col = 0
                button_row += 1

        for i in range(button_row + 1):
            selection_frame.rowconfigure(i, weight=1)
        for j in range(max_cols):
            selection_frame.columnconfigure(j, weight=1)

    def add_classroom(self) -> None:
        """
        添加新班级 / Add a new classroom
        """
        dialog = tk.Toplevel(self)
        dialog.title("添加班级")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(dialog, text="班级名字：").pack(pady=(10, 0), padx=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5, padx=10, fill=tk.X)
        name_entry.focus()

        def confirm():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("输入错误", "班级名字不能为空。")
                return
            
            self.controller.data_store.add_classroom(name)
            dialog.destroy()
            self.refresh_classrooms()
            messagebox.showinfo("成功", f"班级 {name} 已添加。")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="确定", command=confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def edit_classroom(self) -> None:
        """
        修改班级名字 / Edit classroom name
        """
        class_id = self.selected_class_var.get()
        if not class_id:
            messagebox.showwarning("未选择班级", "请先选择一个班级。")
            return

        classroom = self.controller.data_store.get_classroom(class_id)
        
        dialog = tk.Toplevel(self)
        dialog.title("修改班级")
        dialog.geometry("300x150")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ttk.Label(dialog, text="班级名字：").pack(pady=(10, 0), padx=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, classroom.name)
        name_entry.pack(pady=5, padx=10, fill=tk.X)
        name_entry.focus()

        def confirm():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showwarning("输入错误", "班级名字不能为空。")
                return
            
            self.controller.data_store.update_classroom_name(class_id, new_name)
            dialog.destroy()
            self.refresh_classrooms()
            messagebox.showinfo("成功", f"班级已改名为 {new_name}。")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="确定", command=confirm).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_classroom(self) -> None:
        """
        删除班级 / Delete a classroom
        """
        class_id = self.selected_class_var.get()
        if not class_id:
            messagebox.showwarning("未选择班级", "请先选择一个班级。")
            return

        classroom = self.controller.data_store.get_classroom(class_id)
        
        if messagebox.askyesno(
            "确认删除",
            f"确定要删除班级 {classroom.name} 吗？\n此操作不可撤销。",
        ):
            self.controller.data_store.remove_classroom(class_id)
            self.selected_class_var.set("")
            self.selection_display.config(text="未选择班级")
            self.refresh_classrooms()
            messagebox.showinfo("成功", f"班级 {classroom.name} 已删除。")
