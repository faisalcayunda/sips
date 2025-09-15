from typing import override

from app.core.exceptions import NotFoundException
from app.models import ArticleRatingModel
from app.repositories import ArticleRatingRepository

from .base import BaseService


class ArticleRatingService(BaseService[ArticleRatingModel, ArticleRatingRepository]):
    def __init__(self, repository: ArticleRatingRepository):
        super().__init__(ArticleRatingModel, repository)

    @override
    async def create(self, data: dict) -> ArticleRatingModel:
        article = await self.repository.find_by_slug(data["article_slug"])
        if not article:
            raise NotFoundException("Article not found")

        data["article_id"] = article.id

        return await self.repository.create(data)

    @override
    async def update(self, id: str, data: dict, refresh: bool = True) -> ArticleRatingModel:
        article = await self.repository.find_by_slug(data["article_slug"])
        if not article:
            raise NotFoundException("Article not found")

        if "article_id" not in data:
            data["article_id"] = article.id

        return await self.repository.update(id, data, refresh=refresh)

    async def find_by_slug(self, slug: str) -> ArticleRatingModel:
        return await self.repository.find_by_slug(slug)
