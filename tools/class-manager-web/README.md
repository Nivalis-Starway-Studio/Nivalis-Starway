# 课堂管理器Web后端

基于FastAPI的RESTful API服务，提供课堂和学生管理功能。

## 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd tools/class-manager-web

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行应用

```bash
# 使用uvicorn运行（推荐）
uvicorn tools.class-manager-web.backend.main:app --reload

# 或直接运行主文件
python3 tools/class-manager-web/backend/main.py
```

### 3. 访问API文档

应用启动后，访问以下地址：

- API根地址：http://localhost:8000
- 交互式API文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc
- 健康检查：http://localhost:8000/api/v1/health

## 环境变量配置

可以通过环境变量自定义配置：

```bash
# 调试模式
DEBUG=true

# 数据库URL（默认使用SQLite）
DATABASE_URL=sqlite:///./data/classroom.db

# 会话密钥（生产环境必须更改）
SECRET_KEY=your-secret-key-here

# CORS允许的源
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# 环境类型
ENVIRONMENT=development
```

## 项目结构

```
tools/class-manager-web/
├── backend/                    # 后端包
│   ├── __init__.py            # 包初始化
│   ├── main.py                # FastAPI应用入口
│   ├── config.py              # 配置管理
│   ├── database.py            # 数据库配置
│   ├── models.py              # SQLAlchemy数据模型
│   ├── schemas.py             # Pydantic数据模式
│   └── routers/               # API路由
│       ├── __init__.py
│       └── health.py          # 健康检查路由
├── requirements.txt           # Python依赖
├── .gitignore                # Git忽略文件
└── README.md                 # 项目说明
```

## API端点

### 健康检查

- `GET /api/v1/health` - 应用健康状态检查
- `GET /api/v1/status` - 应用状态信息

## 开发说明

- 使用SQLite作为默认数据库，数据文件存储在`data/classroom.db`
- 支持自动数据库表创建
- 包含CORS中间件，支持前端开发
- 提供完整的API文档和交互式测试界面

## 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=backend tests/
```