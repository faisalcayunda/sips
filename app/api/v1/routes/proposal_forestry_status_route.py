from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.proposal_forestry_status_schema import (
    ProposalforestryStatusCreateSchema,
    ProposalforestryStatusSchema,
    ProposalforestryStatusUpdateSchema,
)
from app.services import ProposalforestryStatusService

router = APIRouter()


@router.get(
    "/proposal-forestry-status",
    response_model=PaginatedResponse[ProposalforestryStatusSchema],
)
async def get_forestry_schemas(
    params: CommonParams = Depends(),
    service: ProposalforestryStatusService = Depends(Factory().get_proposal_forestry_status_service),
) -> PaginatedResponse[ProposalforestryStatusSchema]:
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
        items=[ProposalforestryStatusSchema.model_validate(proposal) for proposal in proposals],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/proposal-forestry-status/{id}", response_model=ProposalforestryStatusSchema)
async def get_proposal_forestry_status(
    id: str,
    service: ProposalforestryStatusService = Depends(Factory().get_proposal_forestry_status_service),
) -> Any | ProposalforestryStatusSchema:
    return await service.find_by_id(id)


@router.post(
    "/proposal-forestry-status",
    response_model=ProposalforestryStatusSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_proposal_forestry_status(
    data: ProposalforestryStatusCreateSchema,
    service: ProposalforestryStatusService = Depends(Factory().get_proposal_forestry_status_service),
):
    return await service.create(data.dict())


@router.patch(
    "/proposal-forestry-status/{id}",
    response_model=ProposalforestryStatusSchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_proposal_forestry_status(
    id: str,
    data: ProposalforestryStatusUpdateSchema,
    service: ProposalforestryStatusService = Depends(Factory().get_proposal_forestry_status_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/proposal-forestry-status/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_proposal_forestry_status(
    id: str,
    service: ProposalforestryStatusService = Depends(Factory().get_proposal_forestry_status_service),
):
    await service.delete(id)
