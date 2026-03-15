from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pet(Base):
    """
    宠物信息模型
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, comment="所属用户ID")
    name = Column(String(50), nullable=False, comment="宠物名称")
    breed = Column(String(100), comment="品种")
    gender = Column(String(10), comment="性别：公/母/未知")
    birth_date = Column(Date, comment="出生日期")
    weight = Column(Float, comment="当前体重（kg）")
    color = Column(String(50), comment="毛色")
    chip_number = Column(String(50), comment="芯片号")
    description = Column(Text, comment="特征描述")
    personality = Column(Text, comment="性格特点")
    avatar = Column(String(255), comment="宠物头像路径")
    is_active = Column(Boolean, default=True, comment="是否有效")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    owner = relationship("User", back_populates="pets")
    vaccinations = relationship("Vaccination", back_populates="pet", cascade="all, delete-orphan")
    health_records = relationship("HealthRecord", back_populates="pet", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="pet", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pet {self.name}>"
