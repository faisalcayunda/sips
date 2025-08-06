from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.navigation_schema import (
    NavigationCreateSchema,
    NavigationSchema,
    NavigationUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import NavigationService

router = APIRouter()


@router.get(
    "/navigations",
    response_model=PaginatedResponse[NavigationSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_navigation_list(
    params: CommonParams = Depends(),
    service: NavigationService = Depends(Factory().get_navigation_service),
) -> PaginatedResponse[NavigationSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    navigations, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[NavigationSchema.model_validate(navigation) for navigation in navigations],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/navigations/{id}", response_model=NavigationSchema)
async def get_navigation(
    id: str,
    service: NavigationService = Depends(Factory().get_navigation_service),
) -> Any | NavigationSchema:
    return await service.find_by_id(id)


@router.post(
    "/navigations",
    response_model=NavigationSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_navigation(
    data: NavigationCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: NavigationService = Depends(Factory().get_navigation_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/navigations/{id}",
    response_model=NavigationSchema,
)
async def update_navigation(
    id: str,
    data: NavigationUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: NavigationService = Depends(Factory().get_navigation_service),
):
    return await service.update(id, data.dict(exclude_unset=True), current_user)


@router.delete(
    "/navigations/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_navigation(
    id: str,
    service: NavigationService = Depends(Factory().get_navigation_service),
):
    await service.delete(id)
