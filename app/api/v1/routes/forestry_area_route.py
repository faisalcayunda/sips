from typing import Any

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.forestry_area_schema import ForestryAreaSchema
from app.services import ForestryAreaService

router = APIRouter()


@router.get(
    "/forestry-area",
    response_model=PaginatedResponse[ForestryAreaSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_forestry_area_list(
    params: CommonParams = Depends(),
    service: ForestryAreaService = Depends(Factory().get_forestry_area_service),
) -> PaginatedResponse[ForestryAreaSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    forestry_area_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ForestryAreaSchema.model_validate(area) for area in forestry_area_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/forestry-area/{id}", response_model=ForestryAreaSchema)
async def get_forestry_area(
    id: str,
    service: ForestryAreaService = Depends(Factory().get_forestry_area_service),
) -> Any | ForestryAreaSchema:
    return await service.find_by_id(id)
