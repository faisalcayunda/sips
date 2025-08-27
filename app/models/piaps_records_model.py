from sqlalchemy import Column, Double, Integer, String

from .base import Base


class PiapsRecordsModel(Base):
    __tablename__ = "piaps_records"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    kph_id = Column("id_kph", Integer, nullable=False)
    kph_name = Column("name_kph", String(255), nullable=False)
    allocation = Column("alokasi_piaps", Double, nullable=False)
    achievement = Column("capaian_piaps", Double, nullable=False)
