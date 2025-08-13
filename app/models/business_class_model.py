from sqlalchemy import Column, Integer, String

from . import Base


class BusinessClassModel(Base):
    __tablename__ = "stat_businesses_class"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column("nama_kelas_kups", String(64), nullable=False)
    type = Column("id_kelas", String(8), nullable=False)
    description = Column("keterangan", String(255), nullable=True)
