from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    用户CRUD操作类
    """
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        根据用户名获取用户
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        根据邮箱获取用户
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username_or_email(self, db: Session, *, username: str) -> Optional[User]:
        """
        根据用户名或邮箱获取用户
        """
        return db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        创建用户
        """
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            nickname=obj_in.nickname if obj_in.nickname else obj_in.username,
            phone=obj_in.phone
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        """
        用户认证
        """
        user = self.get_by_username_or_email(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """
        检查用户是否激活
        """
        return user.is_active


user = CRUDUser(User)
