from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# 基础用户模型
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")


# 用户创建模型
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50, description="密码")


# 用户更新模型
class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号码")
    avatar: Optional[str] = Field(None, description="头像路径")


# 修改密码模型
class UserChangePassword(BaseModel):
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=50, description="新密码")


# 用户响应模型
class UserResponse(UserBase):
    id: int
    avatar: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# 用户登录模型
class UserLogin(BaseModel):
    username: str = Field(..., description="用户名/邮箱")
    password: str = Field(..., description="密码")
