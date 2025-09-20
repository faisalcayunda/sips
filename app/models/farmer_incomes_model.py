from sqlalchemy import Column, Double, Integer
from sqlalchemy.dialects.mysql import YEAR

from .base import Base


class IncomeModel(Base):
    __tablename__ = "pendapatan"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    year = Column("tahun", YEAR, nullable=False)
    income = Column("pendapatan", Integer, nullable=False)
    difference = Column("selisih", Integer, nullable=False)
    percentage = Column("persen", Double, nullable=False)
