"""
FastAPI应用主入口

课堂管理器Web后端API服务的主应用文件。
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    print("正在初始化数据库...")
    init_db()
    print("数据库初始化完成")
    
    yield
    
    # 关闭时清理资源
    print("应用关闭，清理资源...")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="基于FastAPI的课堂管理器Web后端API服务",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["健康检查"]
)


@app.get("/")
async def root():
    """根路径欢迎信息"""
    return {
        "message": f"欢迎使用{settings.app_name}",
        "version": settings.version,
        "docs": "/docs" if settings.debug else "文档在开发环境中可用",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )