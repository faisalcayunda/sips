from typing import Optional

from sqlalchemy import select

from app.models import ArticleCommentModel

from .base import BaseRepository


class ArticleCommentRepository(BaseRepository[ArticleCommentModel]):
    def __init__(self, model: type[ArticleCommentModel]):
        super().__init__(model)

    async def find_by_slug(self, slug: str) -> Optional[ArticleCommentModel]:
        query = select(self.model).where(self.model.article_slug == slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
