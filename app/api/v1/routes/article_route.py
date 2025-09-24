from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    ArticleCommentSchema,
    ArticleCreateSchema,
    ArticleRatingCreateSchema,
    ArticleRatingSchema,
    ArticleRatingUpdateSchema,
    ArticleSchema,
    ArticleUpdateSchema,
    UserSchema,
)
from app.schemas.article_comment_schema import ArticleCommentUpdateSchema
from app.schemas.article_rating_schema import ArticleRatingSchema
from app.schemas.base import PaginatedResponse
from app.services import ArticleCommentService, ArticleRatingService, ArticleService

router = APIRouter()


@router.get("/articles/ratings", response_model=PaginatedResponse[ArticleRatingSchema])
async def get_rating_list(
    params: CommonParams = Depends(),
    service: ArticleRatingService = Depends(ServiceFactory().get_article_rating_service),
) -> PaginatedResponse[ArticleRatingSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    rating_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse[ArticleRatingSchema](
        items=[ArticleRatingSchema.model_validate(rating) for rating in rating_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/articles/ratings/{id}", response_model=ArticleRatingSchema)
async def get_rating(
    id: str,
    service: ArticleRatingService = Depends(ServiceFactory().get_article_rating_service),
) -> Any | ArticleRatingSchema:
    return await service.find_by_slug(id)


@router.post(
    "/articles/ratings",
    response_model=ArticleRatingSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_rating(
    data: ArticleRatingCreateSchema,
    service: ArticleRatingService = Depends(ServiceFactory().get_article_rating_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/articles/ratings/{id}",
    response_model=ArticleRatingSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_rating(
    id: str,
    data: ArticleRatingUpdateSchema,
    service: ArticleRatingService = Depends(ServiceFactory().get_article_rating_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/articles/ratings/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_rating(
    id: str,
    service: ArticleRatingService = Depends(ServiceFactory().get_article_rating_service),
):
    await service.delete(id)


@router.get("/articles/comments", response_model=PaginatedResponse[ArticleCommentSchema])
async def get_comment_list(
    params: CommonParams = Depends(),
    service: ArticleCommentService = Depends(ServiceFactory().get_article_comment_service),
) -> PaginatedResponse[ArticleCommentSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    rating_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse[ArticleCommentSchema](
        items=[ArticleCommentSchema.model_validate(rating) for rating in rating_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/articles/comments/{id}", response_model=ArticleCommentSchema)
async def get_comment(
    id: str,
    service: ArticleCommentService = Depends(ServiceFactory().get_article_comment_service),
) -> Any | ArticleCommentSchema:
    return await service.find_by_slug(id)


@router.post(
    "/articles/comments",
    response_model=ArticleCommentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: ArticleCommentSchema,
    service: ArticleCommentService = Depends(ServiceFactory().get_article_comment_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/articles/comments/{id}",
    response_model=ArticleCommentSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_comment(
    id: str,
    data: ArticleCommentUpdateSchema,
    service: ArticleCommentService = Depends(ServiceFactory().get_article_comment_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True))


@router.delete(
    "/articles/comments/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_comment(
    id: str,
    service: ArticleCommentService = Depends(ServiceFactory().get_article_comment_service),
):
    await service.delete(id)


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
    return await service.find_by_id_or_slug(id)


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
