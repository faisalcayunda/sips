from typing import Any

from fastapi import APIRouter, Depends

from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import BusinessHarvestSchema
from app.schemas.base import PaginatedResponse
from app.services import BusinessHarvestService

router = APIRouter()


@router.get("/business-harvests", response_model=PaginatedResponse[BusinessHarvestSchema])
async def get_harvests_list(
    params: CommonParams = Depends(),
    service: BusinessHarvestService = Depends(ServiceFactory().get_business_harvest_service),
) -> PaginatedResponse[BusinessHarvestSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    harvests, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[BusinessHarvestSchema.model_validate(harvest) for harvest in harvests],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/business-harvests/{id}", response_model=BusinessHarvestSchema)
async def get_harvest(
    id: str,
    service: BusinessHarvestService = Depends(ServiceFactory().get_business_harvest_service),
) -> Any | BusinessHarvestSchema:
    return await service.find_by_id(id)
