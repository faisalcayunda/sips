from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    EconomicValuesCreateSchema,
    EconomicValuesSchema,
    EconomicValuesUpdateSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import EconomicValuesService

router = APIRouter()


@router.get("/economic-values", response_model=PaginatedResponse[EconomicValuesSchema])
async def get_economic_values_list(
    params: CommonParams = Depends(),
    service: EconomicValuesService = Depends(ServiceFactory().get_economic_values_service),
) -> PaginatedResponse[EconomicValuesSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    data_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[EconomicValuesSchema.model_validate(data) for data in data_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/economic-values/{id}", response_model=EconomicValuesSchema)
async def get_economic_values(
    id: str,
    service: EconomicValuesService = Depends(ServiceFactory().get_economic_values_service),
) -> Any | EconomicValuesSchema:
    return await service.find_by_id(id)


@router.post(
    "/economic-values",
    response_model=EconomicValuesSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_economic_values(
    data: EconomicValuesCreateSchema,
    service: EconomicValuesService = Depends(ServiceFactory().get_economic_values_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/economic-values/{id}",
    response_model=EconomicValuesSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_economic_values(
    id: str,
    data: EconomicValuesUpdateSchema,
    service: EconomicValuesService = Depends(ServiceFactory().get_economic_values_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True))


@router.delete(
    "/economic-values/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_economic_values(
    id: str,
    service: EconomicValuesService = Depends(ServiceFactory().get_economic_values_service),
):
    await service.delete(id)
