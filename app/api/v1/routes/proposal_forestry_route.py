from typing import Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.proposal_forestry_schema import (
    ProposalForestryCreateSchema,
    ProposalForestrySchema,
    ProposalForestryUpdateSchema,
)
from app.services import ForestyProposalService

router = APIRouter()


@router.get("/proposal-forestry", response_model=PaginatedResponse[ProposalForestrySchema])
async def get_proposal_list(
    params: CommonParams = Depends(),
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
) -> PaginatedResponse[ProposalForestrySchema]:
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset
    forestry_proposals, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[ProposalForestrySchema.model_validate(proposal) for proposal in forestry_proposals],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/proposal-forestry/{id}", response_model=ProposalForestrySchema)
async def get_proposal(
    id: str,
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
) -> Any | ProposalForestrySchema:
    return await service.find_by_id(id)


@router.post(
    "/proposal-forestry",
    response_model=ProposalForestrySchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_proposal(
    data: ProposalForestryCreateSchema,
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
):
    return await service.create(data.dict())


@router.patch(
    "/proposal-forestry/{id}",
    response_model=ProposalForestrySchema,
    dependencies=[Depends(get_current_active_user)],
)
async def update_proposal(
    id: str,
    data: ProposalForestryUpdateSchema,
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
):
    return await service.update(id, data.dict(exclude_unset=True))


@router.delete(
    "/proposal-forestry/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_proposal(
    id: str,
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
):
    await service.delete(id)
