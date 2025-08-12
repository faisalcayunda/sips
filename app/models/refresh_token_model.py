from datetime import datetime

from pytz import timezone
from sqlalchemy import BigInteger, Boolean, Column, DateTime, String

from app.core.config import settings

from . import Base


class RefreshTokenModel(Base):
    __tablename__ = "tokens"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        String(36),
        nullable=False,
        index=True,
    )
    token = Column(String(255), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=True, server_default="0")
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone(settings.TIMEZONE)))
