from typing import Optional

from sqlalchemy import select

from app.models import ArticleRatingModel

from .base import BaseRepository


class ArticleRatingRepository(BaseRepository[ArticleRatingModel]):
    def __init__(self, model: type[ArticleRatingModel]):
        super().__init__(model)

    async def find_by_slug(self, slug: str) -> Optional[ArticleRatingModel]:
        query = select(self.model).where(self.model.article_slug == slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
