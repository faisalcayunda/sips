from datetime import datetime

from pytz import timezone
from sqlalchemy import (
    CHAR,
    JSON,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.config import settings

from . import Base


class ForestryProposalModel(Base):
    __tablename__ = "forestry"

    id = Column("fore_kps_id", CHAR(11), primary_key=True, nullable=False)
    regional_id = Column("reg_id", CHAR(10), ForeignKey("regional.reg_id"), nullable=False)

    assist_account_id = Column("assist_acc_id", JSON, nullable=True)
    name = Column("fore_name", String(256), nullable=True)
    schema_id = Column("fore_skema_id", CHAR(4), nullable=False)
    kph_account_id = Column("kph_acc_id", CHAR(36), nullable=False)
    kh_id = Column("fore_kh_id", JSON, nullable=False)
    akps_id = Column("fore_akps_id", CHAR(32), nullable=False)
    area = Column("fore_luas", Float(precision=2), nullable=False)
    household_count = Column("fore_jumlah_kk", Integer, nullable=False)
    head_name = Column("fore_nama_ketua", String(256), nullable=False)
    head_contact = Column("fore_kontak_ketua", CHAR(16), nullable=False)
    map_ps = Column("fore_peta_ps", String(256), nullable=False)
    pps_id = Column("fore_pps_id", CHAR(11), nullable=True)
    vertex = Column("fore_pps_vertek", CHAR(4), nullable=False)
    status = Column("fore_pps_status", CHAR(4), nullable=True)
    nagari_sk = Column("fore_pps_sknagari", String(256), nullable=False)
    regent_sk = Column("fore_sk_bupati", String(256), nullable=False)
    forestry_sk = Column("fore_sk_menlhk", String(256), nullable=False)
    is_valid = Column("fore_pps_valid", Enum("Y", "N"), nullable=False, default="N")
    request_year = Column("fore_pps_klhk", CHAR(4), nullable=False)
    release_year = Column("fore_kps_menlhk", String(256), nullable=True)
    is_kps_valid = Column("fore_kps_valid", Enum("Y", "N"), nullable=False, default="N")
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

    regional = relationship("RegionalModel", lazy="selectin")
