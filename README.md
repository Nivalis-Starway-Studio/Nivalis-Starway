# 班级管理应用 / Classroom Manager App

一个基于 Tkinter 的班级管理应用，用于管理学生小码币系统。

## 🎉 v5.0 最新更新

### 三大核心优化
1. **登录界面优化** - 删除图片占位符，完美居中对齐
2. **全窗口自适应** - 所有窗口和对话框自动适配屏幕分辨率
3. **总小码币修改** - 支持双击直接修改学生总小码币数量

详见 [更新日志](./CHANGELOG.md) 和 [v5.0优化文档](./docs/OPTIMIZATION_v5.0.md)

## 功能特性

- 🎨 **简洁登录界面**（v5.0）：
  - 无冗余图片，界面简洁
  - 标题和表单完美居中对齐
  - 渐变色动画标题

- 🖥️ **全面自适应**（v5.0）：
  - 主窗口自动适配屏幕尺寸（占90%）
  - 所有对话框根据屏幕分辨率动态调整
  - 支持1366x768到4K显示器

- 📚 **班级管理**：创建和管理多个班级
- 👥 **学生管理**：添加、删除、编辑学生信息

- 💰 **小码币系统**：
  - 记录学生每周小码币（上上周、上周、本周）
  - 累计小码币统计
  - **双击修改**：周币和总币都支持双击修改（v5.0）
  - 历史数据追踪

- 📊 **图表统计**（v4.0自适应优化）：
  - 折线图：学生小码币变化趋势（每行2个学生，可滚动）
  - 柱状图：班级总小码币统计
  - **自适应屏幕分辨率**：根据当前屏幕大小自动调整图表尺寸
  - **区域优化**：折线图区域更大（60%），柱状图区域更小（25%）
  - **标签优化**：柱状图x轴人名正常显示（不旋转）

- 💾 **数据持久化**：CSV格式自动保存

## 快速开始

### 环境要求

- Python 3.7+
- tkinter
- matplotlib

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

#### Windows
```bash
scripts\run\run_app.bat
```

#### Linux/Mac
```bash
bash scripts/run/run_app.sh
```

或直接运行：
```bash
python3 tools/class-manager-app/main.py
```

### 默认登录账号

- 账号：`xigua`
- 密码：`123456`

## 打包发布

### 打包为可执行文件

详细打包指南请查看：[docs/BUILD_README.md](docs/BUILD_README.md)

#### Windows打包
```bash
cd scripts\build
build_exe.bat
```

#### 跨平台打包
```bash
cd scripts/build
python build_exe.py
```

打包后的可执行文件在 `dist/` 目录下。

## 项目结构

```
/
├── docs/                       # 文档
│   ├── README.md              # 主文档（符号链接）
│   ├── BUILD_README.md        # 打包指南
│   ├── CHANGELOG.md           # 版本更新日志
│   └── archive/               # 历史文档归档
├── scripts/                   # 脚本
│   ├── build/                # 打包脚本
│   │   ├── build_exe.py
│   │   ├── build_exe.bat
│   │   └── build_windows.bat
│   ├── run/                  # 运行脚本
│   │   ├── run_app.bat
│   │   └── run_app.sh
│   └── test/                 # 测试脚本
├── tools/                     # 应用主代码
│   └── class-manager-app/
│       ├── main.py           # 程序入口
│       ├── data/             # 数据层
│       └── ui/               # UI层
├── requirements.txt           # Python依赖
├── LICENSE                    # 许可证
└── .gitignore                # Git忽略配置
```

## 最新更新 (v4.0)

### 图表统计优化

1. **自适应屏幕分辨率**
   - 自动检测屏幕尺寸
   - 窗口占屏幕90%，居中显示
   - 图表宽度自适应屏幕宽度

2. **折线图优化**
   - 每行显示2个学生
   - 支持鼠标滚轮滚动
   - 区域占窗口高度60%（更大）
   - 每个折线图完整显示

3. **柱状图优化**
   - 区域占窗口高度25%（更小）
   - x轴人名正常显示（不旋转）
   - 根据学生数量自适应高度

4. **项目文件整理**
   - 文档归档到 `docs/`
   - 脚本分类到 `scripts/`
   - 结构清晰，易于维护

## 使用说明

1. 启动应用后输入账号密码登录
2. 选择或创建班级
3. 添加学生，双击币数单元格修改小码币
4. 点击"图表统计"查看可视化数据
5. 数据自动保存到 `storage_data/` 目录

## 更新日志

详细的版本更新历史请查看：[docs/CHANGELOG.md](docs/CHANGELOG.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 技术支持

如有问题或建议，欢迎提交 Issue。
