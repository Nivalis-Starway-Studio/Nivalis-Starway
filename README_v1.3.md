# 班级管理系统 v1.3 - 优化版本

## 新增优化功能 (New Features v1.3)

### 1. 登录界面优化 (Login Interface Optimization)
- ✅ **账号密码居中**: 使用grid布局实现完美居中对齐
- ✅ **300x300图片位置预留**: 在标题下方预留圆角图片位置，带详细注释说明
- ✅ **动态标题动画**: 保持"西瓜老师"渐变色动画效果

### 2. 班级详情页面优化 (Class Detail View Optimization)
- ✅ **标题行高度修复**: 增加Treeview.Heading的padding，确保日期显示完整
- ✅ **列宽优化**: 
  - 学生名字: 120px
  - 周数据列: 180px (完整显示"上上周\n月/日-月/日"格式)
  - 总小码币: 140px
- ✅ **样式配置**: 使用ttk.Style配置行高和标题样式，确保兼容性

### 3. 图表统计功能 (Chart Statistics)
- ✅ **动态折线图**: 自动显示班级前3名学生的三周趋势
- ✅ **柱状图统计**: 显示所有学生的总小码币
- ✅ **数据标签**: 折线图和柱状图都显示具体数值
- ✅ **中文支持**: 完整支持中文字体显示

### 4. 班级管理功能 (Classroom Management)
- ✅ **新增班级按钮**: 恢复右下角"新增班级"按钮
- ✅ **班级操作**: 支持新增、修改、删除班级
- ✅ **Excel导出**: 一键导出班级数据到Excel文件

## 打包说明 (Packaging Instructions)

### Windows系统打包 (Windows Packaging)
1. **自动打包** (推荐):
   ```cmd
   build_windows.bat
   ```
   这个脚本会：
   - 自动创建虚拟环境
   - 安装所需依赖
   - 打包生成 ClassManagerApp.exe

2. **手动打包**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install PyInstaller matplotlib openpyxl pillow
   python build_exe.py
   ```

### Linux/macOS系统打包 (Linux/macOS Packaging)
```bash
python3 -m venv venv
source venv/bin/activate
pip install PyInstaller matplotlib openpyxl pillow
python build_exe.py
```

## 输出文件 (Output Files)
- **Windows**: `dist/ClassManagerApp.exe` (可直接双击运行)
- **Linux/macOS**: `dist/ClassManagerApp` (可执行文件)

## 登录信息 (Login Information)
- **账号**: xigua
- **密码**: 123456

## 使用说明 (Usage Instructions)

### 登录界面 (Login Screen)
1. 输入账号: xigua
2. 输入密码: 123456
3. 点击"登录"按钮

### 班级管理 (Classroom Management)
1. **新增班级**: 点击"新增班级"按钮
2. **选择班级**: 单击班级按钮进入详情
3. **班级操作**: 右键班级按钮可修改、删除或导出Excel

### 学生管理 (Student Management)
1. **添加学生**: 在班级详情页面点击"添加学生"
2. **修改信息**: 右键学生姓名可修改或删除
3. **币数管理**: 双击币数单元格可修改数值
4. **图表统计**: 点击"图表统计"查看可视化数据

### 数据持久化 (Data Persistence)
- 所有数据自动保存到 `storage_data/` 文件夹
- 支持CSV格式导入导出
- 数据包含学生信息、币数记录、周历史

## 技术特性 (Technical Features)
- **跨平台**: 支持Windows、Linux、macOS
- **单文件打包**: 生成独立可执行文件，无需安装Python
- **现代化UI**: 使用tkinter + ttk实现美观界面
- **数据可视化**: matplotlib集成，支持图表统计
- **Excel集成**: openpyxl支持，数据导出功能

## 故障排除 (Troubleshooting)

### 打包问题 (Build Issues)
- 确保安装了所有依赖: `pip install PyInstaller matplotlib openpyxl pillow`
- Windows用户建议使用 `build_windows.bat` 脚本
- 如果遇到tkinter错误，可能需要安装系统级的tkinter包

### 运行问题 (Runtime Issues)
- 确保有足够的磁盘空间存储数据文件
- 图表功能需要matplotlib支持
- Excel导出需要openpyxl库

## 版本历史 (Version History)
- **v1.0**: 基础功能实现
- **v1.1**: 登录界面优化、图表统计、Excel导出
- **v1.2**: 兼容性修复、启动流程优化
- **v1.3**: 界面完善、新增班级按钮、打包优化

## 联系支持 (Support)
如有问题或建议，请通过以下方式联系：
- 技术支持: 查看代码注释和文档
- 功能建议: 提交功能需求