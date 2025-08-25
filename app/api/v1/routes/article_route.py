from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    ArticleCreateSchema,
    ArticleSchema,
    ArticleUpdateSchema,
    UserSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import ArticleService

router = APIRouter()


@router.get("/articles", response_model=PaginatedResponse[ArticleSchema])
async def get_articles(
    params: CommonParams = Depends(),
    service: ArticleService = Depends(ServiceFactory().get_article_service),
) -> PaginatedResponse[ArticleSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    articles, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ArticleSchema.model_validate(article) for article in articles],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/articles/{id}", response_model=ArticleSchema)
async def get_article(
    id: str,
    service: ArticleService = Depends(ServiceFactory().get_article_service),
) -> Any | ArticleSchema:
    return await service.find_by_id(id)


@router.post("/articles", response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
async def create_article(
    data: ArticleCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ArticleService = Depends(ServiceFactory().get_article_service),
):
    return await service.create(data.model_dump(), current_user=current_user)


@router.patch("/articles/{id}", response_model=ArticleSchema)
async def update_article(
    id: str,
    data: ArticleUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ArticleService = Depends(ServiceFactory().get_article_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True), current_user)


@router.delete(
    "/articles/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_article(
    id: str,
    service: ArticleService = Depends(ServiceFactory().get_article_service),
):
    await service.delete(id)
