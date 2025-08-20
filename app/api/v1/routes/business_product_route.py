from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import ServiceFactory
from app.core.params import CommonParams
from app.schemas import (
    BusinessProductCreate,
    BusinessProductSchema,
    BusinessProductUpdate,
    UserSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import BusinessProductService

router = APIRouter()


@router.get("/business-products", response_model=PaginatedResponse[BusinessProductSchema])
async def get_business_product(
    params: CommonParams = Depends(),
    service: BusinessProductService = Depends(ServiceFactory().get_business_product_service),
) -> PaginatedResponse[BusinessProductSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    business_products, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[BusinessProductSchema.model_validate(product) for product in business_products],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/business-products/{id}", response_model=BusinessProductSchema)
async def get_business_product(
    id: str,
    service: BusinessProductService = Depends(ServiceFactory().get_business_product_service),
) -> Any | BusinessProductSchema:
    return await service.find_by_id(id)


@router.post("/business-products", response_model=BusinessProductSchema, status_code=status.HTTP_201_CREATED)
async def create_business_product(
    data: BusinessProductCreate,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessProductService = Depends(ServiceFactory().get_business_product_service),
):
    return await service.create(data.model_dump(), current_user=current_user)


@router.patch("/business-products/{id}", response_model=BusinessProductSchema)
async def update_business_product(
    id: str,
    data: BusinessProductUpdate,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessProductService = Depends(ServiceFactory().get_business_product_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True), current_user)


@router.delete(
    "/business-products/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_business_product(
    id: str,
    service: BusinessProductService = Depends(ServiceFactory().get_business_product_service),
):
    await service.delete(id)
