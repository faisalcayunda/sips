from datetime import datetime

from pytz import timezone
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.config import settings

from . import Base


class FileModel(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), nullable=False, index=True)
    object_name = Column(String(512), nullable=False, unique=True)
    content_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1024), nullable=False)
    try:
        user_id = Column(String(36), ForeignKey("user_account.acc_id"), nullable=False)
    except Exception:
        user_id = None
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone(settings.TIMEZONE)))
    modified_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone(settings.TIMEZONE)),
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
    )

    uploaded_by = relationship("UserModel", lazy="selectin", uselist=False)
