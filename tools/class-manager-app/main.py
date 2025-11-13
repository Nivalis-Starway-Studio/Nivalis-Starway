"""
课堂管理系统 - 主应用入口
"""

import tkinter as tk
from tkinter import ttk
from data.store import ClassDataStore
from ui.login_view import LoginView
from ui.main_view import MainView
from ui.class_detail_view import ClassDetailView


class ClassManagerApp(tk.Tk):
    """
    主应用类 - 控制器和根窗口
    """

    def __init__(self):
        """初始化应用"""
        super().__init__()

        # 设置窗口属性
        self.title("课堂管理系统")
        self.geometry("900x700")
        self.minsize(800, 600)

        # 初始化数据存储
        self.data_store = ClassDataStore()

        # 当前班级追踪
        self.current_classroom_id = None

        # 配置样式
        self.setup_style()

        # 创建容器
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # 实例化所有视图
        for F in (LoginView, MainView, ClassDetailView):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 显示登录视图
        self.show_frame("LoginView")

    def setup_style(self) -> None:
        """配置应用样式"""
        style = ttk.Style()
        style.theme_use("clam")

        # 配置颜色
        style.configure("TLabel", background="", foreground="black")
        style.configure("TButton", padding=5)
        style.configure("TFrame", background="")
        style.configure(
            "TLabelFrame",
            background="",
            foreground="black",
            padding=10,
        )

    def show_frame(self, name: str) -> None:
        """
        显示指定的视图框架
        
        Args:
            name: 框架名称
        """
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

            # 如果是班级详情视图，加载数据
            if name == "ClassDetailView" and self.current_classroom_id:
                frame.load_classroom_data(self.current_classroom_id)

            # 重置视图
            if hasattr(frame, "reset"):
                frame.reset()

    def set_current_classroom(self, class_id: str) -> None:
        """
        设置当前班级
        
        Args:
            class_id: 班级ID
        """
        self.current_classroom_id = class_id

    def get_current_classroom(self) -> str:
        """
        获取当前班级ID
        
        Returns:
            当前班级ID
        """
        return self.current_classroom_id


def main():
    """应用入口点"""
    app = ClassManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
