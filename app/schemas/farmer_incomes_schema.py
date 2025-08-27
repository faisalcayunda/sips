from typing import Optional

from .base import BaseSchema


class FarmerIncomesSchema(BaseSchema):
    id: int
    year: str
    increase_percentage: float


class FarmerIncomesCreateSchema(BaseSchema):
    year: str
    increase_percentage: float


class FarmerIncomesUpdateSchema(BaseSchema):
    year: Optional[str] = None
    increase_percentage: Optional[float] = None
