# 项目结构说明 / Project Structure

## 目录结构 / Directory Structure

```
/home/engine/project/
│
├── README.md                   # 项目主文档 / Main documentation
├── CHANGELOG.md                # 版本更新日志 / Version changelog
├── LICENSE                     # 开源许可证 / Open source license
├── requirements.txt            # Python依赖列表 / Python dependencies
├── .gitignore                  # Git忽略配置 / Git ignore config
│
├── docs/                       # 📚 文档目录 / Documentation directory
│   ├── README.md              # 主文档（符号链接）/ Main doc (symlink)
│   ├── CHANGELOG.md           # 更新日志（符号链接）/ Changelog (symlink)
│   ├── BUILD_README.md        # 打包构建指南 / Build guide
│   ├── PROJECT_STRUCTURE.md   # 项目结构说明（本文件）/ Structure guide (this file)
│   └── archive/               # 📦 历史文档归档 / Historical docs archive
│       ├── CHANGES.md
│       ├── CHANGES_SUMMARY.md
│       ├── CHART_OPTIMIZATION.md
│       ├── FINAL_VERIFICATION.md
│       ├── OPTIMIZATION_SUMMARY.md
│       ├── OPTIMIZATION_SUMMARY_v2.0.md
│       ├── PROJECT_SUMMARY.md
│       ├── README_v1.3.md
│       └── index.html
│
├── scripts/                    # 🔧 脚本目录 / Scripts directory
│   ├── build/                 # 打包脚本 / Build scripts
│   │   ├── build_exe.py       # Python跨平台打包脚本 / Python cross-platform build script
│   │   ├── build_exe.bat      # Windows打包脚本 / Windows build script
│   │   ├── build_windows.bat  # Windows打包脚本（备用）/ Windows build script (backup)
│   │   └── ClassManagerApp.spec  # PyInstaller配置文件 / PyInstaller config
│   ├── run/                   # 运行脚本 / Run scripts
│   │   ├── run_app.bat        # Windows运行脚本 / Windows run script
│   │   └── run_app.sh         # Linux/Mac运行脚本 / Linux/Mac run script
│   └── test/                  # 测试脚本 / Test scripts
│       ├── test_chart_optimization.py  # 图表优化测试 / Chart optimization test
│       └── test_v1.3.py       # v1.3版本测试 / v1.3 version test
│
├── tools/                      # 🛠️ 应用主代码 / Application main code
│   └── class-manager-app/
│       ├── main.py            # 程序入口 / Program entry point
│       ├── run.py             # PyInstaller适配层 / PyInstaller adapter
│       ├── data/              # 数据层 / Data layer
│       │   ├── __init__.py
│       │   ├── models.py      # 数据模型（Student, Classroom）/ Data models
│       │   ├── store.py       # 数据存储管理 / Data store management
│       │   └── excel_storage.py  # CSV持久化存储 / CSV persistence storage
│       ├── ui/                # UI层 / UI layer
│       │   ├── __init__.py
│       │   ├── login_view.py  # 登录视图 / Login view
│       │   ├── main_view.py   # 主视图 / Main view
│       │   └── class_detail_view.py  # 班级详情视图 / Class detail view
│       └── storage_data/      # 数据文件目录（运行时生成）/ Data files (generated at runtime)
│           └── *.csv          # CSV数据文件 / CSV data files
│
└── shared/                     # 🔄 共享资源 / Shared resources
    └── ...
```

## 文件说明 / File Description

### 根目录文件 / Root Files

- **README.md**：项目主文档，包含快速开始、功能介绍等
- **CHANGELOG.md**：版本更新日志，记录所有版本的改动
- **LICENSE**：MIT开源许可证
- **requirements.txt**：Python依赖包列表
- **.gitignore**：Git版本控制忽略配置

### docs/ - 文档目录

- **BUILD_README.md**：详细的打包和构建指南
- **PROJECT_STRUCTURE.md**：项目结构说明（本文件）
- **archive/**：历史版本文档归档，保留项目演进历史

### scripts/ - 脚本目录

#### scripts/build/ - 打包脚本
- **build_exe.py**：跨平台Python打包脚本，使用PyInstaller
- **build_exe.bat**：Windows一键打包批处理脚本
- **ClassManagerApp.spec**：PyInstaller配置文件

#### scripts/run/ - 运行脚本
- **run_app.bat**：Windows快速启动脚本
- **run_app.sh**：Linux/Mac快速启动脚本

#### scripts/test/ - 测试脚本
- **test_chart_optimization.py**：图表优化功能测试
- **test_v1.3.py**：v1.3版本功能测试

### tools/class-manager-app/ - 应用主代码

#### 核心文件
- **main.py**：应用程序主入口，包含主控制器
- **run.py**：PyInstaller打包适配层

#### data/ - 数据层
- **models.py**：数据模型定义
  - `Student`：学生数据类
  - `Classroom`：班级数据类
- **store.py**：数据存储管理类
  - `ClassDataStore`：统一数据管理接口
- **excel_storage.py**：CSV持久化存储实现

#### ui/ - UI层
- **login_view.py**：登录界面
  - 账号密码输入
  - 登录验证
- **main_view.py**：主界面
  - 班级列表显示
  - 班级创建/删除
- **class_detail_view.py**：班级详情界面
  - 学生列表管理
  - 小码币编辑
  - 图表统计（v4.0优化）

## 设计原则 / Design Principles

1. **分层架构**：数据层、UI层分离，职责清晰
2. **模块化**：每个功能模块独立，易于维护
3. **文档完善**：重要功能都有详细文档说明
4. **脚本集中**：所有脚本统一放在scripts目录
5. **历史归档**：旧版本文档归档保留，便于追溯

## 数据流 / Data Flow

```
用户操作 (UI Layer)
    ↓
控制器 (Controller)
    ↓
数据存储 (ClassDataStore)
    ↓
数据模型 (Student/Classroom)
    ↓
持久化 (CSV Storage)
```

## 构建流程 / Build Process

```
源代码 (tools/class-manager-app/)
    ↓
打包脚本 (scripts/build/)
    ↓
PyInstaller
    ↓
可执行文件 (dist/)
```

## 版本历史 / Version History

- **v4.0**：图表自适应 + 文件整理（当前版本）
- **v3.0**：图表布局优化
- **v2.0**：图表统计功能
- **v1.3**：UI优化 + 打包发布
- **v1.0-v1.2**：基础功能开发

## 维护指南 / Maintenance Guide

### 添加新功能
1. 在 `tools/class-manager-app/` 下对应模块添加代码
2. 更新 `CHANGELOG.md` 记录改动
3. 如需要，更新 `README.md` 文档

### 创建新版本
1. 更新版本号
2. 在 `CHANGELOG.md` 添加版本日志
3. 执行打包脚本生成可执行文件
4. 测试验证

### 文档更新
1. 主文档更新在根目录的 `README.md`
2. 详细文档更新在 `docs/` 目录
3. 历史文档归档到 `docs/archive/`

## 技术栈 / Tech Stack

- **语言**：Python 3.7+
- **GUI框架**：Tkinter
- **图表库**：Matplotlib
- **数据存储**：CSV文件
- **打包工具**：PyInstaller

---

更新时间：2024-11-14
版本：v4.0
