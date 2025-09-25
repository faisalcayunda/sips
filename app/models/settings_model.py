from tokenize import String

from sqlalchemy import Column
from sqlalchemy.types import JSON

from . import Base


class SettingsModel(Base):
    __tablename__ = "settings"

    key = Column(String(128), primary_key=True, unique=True, nullable=False, index=True)
    value = Column(JSON, nullable=True)
    description = Column(String(256), nullable=True)
