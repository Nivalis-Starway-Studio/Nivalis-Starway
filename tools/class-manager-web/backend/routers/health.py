"""
健康检查路由

提供应用健康状态检查端点。
"""

from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database import get_db
from ..schemas import HealthCheck
from ..config import settings

router = APIRouter()


@router.get("/health", response_model=HealthCheck, status_code=200)
async def health_check(db: Session = Depends(get_db)):
    """
    健康检查端点
    
    检查应用和数据库连接状态，返回系统健康信息。
    """
    try:
        # 测试数据库连接
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return HealthCheck(
        status=db_status,
        timestamp=datetime.utcnow(),
        version=settings.version,
        environment=settings.environment
    )


@router.get("/status", response_model=HealthCheck, status_code=200)
async def app_status(db: Session = Depends(get_db)):
    """
    应用状态端点
    
    返回应用当前状态信息，等同于健康检查。
    """
    return await health_check(db)