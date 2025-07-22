from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.foresty_schema_schema import (
    ForestySchemaCreateSchema,
    ForestySchemaSchema,
    ForestySchemaUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import ForestySchemaService

router = APIRouter()


@router.get("/foresty-schemas", response_model=PaginatedResponse[ForestySchemaSchema])
async def get_foresty_schemas(
    params: CommonParams = Depends(),
    service: ForestySchemaService = Depends(Factory().get_foresty_schema_service),
) -> PaginatedResponse[ForestySchemaSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    foresty_schemas, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ForestySchemaSchema.model_validate(schema) for schema in foresty_schemas],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/foresty-schemas/{id}", response_model=ForestySchemaSchema)
async def get_foresty_schemas(
    id: str,
    service: ForestySchemaService = Depends(Factory().get_foresty_schema_service),
) -> Any | ForestySchemaSchema:
    return await service.find_by_id(id)


@router.post(
    "/foresty-schemas",
    response_model=ForestySchemaSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_foresty_schema(
    data: ForestySchemaCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ForestySchemaService = Depends(Factory().get_foresty_schema_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/foresty-schemas/{id}",
    response_model=ForestySchemaSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_foresty_schema(
    id: str,
    data: ForestySchemaUpdateSchema,
    service: ForestySchemaService = Depends(Factory().get_foresty_schema_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/foresty-schemas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_foresty_schema(
    id: str,
    service: ForestySchemaService = Depends(Factory().get_foresty_schema_service),
):
    await service.delete(id)
