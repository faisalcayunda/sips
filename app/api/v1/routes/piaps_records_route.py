from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    PiapsRecordsCreateSchema,
    PiapsRecordsSchema,
    PiapsRecordsUpdateSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import PiapsRecordsService

router = APIRouter()


@router.get("/piaps-records", response_model=PaginatedResponse[PiapsRecordsSchema])
async def get_piaps_records_list(
    params: CommonParams = Depends(),
    service: PiapsRecordsService = Depends(ServiceFactory().get_piaps_records_service),
) -> PaginatedResponse[PiapsRecordsSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    piaps_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[PiapsRecordsSchema.model_validate(piaps) for piaps in piaps_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/piaps-records/{id}", response_model=PiapsRecordsSchema)
async def get_piaps_records(
    id: str,
    service: PiapsRecordsService = Depends(ServiceFactory().get_piaps_records_service),
) -> Any | PiapsRecordsSchema:
    return await service.find_by_id(id)


@router.post(
    "/piaps-records",
    response_model=PiapsRecordsSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_piaps(
    data: PiapsRecordsCreateSchema,
    service: PiapsRecordsService = Depends(ServiceFactory().get_piaps_records_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/piaps-records/{id}",
    response_model=PiapsRecordsSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_piaps_records(
    id: str,
    data: PiapsRecordsUpdateSchema,
    service: PiapsRecordsService = Depends(ServiceFactory().get_piaps_records_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True))


@router.delete(
    "/piaps-records/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_piaps_records(
    id: str,
    service: PiapsRecordsService = Depends(ServiceFactory().get_piaps_records_service),
):
    await service.delete(id)
