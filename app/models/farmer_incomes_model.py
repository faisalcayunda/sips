from sqlalchemy import Column, Double, Integer
from sqlalchemy.dialects.mysql import YEAR

from .base import Base


class FarmerIncomesModel(Base):
    __tablename__ = "farmer_incomes"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    year = Column("tahun", YEAR, nullable=False)
    increase_percentage = Column("persen_peningkatan", Double, nullable=False)
