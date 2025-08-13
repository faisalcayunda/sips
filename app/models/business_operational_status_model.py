from sqlalchemy import CHAR, Column, Integer, String

from . import Base


class BusinessOperationalStatusModel(Base):
    __tablename__ = "stat_businesses_operational"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column("operational_name", String(255), nullable=False)
    type = Column("id_operational", CHAR(4), nullable=False)
    notes = Column("notes", String(255), nullable=True)
