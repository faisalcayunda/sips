from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, Column, DateTime, Enum, Integer, String

from app.core.config import settings
from app.models.base import Base


class BusinessesModel(Base):
    """
    Model untuk tabel businesses (KUPS - Kelompok Usaha Perhutanan Sosial)
    """

    __tablename__ = "businesses"

    # Primary Key
    id = Column("kups_id", CHAR(36), primary_key=True, index=True, comment="ID unik KUPS")

    # Status dan informasi dasar
    status = Column(
        "kups_status",
        Enum("Y", "N", name="kups_status_enum"),
        nullable=False,
        default="Y",
        comment="Status aktif KUPS",
    )
    name = Column("kups_nama", String(256), nullable=False, comment="Nama KUPS")

    # Foreign key ke forestry area
    forestry_area_id = Column(
        "fore_kps_id", CHAR(11), nullable=False, index=True, comment="ID kawasan perhutanan sosial"
    )

    # Informasi legal dan pembentukan
    sk_number = Column("kups_sk_no", String(128), nullable=False, comment="Nomor SK pembentukan")
    establishment_year = Column("kups_pembentukan", Integer, nullable=False, comment="Tahun pembentukan")
    member_count = Column("kups_anggota", Integer, nullable=False, comment="Jumlah anggota")

    # Informasi ketua
    chairman_name = Column("kups_nama_ketua", String(128), nullable=False, comment="Nama ketua KUPS")
    chairman_contact = Column("kups_kontak_ketua", CHAR(16), nullable=False, comment="Kontak ketua")

    # Informasi akun dan lokasi
    account_id = Column("kups_acc_id", String(256), nullable=False, comment="ID akun")
    latitude = Column("kups_latitude", String(256), nullable=False, comment="Latitude lokasi")
    longitude = Column("kups_longitude", String(256), nullable=False, comment="Longitude lokasi")

    # Informasi modal dan operasional
    capital_id = Column("kups_modal_id", CHAR(128), nullable=False, comment="ID modal")
    operational_status_id = Column("kups_status_op_id", CHAR(4), nullable=False, comment="ID status operasional")
    operational_period_id = Column("kups_lama_op_id", CHAR(4), nullable=False, comment="ID lama operasional")
    class_id = Column("kups_kelas_id", CHAR(4), nullable=False, comment="ID kelas")

    # Status validasi
    is_validated = Column(
        "kups_valid", Enum("Y", "N", name="kups_valid_enum"), nullable=False, default="N", comment="Status validasi"
    )

    # Informasi modal (opsional)
    capital_provider_name = Column("kups_nama_pemberi_modal", String(256), nullable=True, comment="Nama pemberi modal")
    capital_provision_type = Column(
        "kups_bentuk_pemberian_modal", String(256), nullable=True, comment="Bentuk pemberian modal"
    )
    capital_provision_type_other = Column(
        "kups_bentuk_pemberian_modal_lain", String(256), nullable=True, comment="Bentuk pemberian modal lainnya"
    )
    capital_repayment_period = Column(
        "kups_jangka_waktu_pelunasan", Integer, nullable=True, comment="Jangka waktu pelunasan modal"
    )

    # Audit fields
    created_by = Column("create_by", CHAR(36), nullable=False, comment="User yang membuat record")
    updated_by = Column("update_by", CHAR(36), nullable=False, comment="User yang mengupdate record")
    created_at = Column(
        "create_at",
        DateTime,
        nullable=False,
        default=datetime.now(timezone(settings.TIMEZONE)),
        comment="Waktu pembuatan record",
    )
    updated_at = Column(
        "update_at",
        DateTime,
        nullable=True,
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
        comment="Waktu update record",
    )

    def __repr__(self):
        return f"<BusinessesModel(id='{self.id}', name='{self.name}')>"
