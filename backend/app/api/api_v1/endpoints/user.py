from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import get_password_hash, verify_password
from app.crud.crud_user import user as crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserChangePassword, UserResponse, UserUpdate

router = APIRouter()
import logging

logger = logging.getLogger(__name__)


@router.get("/profile", response_model=UserResponse, summary="获取当前用户信息")
def read_user_profile(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    获取当前登录用户的个人信息
    """
    try:
        logger.info(f"获取用户信息: user_id={current_user.id}")
        return current_user
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )


@router.put("/profile", response_model=UserResponse, summary="更新用户信息")
def update_user_profile(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    更新当前登录用户的个人信息
    """
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.put("/password", summary="修改用户密码")
def change_password(
    *,
    db: Session = Depends(get_db),
    password_in: UserChangePassword,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    修改当前登录用户的密码
    """
    # 验证旧密码
    if not verify_password(password_in.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 更新密码
    hashed_password = get_password_hash(password_in.new_password)
    current_user.password_hash = hashed_password
    db.add(current_user)
    db.commit()
    
    return {"message": "密码修改成功"}


@router.get("/{user_id}", response_model=UserResponse, summary="获取指定用户信息")
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    根据用户ID获取用户信息（仅允许用户获取自己的信息）
    """
    user = crud_user.get(db, id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问该用户信息"
        )
    
    return user
