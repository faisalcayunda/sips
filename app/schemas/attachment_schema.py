from datetime import datetime
from typing import Optional

from .base import BaseSchema


class AttachmentSchema(BaseSchema):
    id: int
    name: str
    attach_string: str
    attach_type: str
    attach_sign: str
    created_by: str
    created_at: datetime
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None


class AttachmentCreateSchema(BaseSchema):
    name: str
    attach_string: str
    attach_type: str
    attach_sign: str
    created_by: str


class AttachmentUpdateSchema(BaseSchema):
    name: Optional[str] = None
    attach_string: Optional[str] = None
    attach_type: Optional[str] = None
    attach_sign: Optional[str] = None
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
