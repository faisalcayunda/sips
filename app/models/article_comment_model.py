from datetime import datetime

from pytz import timezone
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.config import settings

from .base import Base


class ArticleCommentModel(Base):
    __tablename__ = "article_comments"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    article_id = Column("article_id", Integer, nullable=False, index=True)
    article_slug = Column("article_slug", String(256), nullable=False, index=True)
    comment = Column("comment", Text, nullable=True)

    created_at = Column(
        "created_at",
        DateTime,
        default=datetime.now(timezone(settings.TIMEZONE)),
        nullable=False,
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        onupdate=datetime.now(timezone(settings.TIMEZONE)),
        nullable=True,
    )
