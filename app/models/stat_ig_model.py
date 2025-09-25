from sqlalchemy import Column, Integer, String

from . import Base


class StatIGModel(Base):
    __tablename__ = "stat_data_IG"
    id = Column("id_IG", String(255), primary_key=True)
    id_spatial = Column("id_spatial", Integer, nullable=False, index=True)
