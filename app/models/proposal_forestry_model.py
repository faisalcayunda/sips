from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, JSON, Column, DateTime, Enum, Float, Integer, String

from app.core.config import settings

from . import Base


class ForestryProposalModel(Base):
    __tablename__ = "forestry"

    id = Column(
        "fore_kps_id",
        Integer,
        primary_key=True,
    )
    regional_id = Column(
        "reg_id",
        CHAR(10),
    )

    assist_account_id = Column("assist_acc_id", JSON, nullable=True)
    name = Column("fore_name", String(256), nullable=True)
    schema_id = Column(
        "fore_skema_id",
        CHAR(4),
    )
    kph_account_id = Column(
        "kph_acc_id",
        CHAR(36),
    )
    kh_id = Column(
        "fore_kh_id",
        JSON,
    )
    area = Column(
        "fore_luas",
        Float(precision=2),
    )
    household_count = Column(
        "fore_jumlah_kk",
        Integer,
    )
    head_name = Column(
        "fore_nama_ketua",
        String(256),
    )
    head_contact = Column(
        "fore_kontak_ketua",
        CHAR(16),
    )
    map_ps = Column(
        "fore_peta_ps",
        String(256),
    )
    pps_id = Column("fore_pps_id", CHAR(11), nullable=True)
    vertex = Column(
        "fore_pps_vertek",
        CHAR(4),
    )
    status = Column("fore_pps_status", CHAR(4), nullable=True)
    nagari_sk = Column(
        "fore_pps_sknagari",
        String(256),
    )
    regent_sk = Column(
        "fore_sk_bupati",
        String(256),
    )
    forestry_sk = Column("fore_sk_menlhk", String(256), nullable=True)
    is_valid = Column("fore_pps_valid", Enum("Y", "N"), default="N")
    request_year = Column(
        "fore_pps_klhk",
        CHAR(4),
    )
    release_year = Column("fore_kps_menlhk", String(256), nullable=True)
    is_kps_valid = Column("fore_kps_valid", Enum("Y", "N"), default="N")
    created_by = Column(
        "create_by",
        CHAR(36),
    )
    updated_by = Column("update_by", CHAR(36), nullable=True)
    created_at = Column(
        "create_at",
        DateTime,
        default=datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_at = Column(
        "update_at",
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )
