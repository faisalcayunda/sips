from datetime import datetime

from pytz import timezone
from sqlalchemy import CHAR, BigInteger, Column, DateTime, Enum, Integer, String, Text

from app.core.config import settings

from .base import Base


class ArticleModel(Base):
    __tablename__ = "articles"
    id = Column("article_id", Integer, primary_key=True, autoincrement=True, nullable=False)

    title = Column("article_title", String(128), nullable=False)
    slug = Column("article_slug", String(256), nullable=False, index=True)

    content = Column("article_content", Text, nullable=False)

    enable = Column(
        "article_enable",
        Enum("Y", "N", name="article_enable_enum"),
        nullable=False,
    )

    cover = Column("article_cover", String(128), nullable=True)
    counter = Column("article_counter", BigInteger, default=0, nullable=True)

    created_by = Column("create_by", CHAR(16), nullable=False)
    updated_by = Column("update_by", CHAR(16), nullable=True)

    created_at = Column("create_at", DateTime, default=datetime.now(timezone(settings.TIMEZONE)))
    updated_at = Column("update_at", DateTime, onupdate=datetime.now(timezone(settings.TIMEZONE)), nullable=True)
