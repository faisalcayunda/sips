from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    FarmerIncomesCreateSchema,
    FarmerIncomesSchema,
    FarmerIncomesUpdateSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import FarmerIncomesService

router = APIRouter()


@router.get("/farmer-incomes", response_model=PaginatedResponse[FarmerIncomesSchema])
async def get_farmer_incomes_list(
    params: CommonParams = Depends(),
    service: FarmerIncomesService = Depends(ServiceFactory().get_farmer_incomes_service),
) -> PaginatedResponse[FarmerIncomesSchema]:
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
        items=[FarmerIncomesSchema.model_validate(data) for data in data_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/farmer-incomes/{id}", response_model=FarmerIncomesSchema)
async def get_farmer_incomes(
    id: str,
    service: FarmerIncomesService = Depends(ServiceFactory().get_farmer_incomes_service),
) -> Any | FarmerIncomesSchema:
    return await service.find_by_id(id)


@router.post(
    "/farmer-incomes",
    response_model=FarmerIncomesSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_farmer_incomes(
    data: FarmerIncomesCreateSchema,
    service: FarmerIncomesService = Depends(ServiceFactory().get_farmer_incomes_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/farmer-incomes/{id}",
    response_model=FarmerIncomesSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_farmer_incomes(
    id: str,
    data: FarmerIncomesUpdateSchema,
    service: FarmerIncomesService = Depends(ServiceFactory().get_farmer_incomes_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True))


@router.delete(
    "/farmer-incomes/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_farmer_incomes(
    id: str,
    service: FarmerIncomesService = Depends(ServiceFactory().get_farmer_incomes_service),
):
    await service.delete(id)
