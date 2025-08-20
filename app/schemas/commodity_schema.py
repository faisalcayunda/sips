from typing import Optional

from pydantic import Field

from .base import BaseSchema


class CommoditySchema(BaseSchema):
    id: int
    name: str
    local_name: Optional[str] = Field(default=None)
    latin_name: Optional[str] = Field(default=None)
    type_code: str
    description: Optional[str] = Field(default=None)
    photo: Optional[str] = Field(default=None)
    status: str
