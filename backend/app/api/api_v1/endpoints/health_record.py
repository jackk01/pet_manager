from datetime import date
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_pet import pet as crud_pet
from app.crud.crud_health_record import health_record as crud_health_record
from app.db.session import get_db
from app.models.user import User
from app.schemas.health_record import HealthRecordCreate, HealthRecordResponse, HealthRecordUpdate

router = APIRouter()


@router.get("/upcoming-checkups", response_model=List[HealthRecordResponse], summary="获取即将到来的复查提醒")
def get_upcoming_checkups(
    *,
    db: Session = Depends(get_db),
    days: int = 30,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户即将到来的复查提醒（默认30天内）
    """
    records = crud_health_record.get_upcoming_checkups(
        db,
        user_id=current_user.id,
        days=days
    )
    return records


@router.get("/pets/{pet_id}", response_model=List[HealthRecordResponse], summary="获取指定宠物的健康记录")
def read_pet_health_records(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_type: Optional[str] = Query(None, description="记录类型过滤"),
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的所有健康记录，支持按类型和日期范围过滤
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    records = crud_health_record.get_by_pet_id(
        db,
        pet_id=pet_id,
        record_type=record_type,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return records


@router.post("/pets/{pet_id}", response_model=HealthRecordResponse, summary="为宠物添加健康记录")
def create_health_record(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_in: HealthRecordCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    为指定宠物添加新的健康记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_health_record.create(
        db,
        obj_in=HealthRecordCreate(**record_in.dict(), pet_id=pet_id)
    )
    return record


@router.get("/pets/{pet_id}/{record_id}", response_model=HealthRecordResponse, summary="获取指定健康记录详情")
def read_health_record(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据ID获取指定健康记录的详细信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_health_record.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康记录不存在"
        )
    
    return record


@router.put("/pets/{pet_id}/{record_id}", response_model=HealthRecordResponse, summary="更新健康记录")
def update_health_record(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    record_in: HealthRecordUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新指定健康记录的信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_health_record.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康记录不存在"
        )
    
    record = crud_health_record.update(db, db_obj=record, obj_in=record_in)
    return record


@router.delete("/pets/{pet_id}/{record_id}", summary="删除健康记录")
def delete_health_record(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    删除指定健康记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    record = crud_health_record.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="健康记录不存在"
        )
    
    crud_health_record.remove(db, id=record_id)
    return {"message": "健康记录删除成功"}


@router.get("/pets/{pet_id}/weight-trend", summary="获取宠物体重变化趋势")
def get_weight_trend(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的体重变化趋势数据
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    trend_data = crud_health_record.get_weight_trend(
        db,
        pet_id=pet_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return [
        {"date": record_date.isoformat(), "weight": weight}
        for record_date, weight in trend_data
    ]


@router.get("/pets/{pet_id}/count", summary="统计宠物的健康记录数量")
def count_health_records(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_type: Optional[str] = Query(None, description="记录类型过滤"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计指定宠物的健康记录数量，支持按类型统计
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    count = crud_health_record.count_by_pet_id(
        db,
        pet_id=pet_id,
        record_type=record_type
    )
    return {"count": count}


@router.get("/pets/{pet_id}/statistics", summary="获取宠物健康记录统计数据")
def get_health_statistics(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    year: Optional[int] = Query(None, description="统计年份，默认当前年"),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的健康记录统计数据
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    statistics = crud_health_record.get_statistics(
        db,
        pet_id=pet_id,
        year=year
    )
    return statistics
