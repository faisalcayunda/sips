from typing import Any

from fastapi import APIRouter, Depends

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.roles_schema import RolesSchema
from app.services import RolesService

router = APIRouter()


@router.get(
    "/roles",
    response_model=PaginatedResponse[RolesSchema],
    dependencies=[Depends(get_current_active_user)],
)
async def get_roles_list(
    params: CommonParams = Depends(),
    service: RolesService = Depends(Factory().get_roles_service),
) -> PaginatedResponse[RolesSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    roles_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[RolesSchema.model_validate(roles) for roles in roles_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/roles/{id}", response_model=RolesSchema)
async def get_roles(
    id: str,
    service: RolesService = Depends(Factory().get_roles_service),
) -> Any | RolesSchema:
    return await service.find_by_id(id)
