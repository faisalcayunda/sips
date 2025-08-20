from sqlalchemy import Column, Integer, String

from . import Base


class BusinessHarvestModel(Base):
    __tablename__ = "stat_businesses_prdk_panen"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    harvest_code = Column("id_prdk_panen", String(255), nullable=False)
    name = Column("name_prdk_panen", String(255), nullable=False)
    note = Column("note", String(255), nullable=True)
