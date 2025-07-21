from datetime import datetime
from typing import Optional

from .base import BaseSchema


class Token(BaseSchema):
    access_token: str
    refresh_token: str
    expires_at: float
    token_type: str = "bearer"


class TokenPayload(BaseSchema):
    sub: Optional[str] = None
    exp: Optional[datetime] = None
    type: Optional[str] = None


class RefreshTokenSchema(BaseSchema):
    refresh_token: str
