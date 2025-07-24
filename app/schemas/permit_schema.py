from datetime import datetime
from typing import Dict, Optional

from .base import BaseSchema


class PermitSchema(BaseSchema):
    id: int
    role_id: int
    navigation_id: int
    permit_content: Dict
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class PermitCreateSchema(BaseSchema):
    role_id: int
    navigation_id: int
    permit_content: Dict


class PermitUpdateSchema(BaseSchema):
    role_id: Optional[int] = None
    navigation_id: Optional[int] = None
    permit_content: Optional[Dict] = None
