from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.vaccination import Vaccination
from app.schemas.vaccination import VaccinationCreate, VaccinationUpdate


class CRUDVaccination(CRUDBase[Vaccination, VaccinationCreate, VaccinationUpdate]):
    """
    疫苗记录CRUD操作类
    """
    def get_by_pet_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Vaccination]:
        """
        根据宠物ID获取疫苗记录列表
        """
        return db.query(self.model)\
            .filter(self.model.pet_id == pet_id)\
            .order_by(self.model.vaccination_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_pet_and_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        record_id: int
    ) -> Optional[Vaccination]:
        """
        根据宠物ID和记录ID获取疫苗记录
        """
        return db.query(self.model).filter(
            self.model.pet_id == pet_id,
            self.model.id == record_id
        ).first()
    
    def get_upcoming_by_user_id(
        self,
        db: Session,
        *,
        user_id: int,
        days: int = 30
    ) -> List[Vaccination]:
        """
        获取用户即将到期的疫苗提醒（指定天数内）
        """
        from app.models.pet import Pet
        
        today = date.today()
        end_date = today + timedelta(days=days)
        
        return db.query(self.model)\
            .join(Pet, self.model.pet_id == Pet.id)\
            .filter(
                Pet.user_id == user_id,
                Pet.is_active == True,
                self.model.next_due_date.isnot(None),
                self.model.next_due_date >= today,
                self.model.next_due_date <= end_date,
                self.model.is_reminded == False
            )\
            .order_by(self.model.next_due_date.asc())\
            .all()
    
    def get_expired_by_user_id(
        self,
        db: Session,
        *,
        user_id: int
    ) -> List[Vaccination]:
        """
        获取用户已过期的疫苗记录
        """
        from app.models.pet import Pet
        
        today = date.today()
        
        return db.query(self.model)\
            .join(Pet, self.model.pet_id == Pet.id)\
            .filter(
                Pet.user_id == user_id,
                Pet.is_active == True,
                self.model.next_due_date.isnot(None),
                self.model.next_due_date < today,
                self.model.is_reminded == False
            )\
            .order_by(self.model.next_due_date.asc())\
            .all()
    
    def mark_as_reminded(
        self,
        db: Session,
        *,
        record_id: int
    ) -> Optional[Vaccination]:
        """
        标记疫苗记录为已提醒
        """
        record = self.get(db, id=record_id)
        if record:
            record.is_reminded = True
            db.add(record)
            db.commit()
            db.refresh(record)
        return record
    
    def count_by_pet_id(
        self,
        db: Session,
        *,
        pet_id: int
    ) -> int:
        """
        统计宠物的疫苗记录数量
        """
        return db.query(self.model)\
            .filter(self.model.pet_id == pet_id)\
            .count()


vaccination = CRUDVaccination(Vaccination)
