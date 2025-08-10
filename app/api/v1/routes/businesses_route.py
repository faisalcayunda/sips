from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.businesses_schema import (
    BusinessesCreateSchema,
    BusinessesSchema,
    BusinessesUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import BusinessesService

router = APIRouter()


@router.get("/businesses", response_model=PaginatedResponse[BusinessesSchema])
async def get_businesses(
    params: CommonParams = Depends(),
    service: BusinessesService = Depends(Factory().get_businesses_service),
) -> PaginatedResponse[BusinessesSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    businesses, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[BusinessesSchema.model_validate(business) for business in businesses],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/businesses/{id}", response_model=BusinessesSchema)
async def get_business(
    id: str,
    service: BusinessesService = Depends(Factory().get_businesses_service),
) -> Any | BusinessesSchema:
    return await service.find_by_id(id)


@router.post("/businesses", response_model=BusinessesSchema, status_code=status.HTTP_201_CREATED)
async def create_business(
    data: BusinessesCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    return await service.create(data.model_dump(), current_user=current_user)


@router.patch("/businesses/{id}", response_model=BusinessesSchema)
async def update_business(
    id: str,
    data: BusinessesUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True), current_user)


@router.delete(
    "/businesses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_business(
    id: str,
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    await service.delete(id)
