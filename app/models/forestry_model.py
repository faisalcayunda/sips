from sqlalchemy import CHAR, Column, Float, Integer, String

from . import Base


class PiapsModel(Base):
    __tablename__ = "piaps"

    id = Column("Id_piaps", Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column("Nama_KPH", String(128), nullable=False)
    acc_id = Column(CHAR(36), nullable=False)
    area = Column("Luas_piaps", Float, nullable=False)
    notes = Column("Ket_piaps", String(100), nullable=True)
