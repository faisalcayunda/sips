from typing import Optional

from pydantic import Field

from .base import BaseSchema


class BusinessClass(BaseSchema):
    id: int
    name: str
    type: str
    description: Optional[str] = Field(default=None)
