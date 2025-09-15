from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Integer, String

from app.core.config import settings

from . import Base


class BusinessServiceModel(Base):
    __tablename__ = "businesses_service"

    # Primary key
    id = Column(
        "jasa_id",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    # Identifiers
    business_id = Column(
        "kups_id",
        CHAR(13),
    )  # CHAR(13)
    commodity_id = Column(
        "komoditas_id",
        Integer,
    )  # INT

    # Basic info
    name = Column(
        "jasa_nama",
        String(256),
    )  # VARCHAR(256)
    latitude = Column(
        "jasa_latitude",
        String(256),
    )
    longitude = Column(
        "jasa_longitude",
        String(256),
    )

    visitor_type_id = Column(
        "jasa_tipe_pengunjung_id",
        CHAR(4),
    )
    origin_visitor_id = Column(
        "jasa_asal_pengunjung_id",
        CHAR(4),
    )

    # Pricing
    ticket_price = Column(
        "jasa_harga_tiket_hari",
        Integer,
    )
    parking_fee = Column(
        "jasa_harga_sewa_parkir",
        Integer,
    )
    other_item_price = Column(
        "jasa_harga_item_lain",
        Integer,
    )

    # Additional info
    additional_info = Column(
        "jasa_keterangan_item_lain",
        String(256),
        nullable=True,
    )

    # Audit
    created_by = Column(
        "create_by",
        CHAR(16),
    )
    created_at = Column(
        "create_at",
        DateTime,
        default=lambda: datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_by = Column(
        "update_by",
        CHAR(16),
        nullable=True,
    )
    updated_at = Column(
        "update_at",
        DateTime,
        default=lambda: datetime.now(timezone(settings.TIMEZONE)),
        onupdate=lambda: datetime.now(timezone(settings.TIMEZONE)),
    )
