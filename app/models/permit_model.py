from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, JSON, Column, DateTime, Integer

from app.core.config import settings

from . import Base


class PermitModel(Base):
    __tablename__ = "user_permission"

    id = Column("permit_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    role_id = Column("role_id", Integer, nullable=False)
    navigation_id = Column("nav_id", Integer, nullable=False)
    permit_content = Column("permit_desc", JSON, nullable=False)
    created_by = Column("create_by", CHAR(36), nullable=False)
    updated_by = Column("update_by", CHAR(36), nullable=True)
    created_at = Column(
        "create_at",
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_at = Column(
        "update_at",
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )
