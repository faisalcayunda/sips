from typing import List, Optional, override

from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from app.core.exceptions import NotFoundException
from app.models import ArticleModel

from .base import BaseRepository


class ArticleRepository(BaseRepository[ArticleModel]):
    def __init__(self, model: type[ArticleModel]):
        super().__init__(model)

    @override
    async def find_by_id(self, id: str, relationships: Optional[List[str]] = None) -> Optional[ArticleModel]:
        article = await db.session.scalar(select(ArticleModel).filter(ArticleModel.id == id))
        if not article:
            raise NotFoundException("Article not found")

        article.counter += 1
        await db.session.commit()
        return article

    @override
    async def find_by_slug(self, slug: str, relationships: Optional[List[str]] = None) -> Optional[ArticleModel]:
        article = await db.session.scalar(select(ArticleModel).filter(ArticleModel.slug == slug))
        if not article:
            raise NotFoundException("Article not found")

        article.counter += 1
        await db.session.commit()
        return article
