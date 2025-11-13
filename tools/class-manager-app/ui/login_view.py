"""
登录界面 / Login view for the classroom manager
"""

import tkinter as tk
from tkinter import ttk, messagebox


class LoginView(ttk.Frame):
    """登录视图框架 / Login view frame"""

    def __init__(self, parent, controller, **kwargs):
        """
        初始化登录视图
        / Initialize the login view
        
        Args:
            parent: 父级窗口 / Parent window
            controller: 应用控制器 / Application controller
        """
        super().__init__(parent, **kwargs)
        self.controller = controller

        # 设置样式 / Set style
        self.configure(padding="20")

        # 标题 - 西瓜老师 / Title - XiguaTeacher
        title_label = ttk.Label(
            self, text="西瓜老师", font=("Arial", 32, "bold"), foreground="#4CAF50"
        )
        title_label.pack(pady=(20, 40))

        # 账号输入框 / Username input
        username_frame = ttk.Frame(self)
        username_frame.pack(fill=tk.X, pady=15)

        username_label = ttk.Label(username_frame, text="账号", font=("Arial", 11))
        username_label.pack(side=tk.LEFT, padx=(0, 15))

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var, width=30)
        self.username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.username_entry.focus()

        # 密码输入框 / Password input
        password_frame = ttk.Frame(self)
        password_frame.pack(fill=tk.X, pady=15)

        password_label = ttk.Label(password_frame, text="密码", font=("Arial", 11))
        password_label.pack(side=tk.LEFT, padx=(0, 15))

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame, textvariable=self.password_var, show="*", width=30
        )
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 绑定回车键 / Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())

        # 登录按钮 / Login button - 居中显示
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=30)

        login_button = ttk.Button(button_frame, text="登录", command=self.login, width=15)
        login_button.pack(side=tk.LEFT, padx=5)

        # 底部说明 / Footer text
        info_label = ttk.Label(
            self,
            text="演示账号：xigua / 123456",
            foreground="gray",
            font=("Arial", 10),
        )
        info_label.pack(pady=(30, 0))

    def login(self) -> None:
        """
        验证凭证并导航到主视图
        / Validate credentials and navigate to main view
        """
        username = self.username_var.get().strip()
        password = self.password_var.get()

        # 验证凭证 / Validate credentials
        if username == "xigua" and password == "123456":
            self.controller.show_frame("MainView")
        else:
            messagebox.showerror(
                "登录失败", "用户名或密码错误，请重试。\n正确的账号为 xigua / 123456"
            )
            self.username_var.set("")
            self.password_var.set("")
            self.username_entry.focus()

    def reset(self) -> None:
        """重置登录表单 / Reset login form"""
        self.username_var.set("")
        self.password_var.set("")
        self.username_entry.focus()
