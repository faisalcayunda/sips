from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.attachment_schema import (
    AttachmentCreateSchema,
    AttachmentSchema,
    AttachmentUpdateSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import AttachmentService

router = APIRouter()


@router.get("/attachment", response_model=PaginatedResponse[AttachmentSchema])
async def get_attachment_list(
    params: CommonParams = Depends(),
    service: AttachmentService = Depends(Factory().get_attachment_service),
) -> PaginatedResponse[AttachmentSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    attachment_list, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[AttachmentSchema.model_validate(attachment) for attachment in attachment_list],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/attachment/{id}", response_model=AttachmentSchema)
async def get_attachment(
    id: str,
    service: AttachmentService = Depends(Factory().get_attachment_service),
) -> Any | AttachmentSchema:
    return await service.find_by_id(id)


@router.post(
    "/attachment",
    response_model=AttachmentSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_attachment(
    data: AttachmentCreateSchema,
    service: AttachmentService = Depends(Factory().get_attachment_service),
):
    return await service.create(data.dict())


@router.patch(
    "/attachment/{id}",
    response_model=AttachmentSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_attachment(
    id: str,
    data: AttachmentUpdateSchema,
    service: AttachmentService = Depends(Factory().get_attachment_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/attachment/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_attachment(
    id: str,
    service: AttachmentService = Depends(Factory().get_attachment_service),
):
    await service.delete(id)
