from datetime import datetime
from typing import Optional

from .base import BaseSchema


class ForestryLandSchema(BaseSchema):
    id: int
    forestry_proposal_id: str
    year: int
    area: float
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ForestryLandCreateSchema(BaseSchema):
    forestry_proposal_id: str
    year: int
    area: float
    created_by: str


class ForestryLandUpdateSchema(BaseSchema):
    forestry_proposal_id: Optional[str] = None
    year: Optional[int] = None
    area: Optional[float] = None
    updated_by: Optional[str] = None
