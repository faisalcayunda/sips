from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.api.dependencies.factory import Factory
from app.schemas.base import PaginatedResponse
from app.services import MapsService

router = APIRouter()


@router.get("/maps")
async def get_maps_list(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: MapsService = Depends(Factory().get_maps_service),
    filters: Optional[dict] = None,
) -> PaginatedResponse:
    filters = filters or {}

    maps, total = await service.get_all(
        filters=filters,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=maps,
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )
