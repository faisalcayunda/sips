from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.piaps_schema import PiapsCreateSchema, PiapsSchema, PiapsUpdateSchema
from app.services import PiapsService

router = APIRouter()


@router.get("/piaps", response_model=PaginatedResponse[PiapsSchema])
async def get_piaps_list(
    params: CommonParams = Depends(),
    service: PiapsService = Depends(Factory().get_piaps_service),
) -> PaginatedResponse[PiapsSchema]:
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
        items=[PiapsSchema.model_validate(piaps) for piaps in piaps_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/piaps/{id}", response_model=PiapsSchema)
async def get_piaps(
    id: str,
    service: PiapsService = Depends(Factory().get_piaps_service),
) -> Any | PiapsSchema:
    return await service.find_by_id(id)


@router.post(
    "/piaps",
    response_model=PiapsSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_piaps(
    data: PiapsCreateSchema,
    service: PiapsService = Depends(Factory().get_piaps_service),
):
    return await service.create(data.dict())


@router.patch(
    "/piaps/{id}",
    response_model=PiapsSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_piaps(
    id: str,
    data: PiapsUpdateSchema,
    service: PiapsService = Depends(Factory().get_piaps_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/piaps/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_piaps(
    id: str,
    service: PiapsService = Depends(Factory().get_piaps_service),
):
    await service.delete(id)
