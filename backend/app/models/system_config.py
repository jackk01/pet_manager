from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.base import Base


class SystemConfig(Base):
    """
    系统配置模型
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    config_key = Column(String(50), unique=True, index=True, nullable=False, comment="配置键")
    config_value = Column(Text, comment="配置值")
    description = Column(String(200), comment="配置说明")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<SystemConfig {self.config_key}>"
