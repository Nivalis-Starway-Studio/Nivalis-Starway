"""
课堂管理系统 - 主应用入口
Classroom Manager Application - Main Entry Point
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
    / Main application class - Controller and root window
    """

    def __init__(self):
        """初始化应用 / Initialize the application"""
        super().__init__()

        # 设置窗口属性 / Set window properties
        self.title("课堂管理系统")
        
        # 设置全屏显示 / Set fullscreen display
        self.state('zoomed')  # Windows全屏
        # 对于Linux/Mac，可以使用：
        # self.attributes('-zoomed', True)
        
        # 备用尺寸设置 / Backup size settings
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # 初始化数据存储 / Initialize data store
        self.data_store = ClassDataStore()

        # 当前班级追踪 / Track current classroom
        self.current_classroom_id = None

        # 配置样式 / Configure style
        self.setup_style()

        # 创建容器 / Create container
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # 实例化所有视图 / Instantiate all views
        for F in (LoginView, MainView, ClassDetailView):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 显示登录视图 / Show login view
        self.show_frame("LoginView")

    def setup_style(self) -> None:
        """
        配置应用样式
        / Configure application styling
        """
        style = ttk.Style()
        style.theme_use("clam")

        # 配置颜色 - 修复黑色背景问题 / Configure colors - fix black background issue
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TButton", padding=5)
        style.configure("TFrame", background="white")
        style.configure(
            "TLabelFrame",
            background="white",
            foreground="black",
            padding=10,
        )
        
        # 设置主窗口背景色 / Set main window background
        self.configure(bg="white")

    def show_frame(self, name: str) -> None:
        """
        显示指定的视图框架
        / Show the specified frame
        
        Args:
            name: 框架名称 / Frame name
        """
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

            # 如果是班级详情视图，加载数据 / If ClassDetailView, load data
            if name == "ClassDetailView" and self.current_classroom_id:
                frame.load_classroom_data(self.current_classroom_id)

            # 重置视图 / Reset view if it has reset method
            if hasattr(frame, "reset"):
                frame.reset()

    def set_current_classroom(self, class_id: str) -> None:
        """
        设置当前班级
        / Set current classroom
        
        Args:
            class_id: 班级ID / Classroom ID
        """
        self.current_classroom_id = class_id

    def get_current_classroom(self) -> str:
        """
        获取当前班级ID
        / Get current classroom ID
        
        Returns:
            当前班级ID / Current classroom ID
        """
        return self.current_classroom_id


def main():
    """应用入口点 / Application entry point"""
    app = ClassManagerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
