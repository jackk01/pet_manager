from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Vaccination(Base):
    """
    疫苗记录模型
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pet_id = Column(Integer, ForeignKey("pet.id"), nullable=False, comment="宠物ID")
    vaccine_name = Column(String(100), nullable=False, comment="疫苗名称")
    vaccination_date = Column(Date, nullable=False, comment="接种日期")
    next_due_date = Column(Date, comment="下次接种日期")
    clinic = Column(String(100), comment="接种单位")
    doctor = Column(String(50), comment="医生姓名")
    batch_number = Column(String(50), comment="疫苗批次号")
    remark = Column(Text, comment="备注")
    attachment = Column(String(255), comment="附件路径")
    is_reminded = Column(Boolean, default=False, comment="是否已提醒")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    pet = relationship("Pet", back_populates="vaccinations")
    
    def __repr__(self):
        return f"<Vaccination {self.vaccine_name} for pet {self.pet_id}>"
