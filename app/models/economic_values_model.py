from sqlalchemy import Column, Double, Integer, String, Text
from sqlalchemy.dialects.mysql import YEAR

from .base import Base


class EconomicValueModel(Base):
    __tablename__ = "economic_values"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    kps_id = Column("kps_id", Integer, nullable=False)
    kups_id = Column("kups_id", Integer, nullable=False)
    group_name = Column("kelompok", String(255), nullable=False)
    year = Column("tahun", YEAR, nullable=False)
    commodity_id = Column("komoditas_id", Integer, nullable=False)
    production = Column("produksi", Double, nullable=False)
    value = Column("nilai_ekonomi", Double, nullable=False)
    note = Column("keterangan", Text, nullable=True)
