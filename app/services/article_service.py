from typing import Any, Dict, override

from app.models import ArticleModel
from app.repositories import ArticleRepository
from app.schemas import UserSchema

from .base import BaseService


class ArticleService(BaseService[ArticleModel, ArticleRepository]):
    def __init__(self, repository: ArticleRepository):
        super().__init__(ArticleModel, repository)

    def _slugify(self, text: str) -> str:
        return text.strip().lower().replace(" ", "-")

    async def find_by_id_or_slug(self, id_or_slug: str) -> ArticleModel | None:
        if id_or_slug.isdigit():
            return await self.repository.find_by_id(id_or_slug)
        else:
            return await self.repository.find_by_slug(id_or_slug)

    @override
    async def create(self, data: Dict[str, Any], current_user: UserSchema) -> ArticleModel:
        data["created_by"] = current_user.id
        data["slug"] = self._slugify(data["title"])
        return await super().create(data)

    @override
    async def update(
        self, id: str, data: Dict[str, Any], current_user: UserSchema, refresh: bool = True
    ) -> ArticleModel:
        data["updated_by"] = current_user.id
        if "title" in data:
            data["slug"] = self._slugify(data["title"])

        return await super().update(id, data, refresh=refresh)
