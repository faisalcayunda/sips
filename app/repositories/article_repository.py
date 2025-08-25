from typing import List, Optional, override

from app.models import ArticleModel

from .base import BaseRepository


class ArticleRepository(BaseRepository[ArticleModel]):
    def __init__(self, model):
        super().__init__(model)

    @override
    async def find_by_id(self, id: str, relationships: Optional[List[str]] = None) -> Optional[ArticleModel]:
        article = await super().find_by_id(id, relationships)

        await self.update(id, {"counter": article.counter + 1})
        return article
