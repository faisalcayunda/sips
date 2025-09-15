from datetime import datetime
from typing import Optional

from .base import BaseSchema


class ArticleRatingSchema(BaseSchema):
    id: int
    article_slug: str
    rating: int
    comment: Optional[str] = None
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ArticleRatingCreateSchema(BaseSchema):
    article_slug: str
    rating: int
    comment: Optional[str] = None


class ArticleRatingUpdateSchema(BaseSchema):
    rating: Optional[int] = None
    comment: Optional[str] = None
