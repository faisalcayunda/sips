from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Enum, Integer, SmallInteger, String

from app.core.config import settings

from . import Base


class NavigationModel(Base):
    __tablename__ = "core_navigation"  # Ganti dengan nama tabel aslinya

    id = Column("nav_id", Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("nav_name", String(128), nullable=False)
    parent = Column("nav_parent", SmallInteger, nullable=True)
    is_enabled = Column("nav_enable", Enum("Y", "N"), nullable=False)
    icon = Column("nav_icon", String(128), nullable=True)
    url = Column("nav_url", String(128), nullable=True)
    sort_order = Column("nav_sort", Integer, nullable=True)
    sign = Column("nav_sign", String(128), nullable=True)
    created_by = Column("create_by", CHAR(36), nullable=True)
    updated_by = Column("update_by", CHAR(36), nullable=True)
    created_at = Column(
        "create_at",
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_at = Column("update_at", DateTime, nullable=True)
