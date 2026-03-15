from datetime import date, timedelta
from typing import List, Optional, Tuple

from sqlalchemy import and_, func, Float
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.health_record import HealthRecord
from app.schemas.health_record import HealthRecordCreate, HealthRecordUpdate


class CRUDHealthRecord(CRUDBase[HealthRecord, HealthRecordCreate, HealthRecordUpdate]):
    """
    健康记录CRUD操作类
    """
    def get_by_pet_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        record_type: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[HealthRecord]:
        """
        根据宠物ID获取健康记录列表，支持按类型和日期范围过滤
        """
        query = db.query(self.model).filter(self.model.pet_id == pet_id)
        
        if record_type:
            query = query.filter(self.model.record_type == record_type)
        
        if start_date:
            query = query.filter(self.model.record_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.record_date <= end_date)
        
        return query.order_by(self.model.record_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_pet_and_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        record_id: int
    ) -> Optional[HealthRecord]:
        """
        根据宠物ID和记录ID获取健康记录
        """
        return db.query(self.model).filter(
            self.model.pet_id == pet_id,
            self.model.id == record_id
        ).first()
    
    def get_weight_trend(
        self,
        db: Session,
        *,
        pet_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Tuple[date, float]]:
        """
        获取宠物的体重变化趋势数据
        """
        query = db.query(
            self.model.record_date,
            self.model.content.cast(Float)
        ).filter(
            self.model.pet_id == pet_id,
            self.model.record_type == "weight",
            self.model.content.isnot(None)
        )
        
        if start_date:
            query = query.filter(self.model.record_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.record_date <= end_date)
        
        return query.order_by(self.model.record_date.asc()).all()
    
    def get_upcoming_checkups(
        self,
        db: Session,
        *,
        user_id: int,
        days: int = 30
    ) -> List[HealthRecord]:
        """
        获取用户即将到来的复查提醒（指定天数内）
        """
        from app.models.pet import Pet
        
        today = date.today()
        end_date = today + timedelta(days=days)
        
        return db.query(self.model)\
            .join(Pet, self.model.pet_id == Pet.id)\
            .filter(
                Pet.user_id == user_id,
                Pet.is_active == True,
                self.model.next_check_date.isnot(None),
                self.model.next_check_date >= today,
                self.model.next_check_date <= end_date
            )\
            .order_by(self.model.next_check_date.asc())\
            .all()
    
    def count_by_pet_id(
        self,
        db: Session,
        *,
        pet_id: int,
        record_type: Optional[str] = None
    ) -> int:
        """
        统计宠物的健康记录数量，支持按类型统计
        """
        query = db.query(self.model).filter(self.model.pet_id == pet_id)
        
        if record_type:
            query = query.filter(self.model.record_type == record_type)
        
        return query.count()
    
    def get_statistics(
        self,
        db: Session,
        *,
        pet_id: int,
        year: Optional[int] = None
    ) -> dict:
        """
        获取宠物健康记录统计数据
        """
        if not year:
            year = date.today().year
        
        # 按类型统计数量
        type_stats = db.query(
            self.model.record_type,
            func.count(self.model.id).label("count")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.record_date) == year
        ).group_by(self.model.record_type).all()
        
        # 按月份统计数量
        month_stats = db.query(
            func.month(self.model.record_date).label("month"),
            func.count(self.model.id).label("count")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.record_date) == year
        ).group_by(func.month(self.model.record_date)).all()
        
        # 统计总费用
        total_cost = db.query(
            func.sum(self.model.cost).label("total")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.record_date) == year
        ).scalar() or 0
        
        return {
            "type_stats": {t: c for t, c in type_stats},
            "month_stats": {m: c for m, c in month_stats},
            "total_cost": float(total_cost),
            "year": year
        }


health_record = CRUDHealthRecord(HealthRecord)
