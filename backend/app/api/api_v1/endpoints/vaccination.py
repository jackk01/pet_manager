from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_pet import pet as crud_pet
from app.crud.crud_vaccination import vaccination as crud_vaccination
from app.db.session import get_db
from app.models.user import User
from app.schemas.vaccination import VaccinationCreate, VaccinationResponse, VaccinationUpdate

router = APIRouter()


@router.get("/upcoming", response_model=List[VaccinationResponse], summary="获取即将到期的疫苗提醒")
def get_upcoming_vaccinations(
    *,
    db: Session = Depends(get_db),
    days: int = 30,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户即将到期的疫苗提醒（默认30天内）
    """
    vaccinations = crud_vaccination.get_upcoming_by_user_id(
        db,
        user_id=current_user.id,
        days=days
    )
    return vaccinations


@router.get("/expired", response_model=List[VaccinationResponse], summary="获取已过期的疫苗记录")
def get_expired_vaccinations(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户已过期的疫苗记录
    """
    vaccinations = crud_vaccination.get_expired_by_user_id(
        db,
        user_id=current_user.id
    )
    return vaccinations


@router.get("/pets/{pet_id}", response_model=List[VaccinationResponse], summary="获取指定宠物的疫苗记录")
def read_pet_vaccinations(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取指定宠物的所有疫苗记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    vaccinations = crud_vaccination.get_by_pet_id(
        db,
        pet_id=pet_id,
        skip=skip,
        limit=limit
    )
    return vaccinations


@router.post("/pets/{pet_id}", response_model=VaccinationResponse, summary="为宠物添加疫苗记录")
def create_vaccination(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    vaccination_in: VaccinationCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    为指定宠物添加新的疫苗记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    vaccination = crud_vaccination.create(
        db,
        obj_in=VaccinationCreate(**vaccination_in.dict(), pet_id=pet_id)
    )
    return vaccination


@router.get("/pets/{pet_id}/{record_id}", response_model=VaccinationResponse, summary="获取指定疫苗记录详情")
def read_vaccination(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据ID获取指定疫苗记录的详细信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    vaccination = crud_vaccination.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not vaccination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="疫苗记录不存在"
        )
    
    return vaccination


@router.put("/pets/{pet_id}/{record_id}", response_model=VaccinationResponse, summary="更新疫苗记录")
def update_vaccination(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    vaccination_in: VaccinationUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新指定疫苗记录的信息
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    vaccination = crud_vaccination.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not vaccination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="疫苗记录不存在"
        )
    
    vaccination = crud_vaccination.update(db, db_obj=vaccination, obj_in=vaccination_in)
    return vaccination


@router.delete("/pets/{pet_id}/{record_id}", summary="删除疫苗记录")
def delete_vaccination(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    删除指定疫苗记录
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    vaccination = crud_vaccination.get_by_pet_and_id(
        db,
        pet_id=pet_id,
        record_id=record_id
    )
    
    if not vaccination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="疫苗记录不存在"
        )
    
    crud_vaccination.remove(db, id=record_id)
    return {"message": "疫苗记录删除成功"}


@router.put("/{record_id}/mark-reminded", response_model=VaccinationResponse, summary="标记疫苗记录为已提醒")
def mark_vaccination_reminded(
    *,
    db: Session = Depends(get_db),
    record_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    标记指定疫苗记录为已提醒
    """
    # 验证记录是否属于当前用户
    vaccination = crud_vaccination.get(db, id=record_id)
    if not vaccination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="疫苗记录不存在"
        )
    
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=vaccination.pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作该记录"
        )
    
    vaccination = crud_vaccination.mark_as_reminded(db, record_id=record_id)
    return vaccination


@router.get("/pets/{pet_id}/count", summary="统计宠物的疫苗记录数量")
def count_vaccinations(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计指定宠物的疫苗记录数量
    """
    # 验证宠物是否属于当前用户
    pet = crud_pet.get_by_user_and_id(db, user_id=current_user.id, pet_id=pet_id)
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    count = crud_vaccination.count_by_pet_id(db, pet_id=pet_id)
    return {"count": count}
