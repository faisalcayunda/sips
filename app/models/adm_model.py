from sqlalchemy import Column, String

from .base import Base


class AdmModel(Base):
    __tablename__ = "adm"
    reg_id = Column(String(10), primary_key=True, nullable=False, index=True)  # char(10)
    id_dagri = Column(String(20), nullable=False)  # varchar(20)
    nama_nagdeskel = Column(String(255), nullable=False)  # varchar(255)
    id_kec = Column(String(10), nullable=False)  # char(10)
    nama_kec = Column(String(255), nullable=False)  # varchar(255)
    id_kab = Column(String(10), nullable=False)  # char(10)
    nama_kab = Column(String(255), nullable=False)  # varchar(255)
    id_prov = Column(String(255), nullable=False)  # varchar(255)
    nama_prov = Column(String(255), nullable=False)  # varchar(255)
