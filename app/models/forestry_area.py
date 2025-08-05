from sqlalchemy import Column, Integer, String

from . import Base


class ForestryAreaModel(Base):
    __tablename__ = "forestry_area"  # Ganti dengan nama tabel aslinya kalau ada

    id = Column("id", Integer, primary_key=True, nullable=False)
    name = Column("name", String(512), nullable=False)
    abbreviation = Column("abbreviation", String(20), nullable=False)
