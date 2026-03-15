from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


# 基础消费记录模型
class ExpenseBase(BaseModel):
    category: str = Field(..., description="消费分类：food/medical/grooming/supplies/insurance/other")
    expense_date: date = Field(..., description="消费日期")
    amount: float = Field(..., gt=0, description="金额")
    merchant: Optional[str] = Field(None, max_length=100, description="商家名称")
    remark: Optional[str] = Field(None, description="备注")
    attachment: Optional[str] = Field(None, description="小票/凭证路径")


# 消费记录创建模型
class ExpenseCreate(ExpenseBase):
    pass


# 消费记录更新模型
class ExpenseUpdate(ExpenseBase):
    category: Optional[str] = Field(None, description="消费分类：food/medical/grooming/supplies/insurance/other")
    expense_date: Optional[date] = Field(None, description="消费日期")
    amount: Optional[float] = Field(None, gt=0, description="金额")


# 消费记录响应模型
class ExpenseResponse(ExpenseBase):
    id: int
    pet_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
