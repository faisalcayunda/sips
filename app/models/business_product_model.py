from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Float, Integer, String, Text

from app.core.config import settings

from . import Base


class BusinessProductModel(Base):
    __tablename__ = "businesses_product"

    # Primary key
    id = Column(
        "prdk_id",
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
        "prdk_nama",
        String(256),
    )  # VARCHAR(256)
    description = Column(
        "prdk_desc",
        Text,
    )  # TEXT
    beneficiary_count = Column(
        "prdk_penerima_manfaat",
        Integer,
    )

    # Location / codes
    manufacture_code = Column(
        "prdk_made_id",
        CHAR(4),
    )  # CHAR(4)
    latitude = Column(
        "prdk_latitude",
        String(256),
    )
    longitude = Column(
        "prdk_longitude",
        String(256),
    )

    # Areas (numeric)
    area_managed = Column(
        "prdk_area_kelolaan",
        Float,
    )
    area_planned = Column(
        "prdk_area_rencana",
        Float,
    )

    # Areas (text)
    area_productive = Column(
        "prdk_area_produktif",
        String(256),
    )
    area_unit = Column(
        "prdk_area_satuan",
        String(256),
    )

    # Harvest
    harvest_production = Column(
        "prdk_panen_produksi",
        String(256),
    )
    harvest_unit = Column(
        "prdk_panen_satuan",
        String(128),
    )
    harvest_id = Column(
        "prdk_panen_id",
        CHAR(4),
    )  # CHAR(4)

    # Classification
    type_id = Column(
        "prdk_jenis_id",
        CHAR(4),
    )  # CHAR(4)

    # Tools
    tools_available = Column(
        "prdk_alat_tersedia",
        String(256),
    )
    tools_detail = Column(
        "prdk_alat_ntersedia",
        String(256),
    )

    # Pricing & buyers
    price_sell = Column(
        "prdk_harga_jual",
        Integer,
    )
    buyer_type_id = Column(
        "prdk_pembeli_id",
        CHAR(4),
    )  # CHAR(4)
    buyer_count = Column(
        "prdk_pembeli_jumlah",
        Integer,
    )
    sales_freq_id = Column(
        "prdk_penjualan_id",
        CHAR(4),
    )  # CHAR(4)

    # Export
    export_status_id = Column(
        "prdk_export_id",
        CHAR(4),
    )  # CHAR(4)
    export_purpose = Column(
        "prdk_export_tujuan",
        String(256),
    )

    # Misc
    seedstock_availability = Column("prdk_ketersediaan_bibit_bahan_baku", String(256), nullable=True)
    unit_price_label = Column("prdk_satuan_harga_jual", String(256), nullable=True)
    unit_sold_label = Column("prdk_satuan_produk_terjual", String(256), nullable=True)
    buyer_target = Column("prdk_pembeli_target", String(256), nullable=True)

    # Audit
    created_by = Column(
        "create_by",
        CHAR(16),
    )  # CHAR(16)
    created_at = Column(
        "create_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone(settings.TIMEZONE)),
    )
    updated_by = Column("update_by", CHAR(16), nullable=True)  # CHAR(16)
    updated_at = Column(
        "update_at",
        nullable=True,
        default=lambda: datetime.now(timezone(settings.TIMEZONE)),
        onupdate=lambda: datetime.now(timezone(settings.TIMEZONE)),
    )
