from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# 基础疫苗记录模型
class VaccinationBase(BaseModel):
    vaccine_name: str = Field(..., min_length=1, max_length=100, description="疫苗名称")
    vaccination_date: date = Field(..., description="接种日期")
    next_due_date: Optional[date] = Field(None, description="下次接种日期")
    clinic: Optional[str] = Field(None, max_length=100, description="接种单位")
    doctor: Optional[str] = Field(None, max_length=50, description="医生姓名")
    batch_number: Optional[str] = Field(None, max_length=50, description="疫苗批次号")
    remark: Optional[str] = Field(None, description="备注")
    attachment: Optional[str] = Field(None, description="附件路径")
    is_reminded: Optional[bool] = Field(False, description="是否已提醒")


# 疫苗记录创建模型
class VaccinationCreate(VaccinationBase):
    pass


# 疫苗记录更新模型
class VaccinationUpdate(VaccinationBase):
    vaccine_name: Optional[str] = Field(None, min_length=1, max_length=100, description="疫苗名称")
    vaccination_date: Optional[date] = Field(None, description="接种日期")


# 疫苗记录响应模型
class VaccinationResponse(VaccinationBase):
    id: int
    pet_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
