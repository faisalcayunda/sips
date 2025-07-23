from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Integer, String

from app.core.config import settings

from .base import Base


class AttachmentModel(Base):
    __tablename__ = "attachment"  # Ganti dengan nama tabel sebenarnya

    id = Column("attach_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("attach_name", String(128), nullable=False)
    attach_string = Column("attach_string", String(256), nullable=False)
    attach_type = Column("attach_type", CHAR(4), nullable=False)
    attach_sign = Column("attach_sign", CHAR(16), nullable=False)
    created_by = Column("create_by", CHAR(36), nullable=False)
    created_at = Column(
        "create_at",
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_by = Column("update_by", CHAR(36), nullable=True)
    updated_at = Column(
        "update_at",
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )
