from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Expense(Base):
    """
    消费记录模型
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pet_id = Column(Integer, ForeignKey("pet.id"), nullable=False, comment="宠物ID")
    category = Column(String(20), nullable=False, comment="消费分类：food/medical/grooming/supplies/insurance/other")
    expense_date = Column(Date, nullable=False, comment="消费日期")
    amount = Column(Float, nullable=False, comment="金额")
    merchant = Column(String(100), comment="商家名称")
    remark = Column(Text, comment="备注")
    attachment = Column(String(255), comment="小票/凭证路径")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    pet = relationship("Pet", back_populates="expenses")
    
    def __repr__(self):
        return f"<Expense {self.amount} for pet {self.pet_id}>"
