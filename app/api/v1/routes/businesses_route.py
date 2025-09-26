from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.businesses_schema import (
    BusinessesCreateSchema,
    BusinessesSchema,
    BusinessesUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import BusinessesService

router = APIRouter()


@router.get("/businesses", response_model=PaginatedResponse[BusinessesSchema])
async def get_businesses(
    params: CommonParams = Depends(),
    service: BusinessesService = Depends(Factory().get_businesses_service),
) -> PaginatedResponse[BusinessesSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    businesses, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[BusinessesSchema.model_validate(business) for business in businesses],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/businesses/export")
async def export_business(
    filters: Optional[List[str]] = Query(None),
    sort: Optional[List[str]] = Query(None),
    search: str = Query(""),
    group_by: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(0),
    relationships: Optional[List[str]] = Query(None),
    searchable_columns: Optional[List[str]] = Query(None),
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    excel_bytes = await service.export_to_excel(
        filters=filters,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
        relationships=relationships,
        searchable_columns=searchable_columns,
    )
    return StreamingResponse(
        iter([excel_bytes]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=KUPS.xlsx"},
    )


@router.get("/businesses/{id}", response_model=BusinessesSchema)
async def get_business(
    id: str,
    service: BusinessesService = Depends(Factory().get_businesses_service),
) -> Any | BusinessesSchema:
    return await service.find_by_id(id)


@router.post("/businesses", response_model=BusinessesSchema, status_code=status.HTTP_201_CREATED)
async def create_business(
    data: BusinessesCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    return await service.create(data.model_dump(), current_user=current_user)


@router.patch("/businesses/{id}", response_model=BusinessesSchema)
async def update_business(
    id: str,
    data: BusinessesUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    return await service.update(id, data.model_dump(exclude_unset=True), current_user)


@router.delete(
    "/businesses/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_business(
    id: str,
    service: BusinessesService = Depends(Factory().get_businesses_service),
):
    await service.delete(id)
