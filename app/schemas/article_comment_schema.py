from datetime import datetime
from typing import Optional

from .base import BaseSchema


class ArticleCommentSchema(BaseSchema):
    id: int
    article_slug: str
    comment: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ArticleCommentCreateSchema(BaseSchema):
    article_slug: str
    comment: Optional[str] = None


class ArticleCommentUpdateSchema(BaseSchema):
    article_slug: Optional[str] = None
    comment: Optional[str] = None
