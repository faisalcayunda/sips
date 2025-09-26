from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import StreamingResponse

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.proposal_forestry_schema import (
    ProposalForestryCreateSchema,
    ProposalForestrySchema,
    ProposalForestryUpdateSchema,
)
from app.schemas.user_schema import UserSchema
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
        items=[
            ProposalForestrySchema.model_validate(proposal, by_alias=False, by_name=True)
            for proposal in forestry_proposals
        ],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/proposal-forestry/export")
async def export_forestry_proposal(
    filters: Optional[List[str]] = Query(None),
    sort: Optional[List[str]] = Query(None),
    search: str = Query(""),
    group_by: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(0),
    relationships: Optional[List[str]] = Query(None),
    searchable_columns: Optional[List[str]] = Query(None),
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
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
        headers={"Content-Disposition": "attachment; filename=KPS.xlsx"},
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
)
async def create_proposal(
    data: ProposalForestryCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
):
    return await service.create(data.dict(), current_user)


@router.patch(
    "/proposal-forestry/{id}",
    response_model=ProposalForestrySchema,
)
async def update_proposal(
    id: str,
    data: ProposalForestryUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: ForestyProposalService = Depends(Factory().get_proposal_forestry_service),
):
    return await service.update(id, data.dict(exclude_unset=True), current_user)


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
