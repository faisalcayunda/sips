from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.forestry_schema_schema import (
    forestrySchemaCreateSchema,
    forestrySchemaSchema,
    forestrySchemaUpdateSchema,
)
from app.services import forestrySchemaService

router = APIRouter()


@router.get("/forestry-schemas", response_model=PaginatedResponse[forestrySchemaSchema])
async def get_forestry_schemas(
    params: CommonParams = Depends(),
    service: forestrySchemaService = Depends(Factory().get_forestry_schema_service),
) -> PaginatedResponse[forestrySchemaSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    forestry_schemas, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[forestrySchemaSchema.model_validate(schema) for schema in forestry_schemas],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/forestry-schemas/{id}", response_model=forestrySchemaSchema)
async def get_forestry_schemas(
    id: str,
    service: forestrySchemaService = Depends(Factory().get_forestry_schema_service),
) -> Any | forestrySchemaSchema:
    return await service.find_by_id(id)


@router.post(
    "/forestry-schemas",
    response_model=forestrySchemaSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_forestry_schema(
    data: forestrySchemaCreateSchema,
    service: forestrySchemaService = Depends(Factory().get_forestry_schema_service),
):
    return await service.create(data.dict())


@router.patch(
    "/forestry-schemas/{id}",
    response_model=forestrySchemaSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_forestry_schema(
    id: str,
    data: forestrySchemaUpdateSchema,
    service: forestrySchemaService = Depends(Factory().get_forestry_schema_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/forestry-schemas/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_forestry_schema(
    id: str,
    service: forestrySchemaService = Depends(Factory().get_forestry_schema_service),
):
    await service.delete(id)
