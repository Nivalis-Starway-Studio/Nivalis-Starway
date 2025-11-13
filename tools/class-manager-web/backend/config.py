"""
应用配置设置

管理环境变量和应用配置，包括数据库连接、会话密钥等。
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """应用设置类"""
    
    # 应用基础配置
    app_name: str = "课堂管理器Web后端"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 数据库配置
    database_url: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{Path(__file__).parent.parent / "data" / "classroom.db"}"
    )
    
    # 会话和安全配置
    secret_key: str = os.getenv(
        "SECRET_KEY", 
        "classroom-manager-secret-key-change-in-production"
    )
    
    # API配置
    api_prefix: str = "/api/v1"
    
    # CORS配置（开发环境默认允许所有源）
    cors_origins: list[str] = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080"
    ).split(",")
    
    # 开发环境配置
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    def __init__(self):
        """初始化设置，确保数据目录存在"""
        if self.database_url.startswith("sqlite:///"):
            db_path = Path(self.database_url.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)


# 全局设置实例
settings = Settings()