from sqlalchemy import Column, String

from . import Base


class AdmModel(Base):
    __tablename__ = "adm"
    reg_id = Column(String(10), primary_key=True, nullable=False, index=True)
    id_dagri = Column(String(20), nullable=False)
    nama_nagasek = Column(String(255), nullable=False)
    id_kec = Column(String(10), nullable=False)
    nama_kec = Column(String(255), nullable=False)
    id_kab = Column(String(10), nullable=False)
    nama_kab = Column(String(255), nullable=False)
    id_prov = Column(String(10), nullable=False)
    nama_prov = Column(String(255), nullable=False)
