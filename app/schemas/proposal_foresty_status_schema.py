from typing import Optional

from .base import BaseSchema


class ProposalForestyStatusSchema(BaseSchema):
    id: str
    name: str
    proposal_foresty_vertex: str
    description: Optional[str] = None


class ProposalForestyStatusCreateSchema(BaseSchema):
    id: str
    name: str
    proposal_forestry_vertex: str
    description: Optional[str] = None


class ProposalForestyStatusUpdateSchema(BaseSchema):
    name: Optional[str] = None
    proposal_forestry_vertex: Optional[str] = None
    description: Optional[str] = None
