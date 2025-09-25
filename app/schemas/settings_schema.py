from typing import Any, Optional

from .base import BaseSchema


class SettingsResponseSchema(BaseSchema):
    key: str
    value: Optional[Any] = None
    description: Optional[str] = None


class SettingsCreateSchema(BaseSchema):
    key: str
    value: Optional[Any] = None
    description: Optional[str] = None


class SettingsUpdateSchema(BaseSchema):
    value: Optional[Any] = None
    description: Optional[str] = None
