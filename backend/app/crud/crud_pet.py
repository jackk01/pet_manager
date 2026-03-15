from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate


class CRUDPet(CRUDBase[Pet, PetCreate, PetUpdate]):
    """
    宠物CRUD操作类
    """
    def get_by_user_id(
        self, 
        db: Session, 
        *, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        include_inactive: bool = False
    ) -> List[Pet]:
        """
        根据用户ID获取宠物列表
        """
        query = db.query(self.model).filter(self.model.user_id == user_id)
        
        if not include_inactive:
            query = query.filter(self.model.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_user_and_id(
        self, 
        db: Session, 
        *, 
        user_id: int, 
        pet_id: int
    ) -> Optional[Pet]:
        """
        根据用户ID和宠物ID获取宠物信息
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.id == pet_id
        ).first()
    
    def create_with_user(
        self, 
        db: Session, 
        *, 
        obj_in: PetCreate, 
        user_id: int
    ) -> Pet:
        """
        创建属于指定用户的宠物
        """
        db_obj = self.model(
            **obj_in.dict(),
            user_id=user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def count_by_user_id(
        self, 
        db: Session, 
        *, 
        user_id: int,
        include_inactive: bool = False
    ) -> int:
        """
        统计用户的宠物数量
        """
        query = db.query(self.model).filter(self.model.user_id == user_id)
        
        if not include_inactive:
            query = query.filter(self.model.is_active == True)
        
        return query.count()


pet = CRUDPet(Pet)
