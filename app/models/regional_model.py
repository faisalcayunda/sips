from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, String

from app.core.config import settings

from . import Base


class RegionalModel(Base):
    __tablename__ = "regional"  # Ganti dengan nama tabel aslinya kalau ada

    id = Column("reg_id", CHAR(36), primary_key=True, nullable=False)
    name = Column("reg_name", String(512), nullable=False)
    parent = Column("reg_parent", CHAR(36), nullable=False)
    group = Column("reg_group", String(50), nullable=False)
    create_by = Column(CHAR(36), nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now(timezone(settings.TIMEZONE)))
