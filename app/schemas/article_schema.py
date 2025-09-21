from datetime import datetime
from typing import Optional

from .base import BaseSchema


class ArticleSchema(BaseSchema):
    id: int
    title: str
    slug: str
    content: str
    enable: str
    cover: Optional[str] = None
    counter: Optional[int] = None
    rating: Optional[float] = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None


class ArticleCreateSchema(BaseSchema):
    title: str
    content: str
    enable: str
    cover: Optional[str] = None
    counter: Optional[int] = None


class ArticleUpdateSchema(BaseSchema):
    title: Optional[str] = None
    content: Optional[str] = None
    enable: Optional[str] = None
    cover: Optional[str] = None
    counter: Optional[int] = None
