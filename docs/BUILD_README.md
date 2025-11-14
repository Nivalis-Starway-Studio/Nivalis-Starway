# 班级管理系统 - 打包和发布指南
# Classroom Manager Application - Build and Release Guide

## 中文说明

### 项目概述
这是一个使用Tkinter开发的班级管理系统，支持：
- 班级和学生管理
- 小码币积分系统
- 数据统计和可视化
- 3周历史数据追踪
- Excel导出功能

### 系统要求
- Python 3.8+
- tkinter (通常随Python自动安装)
- 依赖库：openpyxl, matplotlib

### 打包为可执行文件

#### 在Linux/macOS上打包
```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install pyinstaller openpyxl matplotlib

# 3. 运行打包脚本
python3 build_exe.py

# 4. 生成的文件位置
# dist/ClassManagerApp - Linux可执行文件
```

#### 在Windows上打包
```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install pyinstaller openpyxl matplotlib

# 3. 运行打包脚本
python build_exe.py

# 4. 生成的文件位置
# dist\ClassManagerApp.exe - Windows可执行文件
```

### 运行应用

#### 直接运行源代码
```bash
# 进入项目目录
cd /home/engine/project

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行应用
python tools/class-manager-app/main.py
```

#### 运行打包后的可执行文件
```bash
# Linux
./dist/ClassManagerApp

# macOS
./dist/ClassManagerApp

# Windows
dist\ClassManagerApp.exe
```

### 登录凭证
- **账号**: xigua
- **密码**: 123456

### 功能说明

#### 1. 登录界面
- 动态渐变色"西瓜老师"标题
- 账号和密码输入（仅支持ASCII字符）
- 300x300的圆角图片位置预留（代码已标记位置）

#### 2. 班级管理
- 查看所有班级
- 单击进入班级详情
- 右键菜单：修改班级名字、删除班级、导出Excel

#### 3. 学生管理
- 添加、修改、删除学生
- 右键选中学生并进行操作
- 自动保存数据

#### 4. 小码币管理
- 显示三周历史数据（上上周、上周、本周）
- 总小码币累计
- 双击修改单元格中的数值
- 支持全班和单个学生更新

#### 5. 数据统计
- 每个学生的折线图（显示三周变化）
- 班级总小码币柱状图（按学生统计）
- 中文支持的图表

#### 6. 数据导出
- 导出班级学生数据到Excel
- 包含学生名字和总小码币

#### 7. 数据持久化
- 自动保存到CSV文件
- 位置：`tools/class-manager-app/storage_data/`
- 包含：班级、学生、周历史记录

### 项目结构
```
tools/class-manager-app/
├── main.py                      # 主应用入口
├── ui/
│   ├── login_view.py           # 登录界面
│   ├── main_view.py            # 班级管理界面
│   └── class_detail_view.py    # 班级详情界面
├── data/
│   ├── models.py               # 数据模型
│   ├── store.py                # 数据存储
│   └── excel_storage.py        # CSV持久化
└── storage_data/               # 数据存储目录（自动创建）
    ├── classrooms.csv
    ├── students.csv
    └── weekly_history.csv
```

### UI优化说明

#### 登录界面优化
- ✓ 账号和密码文字提示及输入框居中
- ✓ 西瓜老师标题下方预留300x300圆角图片位置
- ✓ 代码已注释并标记位置，可直接替换

#### 班级详情页面优化
- ✓ 增加行高到40px，适配两行标题
- ✓ 调整列宽，确保日期显示完整
- ✓ 学生名字：120px
- ✓ 周数据列：180px（用于显示"上上周\n月/日-月/日"格式）
- ✓ 总小码币：140px
- ✓ 右键任何列都可以选中学生并进行操作

#### 图表统计优化
- ✓ 支持最多3个学生的折线图
- ✓ 折线图显示上上周、上周、本周的数据
- ✓ 折线图左边显示学生名字
- ✓ 底部柱状图显示班级所有学生的总小码币
- ✓ 中文字体支持

### 依赖库安装

如果直接安装而不使用虚拟环境，可能需要提升权限：
```bash
pip install pyinstaller openpyxl matplotlib tkinter --break-system-packages
```

### 故障排除

**问题**: "No module named 'tkinter'"
**解决**:
- Linux: `sudo apt-get install python3-tk`
- macOS: `brew install python-tk`
- Windows: 重新安装Python，勾选"tcl/tk and IDLE"

**问题**: 导入错误
**解决**: 确保虚拟环境已激活，且依赖已安装

**问题**: 无法生成.exe文件
**解决**: 在Windows上运行build_exe.py脚本

### 开发建议

#### 修改后重新打包
```bash
# 1. 修改源代码
# 2. 清理旧的构建文件
rm -rf dist build

# 3. 重新运行打包脚本
python build_exe.py
```

#### 自定义打包选项
在`build_exe.py`中修改PyInstaller命令参数：
- `--onefile`: 生成单一可执行文件（推荐）
- `--windowed`: 隐藏控制台窗口
- `--icon`: 添加应用图标
- `--add-data`: 添加数据文件

### 许可证
本项目为教学用途

### 联系方式
如有问题，请提交issue或反馈

---

## English Guide

### Project Overview
A classroom management system built with Tkinter, featuring:
- Class and student management
- Xiaoma coin reward system
- Data statistics and visualization
- 3-week historical data tracking
- Excel export functionality

### System Requirements
- Python 3.8+
- tkinter (usually installed with Python)
- Dependencies: openpyxl, matplotlib

### Building Executable Files

#### On Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller openpyxl matplotlib
python3 build_exe.py
# Output: dist/ClassManagerApp
```

#### On Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install pyinstaller openpyxl matplotlib
python build_exe.py
# Output: dist\ClassManagerApp.exe
```

### Running the Application

#### From source
```bash
python tools/class-manager-app/main.py
```

#### From executable
```bash
# Linux/macOS
./dist/ClassManagerApp

# Windows
dist\ClassManagerApp.exe
```

### Login Credentials
- **Username**: xigua
- **Password**: 123456

### Build Notes
- First time build may take 2-3 minutes
- Output file size is approximately 11-12 MB
- Uses PyInstaller with --onefile option for single executable
