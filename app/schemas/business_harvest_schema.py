from typing import Optional

from pydantic import Field

from .base import BaseSchema


class BusinessHarvestSchema(BaseSchema):
    id: int
    harvest_code: str
    name: str
    note: Optional[str] = Field(default=None)
