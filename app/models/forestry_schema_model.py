from sqlalchemy import Column, Integer, String

from . import Base


class forestrySchemaModel(Base):
    __tablename__ = "stat_forestry_skema"  # Ganti dengan nama tabel sebenarnya

    id = Column("id_skem", String(11), primary_key=True, nullable=False)
    schema_id = Column("id_skema", String(255), nullable=False)
    name = Column("nama_skema", String(255), nullable=False)
    description = Column("keterangan", String(255), nullable=True)
    ord = Column(Integer, nullable=True)
