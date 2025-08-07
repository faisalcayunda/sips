from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.forestry_land_schema import (
    ForestryLandCreateSchema,
    ForestryLandSchema,
    ForestryLandUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import ForestryLandService

router = APIRouter()


@router.get("/forestry-land", response_model=PaginatedResponse[ForestryLandSchema])
async def get_land_list(
    params: CommonParams = Depends(),
    service: ForestryLandService = Depends(Factory().get_forestry_land_service),
) -> PaginatedResponse[ForestryLandSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    forestry_lands, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ForestryLandSchema.model_validate(land) for land in forestry_lands],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/forestry-land/{id}", response_model=ForestryLandSchema)
async def get_land(
    id: str,
    service: ForestryLandService = Depends(Factory().get_forestry_land_service),
) -> Any | ForestryLandSchema:
    return await service.find_by_id(id)


@router.post(
    "/forestry-land",
    response_model=ForestryLandSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_land(
    data: ForestryLandCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ForestryLandService = Depends(Factory().get_forestry_land_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/forestry-land/{id}",
    response_model=ForestryLandSchema,
)
async def update_land(
    id: str,
    data: ForestryLandUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ForestryLandService = Depends(Factory().get_forestry_land_service),
):
    return await service.update(
        id,
        data.dict(
            exclude_unset=True,
        ),
        current_user,
    )


@router.delete(
    "/forestry-land/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_land(
    id: str,
    service: ForestryLandService = Depends(Factory().get_forestry_land_service),
):
    await service.delete(id)
