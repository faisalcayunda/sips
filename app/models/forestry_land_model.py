from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Float, Integer
from sqlalchemy.dialects.mysql import YEAR

from app.core.config import settings

from .base import Base


class ForestryLandModel(Base):
    __tablename__ = "forestry_land"  # Ganti dengan nama tabel aslinya

    id = Column("land_id", Integer, primary_key=True, nullable=False, autoincrement=True)
    forestry_proposal_id = Column("fore_kps_id", CHAR(36), nullable=False)
    year = Column("land_year", YEAR, nullable=False)  # YEAR di MySQL biasanya Integer di SQLAlchemy
    area = Column("land_area", Float, nullable=False)
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
