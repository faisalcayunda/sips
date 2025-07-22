from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.proposal_foresty_status_schema import (
    ProposalForestyStatusCreateSchema,
    ProposalForestyStatusSchema,
    ProposalForestyStatusUpdateSchema,
)
from app.schemas.user_schema import UserSchema
from app.services import ProposalForestyStatusService

router = APIRouter()


@router.get(
    "/proposal-foresty-status",
    response_model=PaginatedResponse[ProposalForestyStatusSchema],
)
async def get_foresty_schemas(
    params: CommonParams = Depends(),
    service: ProposalForestyStatusService = Depends(Factory().get_proposal_foresty_status_service),
) -> PaginatedResponse[ProposalForestyStatusSchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    proposals, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ProposalForestyStatusSchema.model_validate(proposal) for proposal in proposals],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/proposal-foresty-status/{id}", response_model=ProposalForestyStatusSchema)
async def get_proposal_foresty_status(
    id: str,
    service: ProposalForestyStatusService = Depends(Factory().get_proposal_foresty_status_service),
) -> Any | ProposalForestyStatusSchema:
    return await service.find_by_id(id)


@router.post(
    "/proposal-foresty-status",
    response_model=ProposalForestyStatusSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_proposal_foresty_status(
    data: ProposalForestyStatusCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ProposalForestyStatusService = Depends(Factory().get_proposal_foresty_status_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/proposal-foresty-status/{id}",
    response_model=ProposalForestyStatusSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_proposal_foresty_status(
    id: str,
    data: ProposalForestyStatusUpdateSchema,
    service: ProposalForestyStatusService = Depends(Factory().get_proposal_foresty_status_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/proposal-foresty-status/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_proposal_foresty_status(
    id: str,
    service: ProposalForestyStatusService = Depends(Factory().get_proposal_foresty_status_service),
):
    await service.delete(id)
