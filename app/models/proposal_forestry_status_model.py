from sqlalchemy import CHAR, Column, String, Text

from . import Base


class ProposalforestryStatusModel(Base):
    __tablename__ = "stat_forestry_pps_proses"

    id = Column("id_pps_status", String(255), primary_key=True, nullable=False)
    name = Column("nama_proses_pps", String(255), nullable=False)
    proposal_forestry_vertex = Column("fore_pps_vertek", CHAR(4), nullable=False)
    description = Column("keterangan", Text, nullable=True)
