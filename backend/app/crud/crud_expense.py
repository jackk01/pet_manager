from datetime import date
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


class CRUDExpense(CRUDBase[Expense, ExpenseCreate, ExpenseUpdate]):
    """
    消费记录CRUD操作类
    """
    def get_by_pet_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Expense]:
        """
        根据宠物ID获取消费记录列表，支持按分类和日期范围过滤
        """
        query = db.query(self.model).filter(self.model.pet_id == pet_id)
        
        if category:
            query = query.filter(self.model.category == category)
        
        if start_date:
            query = query.filter(self.model.expense_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.expense_date <= end_date)
        
        return query.order_by(self.model.expense_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_user_id(
        self,
        db: Session,
        *,
        user_id: int,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Expense]:
        """
        根据用户ID获取所有宠物的消费记录
        """
        from app.models.pet import Pet
        
        query = db.query(self.model)\
            .join(Pet, self.model.pet_id == Pet.id)\
            .filter(Pet.user_id == user_id, Pet.is_active == True)
        
        if category:
            query = query.filter(self.model.category == category)
        
        if start_date:
            query = query.filter(self.model.expense_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.expense_date <= end_date)
        
        return query.order_by(self.model.expense_date.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_pet_and_id(
        self, 
        db: Session, 
        *, 
        pet_id: int, 
        record_id: int
    ) -> Optional[Expense]:
        """
        根据宠物ID和记录ID获取消费记录
        """
        return db.query(self.model).filter(
            self.model.pet_id == pet_id,
            self.model.id == record_id
        ).first()
    
    def count_by_pet_id(
        self,
        db: Session,
        *,
        pet_id: int,
        category: Optional[str] = None
    ) -> int:
        """
        统计宠物的消费记录数量，支持按分类统计
        """
        query = db.query(self.model).filter(self.model.pet_id == pet_id)
        
        if category:
            query = query.filter(self.model.category == category)
        
        return query.count()
    
    def get_total_amount_by_pet_id(
        self,
        db: Session,
        *,
        pet_id: int,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        统计宠物的消费总金额，支持按分类和日期范围统计
        """
        query = db.query(func.sum(self.model.amount)).filter(self.model.pet_id == pet_id)
        
        if category:
            query = query.filter(self.model.category == category)
        
        if start_date:
            query = query.filter(self.model.expense_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.expense_date <= end_date)
        
        total = query.scalar() or 0
        return float(total)
    
    def get_total_amount_by_user_id(
        self,
        db: Session,
        *,
        user_id: int,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> float:
        """
        统计用户所有宠物的消费总金额
        """
        from app.models.pet import Pet
        
        query = db.query(func.sum(self.model.amount))\
            .join(Pet, self.model.pet_id == Pet.id)\
            .filter(Pet.user_id == user_id, Pet.is_active == True)
        
        if category:
            query = query.filter(self.model.category == category)
        
        if start_date:
            query = query.filter(self.model.expense_date >= start_date)
        
        if end_date:
            query = query.filter(self.model.expense_date <= end_date)
        
        total = query.scalar() or 0
        return float(total)
    
    def get_statistics_by_pet_id(
        self,
        db: Session,
        *,
        pet_id: int,
        year: Optional[int] = None
    ) -> dict:
        """
        获取指定宠物的消费统计数据
        """
        if not year:
            year = date.today().year
        
        # 按分类统计金额
        category_stats = db.query(
            self.model.category,
            func.sum(self.model.amount).label("amount"),
            func.count(self.model.id).label("count")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.expense_date) == year
        ).group_by(self.model.category).all()
        
        # 按月份统计金额
        month_stats = db.query(
            func.month(self.model.expense_date).label("month"),
            func.sum(self.model.amount).label("amount"),
            func.count(self.model.id).label("count")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.expense_date) == year
        ).group_by(func.month(self.model.expense_date)).all()
        
        # 统计年度总金额
        total_amount = db.query(
            func.sum(self.model.amount).label("total")
        ).filter(
            self.model.pet_id == pet_id,
            func.year(self.model.expense_date) == year
        ).scalar() or 0
        
        return {
            "category_stats": {
                cat: {"amount": float(amt), "count": cnt} 
                for cat, amt, cnt in category_stats
            },
            "month_stats": {
                month: {"amount": float(amt), "count": cnt} 
                for month, amt, cnt in month_stats
            },
            "total_amount": float(total_amount),
            "year": year
        }
    
    def get_statistics_by_user_id(
        self,
        db: Session,
        *,
        user_id: int,
        year: Optional[int] = None
    ) -> dict:
        """
        获取用户所有宠物的消费统计数据
        """
        from app.models.pet import Pet
        
        if not year:
            year = date.today().year
        
        # 按分类统计金额
        category_stats = db.query(
            self.model.category,
            func.sum(self.model.amount).label("amount"),
            func.count(self.model.id).label("count")
        ).join(Pet, self.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == user_id,
            Pet.is_active == True,
            func.year(self.model.expense_date) == year
        ).group_by(self.model.category).all()
        
        # 按月份统计金额
        month_stats = db.query(
            func.month(self.model.expense_date).label("month"),
            func.sum(self.model.amount).label("amount"),
            func.count(self.model.id).label("count")
        ).join(Pet, self.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == user_id,
            Pet.is_active == True,
            func.year(self.model.expense_date) == year
        ).group_by(func.month(self.model.expense_date)).all()
        
        # 按宠物统计金额
        pet_stats = db.query(
            Pet.name,
            Pet.id,
            func.sum(self.model.amount).label("amount"),
            func.count(self.model.id).label("count")
        ).join(Pet, self.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == user_id,
            Pet.is_active == True,
            func.year(self.model.expense_date) == year
        ).group_by(Pet.id, Pet.name).all()
        
        # 统计年度总金额
        total_amount = db.query(
            func.sum(self.model.amount).label("total")
        ).join(Pet, self.model.pet_id == Pet.id)\
        .filter(
            Pet.user_id == user_id,
            Pet.is_active == True,
            func.year(self.model.expense_date) == year
        ).scalar() or 0
        
        return {
            "category_stats": {
                cat: {"amount": float(amt), "count": cnt} 
                for cat, amt, cnt in category_stats
            },
            "month_stats": {
                month: {"amount": float(amt), "count": cnt} 
                for month, amt, cnt in month_stats
            },
            "pet_stats": {
                pet_id: {"name": name, "amount": float(amt), "count": cnt} 
                for name, pet_id, amt, cnt in pet_stats
            },
            "total_amount": float(total_amount),
            "year": year
        }


expense = CRUDExpense(Expense)
