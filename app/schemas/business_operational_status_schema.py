from typing import Optional

from pydantic import Field

from .base import BaseSchema


class BusinessOperationalStatus(BaseSchema):
    id: int
    name: str
    type: str
    notes: Optional[str] = Field(default=None)
