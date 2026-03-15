from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# 基础宠物模型
class PetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="宠物名称")
    breed: Optional[str] = Field(None, max_length=100, description="品种")
    gender: Optional[str] = Field(None, description="性别：公/母/未知")
    birth_date: Optional[date] = Field(None, description="出生日期")
    weight: Optional[float] = Field(None, ge=0, description="当前体重（kg）")
    color: Optional[str] = Field(None, max_length=50, description="毛色")
    chip_number: Optional[str] = Field(None, max_length=50, description="芯片号")
    description: Optional[str] = Field(None, description="特征描述")
    personality: Optional[str] = Field(None, description="性格特点")
    avatar: Optional[str] = Field(None, description="宠物头像路径")


# 宠物创建模型
class PetCreate(PetBase):
    pass


# 宠物更新模型
class PetUpdate(PetBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="宠物名称")
    is_active: Optional[bool] = Field(None, description="是否有效")


# 宠物响应模型
class PetResponse(PetBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
