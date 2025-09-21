from typing import Any, List, Optional, Tuple, override

from fastapi_async_sqlalchemy import db
from sqlalchemy import Sequence, String, cast, func, select
from sqlalchemy.orm import joinedload, selectinload

from app.core.exceptions import NotFoundException
from app.models import ArticleModel, ArticleRatingModel

from .base import BaseRepository


class ArticleRepository(BaseRepository[ArticleModel]):
    def __init__(self, model: type[ArticleModel]):
        super().__init__(model)

    @override
    def build_base_query(self, include_deleted: bool = False):
        """Build base query dengan soft delete handling."""
        query = (
            select(
                self.model.id,
                self.model.title,
                self.model.slug,
                self.model.content,
                self.model.enable,
                self.model.cover,
                self.model.counter,
                func.avg(func.nullif(ArticleRatingModel.rating, None)).label("rating"),
                self.model.created_by,
                self.model.updated_by,
                self.model.created_at,
                self.model.updated_at,
            )
            .outerjoin(
                ArticleRatingModel,
                self.model.id == ArticleRatingModel.article_id,
            )
            .group_by(
                self.model.id,
                self.model.title,
                self.model.slug,
                self.model.content,
                self.model.enable,
                self.model.cover,
                self.model.counter,
                self.model.created_by,
                self.model.updated_by,
                self.model.created_at,
                self.model.updated_at,
            )
        )
        if hasattr(self.model, "is_deleted") and not include_deleted:
            query = query.where(self.model.is_deleted.is_(False))
        return query

    @override
    async def find_all(
        self,
        filters: Optional[List[Any]] = None,
        sort: Optional[List[Any]] = None,
        search: str = "",
        group_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        relationships: Optional[List[str]] = None,
        searchable_columns: Optional[List[str]] = None,
    ) -> Tuple[List[ArticleModel], int]:
        """Optimized find_all method."""

        filters = filters or []
        sort = sort or []
        relationships = relationships or []
        searchable_columns = searchable_columns or []

        query = self.build_base_query().filter(*filters)

        # Optimized search
        if search:
            if searchable_columns:
                search_conditions = [
                    cast(getattr(self.model, col), String).ilike(f"%{search}%")
                    for col in searchable_columns
                    if hasattr(self.model, col)
                ]
            else:
                search_conditions = [
                    cast(getattr(self.model, col_name), String).ilike(f"%{search}%")
                    for col_name in self.inspector.c.keys()
                ]

            if search_conditions:
                query = query.where(or_(*search_conditions))

        if group_by:
            query = query.group_by(getattr(self.model, group_by))

        # Count query
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)
        if total is None:
            total = 0

        # Data query
        if sort:
            query = query.order_by(*sort)
        else:
            query = query.order_by(self.model.id)

        if relationships:
            for rel in relationships:
                if hasattr(self.model, rel):
                    attr = getattr(self.model, rel)
                    if hasattr(attr.property, "collection_class"):
                        query = query.options(selectinload(attr))
                    else:
                        query = query.options(joinedload(attr))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        records_seq: Sequence[ArticleModel] = result.mappings().all()
        records: List[ArticleModel] = list(records_seq)

        return records, total

    @override
    async def find_by_id(self, id: str, relationships: Optional[List[str]] = None) -> Optional[ArticleModel]:
        query = self.build_base_query().filter(self.model.id == id)
        article = await db.session.execute(query)
        article = article.mappings().first()
        if not article:
            raise NotFoundException("Article not found")

        await db.session.execute(
            ArticleModel.__table__.update().where(ArticleModel.id == id).values(counter=ArticleModel.counter + 1)
        )
        await db.session.commit()

        return article

    async def find_by_slug(self, slug: str, relationships: Optional[List[str]] = None) -> Optional[ArticleModel]:
        query = self.build_base_query().filter(self.model.slug == slug)
        article = await db.session.execute(query)
        article = article.mappings().first()

        if not article:
            raise NotFoundException("Article not found")

        await db.session.execute(
            ArticleModel.__table__.update().where(ArticleModel.slug == slug).values(counter=ArticleModel.counter + 1)
        )
        await db.session.commit()
        return article
