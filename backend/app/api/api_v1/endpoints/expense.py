from datetime import date
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_pet import pet as crud_pet
from app.crud.crud_expense import expense as crud_expense
from app.db.session import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate

router = APIRouter()


@router.get("", response_model=List[ExpenseResponse], summary="获取用户所有宠物的消费记录")
def read_user_expenses(
    *,
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="消费分类过滤"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户所有宠物的消费记录，支持按分类和日期范围过滤
    """
    records = crud_expense.get_by_user_id(
        db,
        user_id=current_user.id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return records


@router.get("/pets/{pet_id}", response_model=List[ExpenseResponse], summary="获取指定宠物的消费记录")
def read_pet_expenses(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    category: Optional[str] = Query(None, description="消费分类过滤"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的所有消费记录，支持按分类和日期范围过滤
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    records = crud_expense.get_by_pet_id(
        db,
        pet_id=pet_id,
        category=category,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return records


@router.post("/pets/{pet_id}", response_model=ExpenseResponse, summary="为宠物添加消费记录")
def create_expense(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_in: ExpenseCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    为指定宠物添加新的消费记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_expense.create(
        db,
        obj_in=ExpenseCreate(**record_in.dict(), pet_id=pet_id)
    )
    return record


@router.get("/pets/{pet_id}/{record_id}", response_model=ExpenseResponse, summary="获取指定消费记录详情")
def read_expense(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据ID获取指定消费记录的详细信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_expense.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消费记录不存在"
        )
    
    return record


@router.put("/pets/{pet_id}/{record_id}", response_model=ExpenseResponse, summary="更新消费记录")
def update_expense(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    record_in: ExpenseUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新指定消费记录的信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_expense.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消费记录不存在"
        )
    
    record = crud_expense.update(db, db_obj=record, obj_in=record_in)
    return record


@router.delete("/pets/{pet_id}/{record_id}", summary="删除消费记录")
def delete_expense(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    删除指定消费记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_expense.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="消费记录不存在"
        )
    
    crud_expense.remove(db, id=record_id)
    return {"message": "消费记录删除成功"}


@router.get("/pets/{pet_id}/count", summary="统计宠物的消费记录数量")
def count_pet_expenses(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    category: Optional[str] = Query(None, description="消费分类过滤"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计指定宠物的消费记录数量，支持按分类统计
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    count = crud_expense.count_by_pet_id(
        db,
        pet_id=pet_id,
        category=category
    )
    return {"count": count}


@router.get("/pets/{pet_id}/total", summary="统计宠物的消费总金额")
def get_pet_total_expense(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    category: Optional[str] = Query(None, description="消费分类过滤"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计指定宠物的消费总金额，支持按分类和日期范围统计
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    total = crud_expense.get_total_amount_by_pet_id(
        db,
        pet_id=pet_id,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    return {"total_amount": total}


@router.get("/total", summary="统计用户所有宠物的消费总金额")
def get_user_total_expense(
    *,
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="消费分类过滤"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计当前用户所有宠物的消费总金额
    """
    total = crud_expense.get_total_amount_by_user_id(
        db,
        user_id=current_user.id,
        category=category,
        start_date=start_date,
        end_date=end_date
    )
    return {"total_amount": total}


@router.get("/pets/{pet_id}/statistics", summary="获取指定宠物的消费统计数据")
def get_pet_expense_statistics(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    year: Optional[int] = Query(None, description="统计年份，默认当前年"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的消费统计数据
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    statistics = crud_expense.get_statistics_by_pet_id(
        db,
        pet_id=pet_id,
        year=year
    )
    return statistics


@router.get("/statistics", summary="获取用户所有宠物的消费统计数据")
def get_user_expense_statistics(
    *,
    db: Session = Depends(get_db),
    year: Optional[int] = Query(None, description="统计年份，默认当前年"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户所有宠物的消费统计数据
    """
    statistics = crud_expense.get_statistics_by_user_id(
        db,
        user_id=current_user.id,
        year=year
    )
    return statistics
