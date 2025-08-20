from sqlalchemy import CHAR, Column, Enum, Integer, String, Text

from . import Base


class CommodityModel(Base):
    __tablename__ = "komoditas"

    id = Column(
        "komoditas_id",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        "komoditas_nama",
        String(256),
    )
    local_name = Column("komoditas_lokal", String(256), nullable=True)
    latin_name = Column("komoditas_latin", String(256), nullable=True)

    type_code = Column("komoditas_jenis", CHAR(8))
    description = Column("komoditas_desc", Text, nullable=True)
    photo = Column("komoditas_photo", String(256), nullable=True)

    status = Column("komoditas_status", Enum("Y", "N"))
