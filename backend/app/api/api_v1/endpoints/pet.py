from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_pet import pet as crud_pet
from app.db.session import get_db
from app.models.user import User
from app.schemas.pet import PetCreate, PetResponse, PetUpdate

router = APIRouter()


@router.get("", response_model=List[PetResponse], summary="获取用户的宠物列表")
def read_pets(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前用户的所有宠物列表
    """
    pets = crud_pet.get_by_user_id(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        include_inactive=include_inactive
    )
    return pets


@router.post("", response_model=PetResponse, summary="添加新宠物")
def create_pet(
    *,
    db: Session = Depends(get_db),
    pet_in: PetCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    为当前用户添加新宠物
    """
    pet = crud_pet.create_with_user(
        db,
        obj_in=pet_in,
        user_id=current_user.id
    )
    return pet


@router.get("/{pet_id}", response_model=PetResponse, summary="获取指定宠物详情")
def read_pet(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    根据ID获取指定宠物的详细信息
    """
    pet = crud_pet.get_by_user_and_id(
        db,
        user_id=current_user.id,
        pet_id=pet_id
    )
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    return pet


@router.put("/{pet_id}", response_model=PetResponse, summary="更新宠物信息")
def update_pet(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    pet_in: PetUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新指定宠物的信息
    """
    pet = crud_pet.get_by_user_and_id(
        db,
        user_id=current_user.id,
        pet_id=pet_id
    )
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    pet = crud_pet.update(db, db_obj=pet, obj_in=pet_in)
    return pet


@router.delete("/{pet_id}", summary="删除宠物")
def delete_pet(
    *,
    db: Session = Depends(get_db),
    pet_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    删除指定宠物（软删除）
    """
    pet = crud_pet.get_by_user_and_id(
        db,
        user_id=current_user.id,
        pet_id=pet_id
    )
    
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="宠物不存在"
        )
    
    # 软删除
    pet.is_active = False
    db.add(pet)
    db.commit()
    
    return {"message": "宠物删除成功"}


@router.get("/count", summary="统计用户的宠物数量")
def count_pets(
    *,
    db: Session = Depends(get_db),
    include_inactive: bool = False,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    统计当前用户的宠物数量
    """
    count = crud_pet.count_by_user_id(
        db,
        user_id=current_user.id,
        include_inactive=include_inactive
    )
    
    return {"count": count}
