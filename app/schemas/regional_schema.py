from datetime import datetime
from typing import Optional

from .base import BaseSchema


class RegionalSchema(BaseSchema):
    id: str
    name: str
    parent: str
    group: str
    create_by: Optional[str]
    create_at: datetime


class RegionalCreateSchema(BaseSchema):
    name: str
    parent: str
    group: str


class RegionalUpdateSchema(BaseSchema):
    name: Optional[str] = None
    parent: Optional[str] = None
    group: Optional[str] = None
