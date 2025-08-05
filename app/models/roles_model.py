from sqlalchemy import Column, Integer, String

from . import Base


class RolesModel(Base):
    __tablename__ = "role_users"

    id = Column("id", Integer, primary_key=True, nullable=False, index=True)
    name = Column("name", String(255), nullable=False)
