from typing import Optional

from .base import BaseSchema


class ProposalforestryStatusSchema(BaseSchema):
    id: str
    name: str
    proposal_forestry_vertex: str
    description: Optional[str] = None


class ProposalforestryStatusCreateSchema(BaseSchema):
    id: str
    name: str
    proposal_forestry_vertex: str
    description: Optional[str] = None


class ProposalforestryStatusUpdateSchema(BaseSchema):
    name: Optional[str] = None
    proposal_forestry_vertex: Optional[str] = None
    description: Optional[str] = None
