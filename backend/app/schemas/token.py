from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    令牌返回模型
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """
    令牌负载模型
    """
    sub: int
    exp: datetime
    type: Optional[str] = None
