from sqlalchemy import Column, Integer

from . import Base


class StatIGModel(Base):
    __tablename__ = "stat_data_IG"
    id = Column("id_IG", Integer, primary_key=True, nullable=False, index=True)
    id_spatial = Column("id_spatial", Integer, nullable=False, index=True)
