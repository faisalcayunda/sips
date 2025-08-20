from typing import Any

from fastapi import APIRouter, Depends

from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import CommoditySchema
from app.schemas.base import PaginatedResponse
from app.services import CommodityService

router = APIRouter()


@router.get("/commodities", response_model=PaginatedResponse[CommoditySchema])
async def get_commodities_list(
    params: CommonParams = Depends(),
    service: CommodityService = Depends(ServiceFactory().get_commodity_service),
) -> PaginatedResponse[CommoditySchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    commodities, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[CommoditySchema.model_validate(commodity) for commodity in commodities],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/commodities/{id}", response_model=CommoditySchema)
async def get_commodity(
    id: str,
    service: CommodityService = Depends(ServiceFactory().get_commodity_service),
) -> Any | CommoditySchema:
    return await service.find_by_id(id)
