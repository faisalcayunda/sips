from typing import Optional

from .base import BaseSchema


class PiapsSchema(BaseSchema):
    id: int
    name: str
    acc_id: str
    area: float
    notes: Optional[str] = None


class PiapsCreateSchema(BaseSchema):
    name: str
    area: float
    acc_id: str
    notes: Optional[str] = None


class PiapsUpdateSchema(BaseSchema):
    name: Optional[str] = None
    area: Optional[float] = None
    acc_id: Optional[str] = None
    notes: Optional[str] = None
