from typing import Optional

from .base import BaseSchema


class FarmerIncomesSchema(BaseSchema):
    id: int
    year: int
    income: int
    difference: int
    percentage: float


class FarmerIncomesCreateSchema(BaseSchema):
    year: int
    income: int
    difference: int
    percentage: float


class FarmerIncomesUpdateSchema(BaseSchema):
    year: Optional[int] = None
    income: Optional[int] = None
    difference: Optional[int] = None
    percentage: Optional[float] = None
