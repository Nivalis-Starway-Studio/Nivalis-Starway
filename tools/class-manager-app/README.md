# 课堂管理系统 / Classroom Manager Application

## 功能特性 / Features

### 1. 数据持久化 / Data Persistence
- 所有数据自动保存到Excel文件（`classroom_data.xlsx`）
- 每个班级对应一个工作表（worksheet）
- 支持多周的周币记录（最多52周）
- 累计币自动计算和保存

### 2. 周数管理 / Week Management
- 第一周开始日期：**2025年11月13日**
- 自动计算当前是第几周
- 界面显示当前周数提示

### 3. 多周币数显示 / Multi-Week Coins Display
- 同时显示4周的周币数据
- 显示范围：当前周及前3周（如果当前周<4，则显示第1-4周）
- 当前周在表头中标记为"(当前)"

### 4. 直接编辑周币 / Direct Week Coins Editing
- 双击任意周币单元格即可编辑
- 修改后累计币**自动更新**
- 无需点击"重置"按钮
- 支持回车键确认、ESC键取消

### 5. 实时统计 / Real-time Statistics
- 显示各周的总币数
- 显示累计总币
- 自动刷新统计信息

## 使用说明 / Usage

### 启动应用 / Launch Application
```bash
cd /home/engine/project/tools/class-manager-app
python3 main.py
```

### 登录 / Login
- 用户名：`xigua`
- 密码：`123456`

### 编辑周币 / Edit Week Coins
1. 选择班级进入详情页
2. 双击任意学生的周币单元格
3. 在弹出的对话框中输入新的币数
4. 点击"确认"或按回车键
5. 累计币会自动更新

### 查看统计 / View Statistics
- 统计栏显示各周总币数和累计总币
- 数据实时更新

## 数据结构 / Data Structure

### Student 模型
```python
@dataclass
class Student:
    name: str                           # 学生名字
    cumulative_coins: int = 0           # 累计币（总和）
    week_coins: Dict[int, int] = {}     # 周币记录 {周数: 币数}
```

### Excel 文件结构
```
| 学生名字 | 累计币 | 第1周 | 第2周 | 第3周 | ... | 第52周 |
|---------|-------|------|------|------|-----|--------|
| 张三     | 57    | 5    | 3    | 7    | ... | 0      |
| 李四     | 45    | 2    | 4    | 0    | ... | 0      |
```

## 自动功能 / Automatic Features

### 累计币自动更新 / Auto-Update Cumulative Coins
当修改任意周的币数时：
1. 计算新旧币数的差值
2. 自动调整累计币（累计币 += 差值）
3. 保存到Excel文件

例如：
- 原第3周币数：5
- 修改为：7
- 差值：+2
- 累计币自动增加2

### 数据自动保存 / Auto-Save
每次修改周币后，数据自动保存到Excel文件，无需手动保存。

## 技术实现 / Technical Implementation

### 依赖库 / Dependencies
- `tkinter` - GUI界面
- `openpyxl` - Excel文件读写
- `datetime` - 日期时间计算

### 核心模块 / Core Modules
- `data/models.py` - 数据模型
- `data/store.py` - 数据存储和业务逻辑
- `data/excel_store.py` - Excel文件操作
- `utils/week_utils.py` - 周数计算工具
- `ui/class_detail_view.py` - 班级详情视图

## 注意事项 / Notes

1. **Excel文件位置**：应用目录下的 `classroom_data.xlsx`
2. **首次运行**：如果没有Excel文件，会自动创建并加载示例数据
3. **数据备份**：建议定期备份 `classroom_data.xlsx` 文件
4. **周数限制**：Excel支持最多52周的数据记录
5. **币数验证**：币数必须为非负整数

## 更新日志 / Changelog

### v2.0 (2024)
- ✨ 新增：Excel数据持久化
- ✨ 新增：多周币数显示（4周）
- ✨ 新增：双击单元格编辑功能
- ✨ 新增：周数自动计算（基于2025-11-13）
- ✨ 新增：累计币自动更新
- 🗑️ 移除：手动重置周币按钮（不再需要）

### v1.0 (2024)
- ✅ 基础登录系统
- ✅ 班级和学生管理
- ✅ 简单的周币和累计币管理
