"""
登录界面 / Login view for the classroom manager
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Canvas


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

        # 设置样式 / Set style (ttk.Frame不支持background参数)
        self.configure(padding="20")

        # 创建主容器用于垂直居中 / Create main container for vertical centering
        main_container = ttk.Frame(self)
        main_container.place(relx=0.5, rely=0.5, anchor="center")

        # 创建渐变色标题 - 西瓜老师 / Create gradient title - XiguaTeacher
        self.title_canvas = Canvas(main_container, width=400, height=100, bg="white", highlightthickness=0)
        self.title_canvas.pack(pady=(0, 50))
        
        # 绘制渐变色文字（居中） / Draw gradient text (centered)
        self._gradient_colors = ["#2E7D32", "#388E3C", "#43A047", "#4CAF50", "#66BB6A", "#81C784"]
        text = "西瓜老师"
        font_size = 36
        self._title_items = []
        
        # 计算文字总宽度以实现居中 / Calculate total text width for centering
        total_width = len(text) * 55
        start_x = (400 - total_width) / 2 + 27.5
        
        for i, char in enumerate(text):
            x = start_x + i * 55
            y = 50
            color = self._gradient_colors[i % len(self._gradient_colors)]
            item = self.title_canvas.create_text(
                x,
                y,
                text=char,
                font=("Arial", font_size, "bold"),
                fill=color,
                anchor="center",
            )
            self._title_items.append(item)
        
        # 启动标题渐变动画 / Start title gradient animation
        self.after(120, self._animate_title_gradient)

        # 账号密码输入容器（居中对齐）/ Username and password input container (centered)
        input_container = ttk.Frame(main_container)
        input_container.pack(pady=20)

        # 账号输入框 / Username input
        username_label = ttk.Label(input_container, text="账号", font=("Arial", 11))
        username_label.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="e")

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(input_container, textvariable=self.username_var, width=20)
        self.username_entry.grid(row=0, column=1, pady=10)
        self.username_entry.focus()

        # 密码输入框 / Password input
        password_label = ttk.Label(input_container, text="密码", font=("Arial", 11))
        password_label.grid(row=1, column=0, padx=(0, 15), pady=10, sticky="e")

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            input_container, textvariable=self.password_var, show="*", width=20
        )
        self.password_entry.grid(row=1, column=1, pady=10)

        # 输入内容仅允许英文字符 / Restrict input to ASCII characters
        vcmd = (self.register(self._validate_ascii), "%P")
        self.username_entry.configure(validate="key", validatecommand=vcmd)
        self.password_entry.configure(validate="key", validatecommand=vcmd)

        # 绑定回车键 / Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self.login())

        # 登录按钮（居中显示）/ Login button (centered)
        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=30)

        login_button = ttk.Button(button_frame, text="登录", command=self.login, width=15)
        login_button.pack()

    def _validate_ascii(self, text: str) -> bool:
        """验证输入只包含ASCII字符 / Validate input contains only ASCII characters"""
        if not text:
            return True
        return all(ord(char) < 128 for char in text)

    def _animate_title_gradient(self) -> None:
        """标题渐变动画 / Animate title gradient"""
        if not self.winfo_exists():
            return
        
        # 旋转颜色数组 / Rotate color array
        self._gradient_colors = self._gradient_colors[1:] + [self._gradient_colors[0]]
        
        # 更新每个字符的颜色 / Update each character's color
        for i, item in enumerate(self._title_items):
            color = self._gradient_colors[i % len(self._gradient_colors)]
            self.title_canvas.itemconfig(item, fill=color)
        
        # 继续动画 / Continue animation
        self.after(300, self._animate_title_gradient)

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
                "登录失败", "用户名或密码错误，请重试。"
            )
            self.username_var.set("")
            self.password_var.set("")
            self.username_entry.focus()

    def reset(self) -> None:
        """重置登录表单 / Reset login form"""
        self.username_var.set("")
        self.password_var.set("")
        self.username_entry.focus()
