from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.permit_schema import (
    PermitCreateSchema,
    PermitSchema,
    PermitUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import PermitService

router = APIRouter()


@router.get("/permissions", response_model=PaginatedResponse[PermitSchema])
async def get_permission_list(
    params: CommonParams = Depends(),
    service: PermitService = Depends(Factory().get_permit_service),
) -> PaginatedResponse[PermitSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    permissions, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[PermitSchema.model_validate(permission) for permission in permissions],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/permissions/{id}", response_model=PermitSchema)
async def get_permission(
    id: str,
    service: PermitService = Depends(Factory().get_permit_service),
) -> Any | PermitSchema:
    return await service.find_by_id(id)


@router.post(
    "/permissions",
    response_model=PermitSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    data: PermitCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: PermitService = Depends(Factory().get_permit_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/permissions/{id}",
    response_model=PermitSchema,
)
async def update_permission(
    id: str,
    data: PermitUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: PermitService = Depends(Factory().get_permit_service),
):
    return await service.update(id, data.dict(exclude_unset=True), current_user)


@router.delete(
    "/permissions/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_permission(
    id: str,
    service: PermitService = Depends(Factory().get_permit_service),
):
    await service.delete(id)
