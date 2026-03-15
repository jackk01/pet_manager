from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# 基础健康记录模型
class HealthRecordBase(BaseModel):
    record_type: str = Field(..., description="记录类型：就诊/体检/体重/驱虫/过敏/手术/其他")
    record_date: date = Field(..., description="记录日期")
    title: str = Field(..., min_length=1, max_length=200, description="标题")
    content: Optional[str] = Field(None, description="详细内容")
    hospital: Optional[str] = Field(None, max_length=100, description="医院名称")
    doctor: Optional[str] = Field(None, max_length=50, description="医生姓名")
    cost: Optional[float] = Field(None, ge=0, description="费用")
    attachment: Optional[str] = Field(None, description="附件路径")
    next_check_date: Optional[date] = Field(None, description="下次复查日期")


# 健康记录创建模型
class HealthRecordCreate(HealthRecordBase):
    pass


# 健康记录更新模型
class HealthRecordUpdate(HealthRecordBase):
    record_type: Optional[str] = Field(None, description="记录类型：visit/weight/deworming/allergy/surgery/other")
    record_date: Optional[date] = Field(None, description="记录日期")
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="标题")


# 健康记录响应模型
class HealthRecordResponse(HealthRecordBase):
    id: int
    pet_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
