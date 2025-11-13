"""
Pydantic数据模式

定义API请求和响应的数据验证模式。
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# 基础模式
class BaseSchema(BaseModel):
    """基础模式类"""
    class Config:
        from_attributes = True


# 用户相关模式
class UserBase(BaseSchema):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """创建用户模式"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseSchema):
    """更新用户模式"""
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class User(UserBase):
    """用户响应模式"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


# 课堂相关模式
class ClassroomBase(BaseSchema):
    """课堂基础模式"""
    name: str = Field(..., min_length=1, max_length=100)
    grade_level: str = Field(..., max_length=20)
    description: Optional[str] = Field(None, max_length=500)


class ClassroomCreate(ClassroomBase):
    """创建课堂模式"""
    pass


class ClassroomUpdate(BaseSchema):
    """更新课堂模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    grade_level: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=500)


class Classroom(ClassroomBase):
    """课堂响应模式"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    student_count: Optional[int] = 0  # 学生数量


# 学生相关模式
class StudentBase(BaseSchema):
    """学生基础模式"""
    name: str = Field(..., min_length=1, max_length=100)
    student_number: Optional[str] = Field(None, max_length=50)
    weekly_coins: int = Field(0, ge=0)
    cumulative_coins: int = Field(0, ge=0)


class StudentCreate(StudentBase):
    """创建学生模式"""
    classroom_id: int = Field(..., gt=0)


class StudentUpdate(BaseSchema):
    """更新学生模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    student_number: Optional[str] = Field(None, max_length=50)
    weekly_coins: Optional[int] = Field(None, ge=0)
    cumulative_coins: Optional[int] = Field(None, ge=0)
    classroom_id: Optional[int] = Field(None, gt=0)


class Student(StudentBase):
    """学生响应模式"""
    id: int
    classroom_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    classroom: Optional[Classroom] = None


# 包含课堂信息的学生模式
class StudentWithClassroom(Student):
    """包含课堂信息的学生模式"""
    classroom: Classroom


# 课堂统计模式
class ClassroomStats(BaseSchema):
    """课堂统计模式"""
    total_students: int
    total_weekly_coins: int
    total_cumulative_coins: int


# 健康检查模式
class HealthCheck(BaseSchema):
    """健康检查响应模式"""
    status: str = "healthy"
    timestamp: datetime
    version: str
    environment: str