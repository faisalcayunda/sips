from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict

from app.utils.helpers import orjson_dumps

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base Pydantic model with orjson configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    def model_dump_json(self, **kwargs):
        """Override default json serialization to use orjson."""
        return orjson_dumps(self.model_dump(**kwargs))


class PaginatedResponse(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool
