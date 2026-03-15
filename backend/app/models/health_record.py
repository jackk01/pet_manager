from datetime import datetime
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class HealthRecord(Base):
    """
    健康记录模型
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pet_id = Column(Integer, ForeignKey("pet.id"), nullable=False, comment="宠物ID")
    record_type = Column(String(20), nullable=False, comment="记录类型：就诊/体检/体重/驱虫/过敏/手术/其他")
    record_date = Column(Date, nullable=False, comment="记录日期")
    title = Column(String(200), nullable=False, comment="标题")
    content = Column(Text, comment="详细内容")
    hospital = Column(String(100), comment="医院名称")
    doctor = Column(String(50), comment="医生姓名")
    cost = Column(Float, comment="费用")
    attachment = Column(String(255), comment="附件路径")
    next_check_date = Column(Date, comment="下次复查日期")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    pet = relationship("Pet", back_populates="health_records")
    
    def __repr__(self):
        return f"<HealthRecord {self.title} for pet {self.pet_id}>"
