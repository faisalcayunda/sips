from typing import Optional

from .base import BaseSchema


class forestrySchemaSchema(BaseSchema):
    id: str
    schema_id: str
    name: str
    description: Optional[str] = None
    ord: Optional[int] = None


class forestrySchemaCreateSchema(BaseSchema):
    schema_id: str
    name: str
    description: Optional[str] = None
    ord: Optional[int] = None


class forestrySchemaUpdateSchema(BaseSchema):
    schema_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    ord: Optional[int] = None
