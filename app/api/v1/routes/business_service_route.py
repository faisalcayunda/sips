from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    BusinessServiceCreate,
    BusinessServiceSchema,
    BusinessServiceUpdate,
    UserSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import BusinessServiceService

router = APIRouter()


@router.get("/business-services", response_model=PaginatedResponse[BusinessServiceSchema])
async def get_business_services(
    params: CommonParams = Depends(),
    service: BusinessServiceService = Depends(ServiceFactory().get_business_service_service),
) -> PaginatedResponse[BusinessServiceSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    business_services, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[BusinessServiceSchema.model_validate(service_item) for service_item in business_services],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/business-services/{id}", response_model=BusinessServiceSchema)
async def get_business_service(
    id: str,
    service: BusinessServiceService = Depends(ServiceFactory().get_business_service_service),
) -> Any | BusinessServiceSchema:
    return await service.find_by_id(id)


@router.post("/business-services", response_model=BusinessServiceSchema, status_code=status.HTTP_201_CREATED)
async def create_business_service(
    data: BusinessServiceCreate,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessServiceService = Depends(ServiceFactory().get_business_service_service),
):
    return await service.create(data.model_dump(), current_user=current_user)


@router.patch("/business-services/{id}", response_model=BusinessServiceSchema)
async def update_business_service(
    id: str,
    data: BusinessServiceUpdate,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessServiceService = Depends(ServiceFactory().get_business_service_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True), current_user)


@router.delete(
    "/business-services/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_business_service(
    id: str,
    service: BusinessServiceService = Depends(ServiceFactory().get_business_service_service),
):
    await service.delete(id)
