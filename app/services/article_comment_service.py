from typing import override

from app.core.exceptions import NotFoundException
from app.models import ArticleCommentModel
from app.repositories import ArticleCommentRepository

from .base import BaseService


class ArticleCommentService(BaseService[ArticleCommentModel, ArticleCommentRepository]):
    def __init__(self, repository: ArticleCommentRepository):
        super().__init__(ArticleCommentModel, repository)

    @override
    async def create(self, data: dict) -> ArticleCommentModel:
        article = await self.repository.find_by_slug(data["article_slug"])
        if not article:
            raise NotFoundException("Article not found")

        data["article_id"] = article.id

        return await self.repository.create(data)

    @override
    async def update(self, id: str, data: dict, refresh: bool = True) -> ArticleCommentModel:
        article = await self.repository.find_by_slug(data["article_slug"])
        if not article:
            raise NotFoundException("Article not found")

        if "article_id" not in data:
            data["article_id"] = article.id

        return await self.repository.update(id, data, refresh=refresh)
