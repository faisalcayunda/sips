from datetime import datetime
from typing import Dict, Optional

from pydantic import Field

from app.core.data_types import YesNoEnum

from .base import BaseSchema


class NavigationSchema(BaseSchema):
    id: int
    name: str
    parent: Optional[int] = None
    is_enabled: YesNoEnum
    icon: Optional[str] = None
    url: Optional[str] = None
    sort_order: Optional[int] = None
    sign: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class NavigationPermissionSchema(BaseSchema):
    id: int
    name: str
    parent: Optional[int] = None
    is_enabled: YesNoEnum
    icon: Optional[str] = None
    url: Optional[str] = None
    sort_order: Optional[int] = None
    sign: Optional[str] = None
    permissions: Optional[Dict] = Field(default={})


class NavigationCreateSchema(BaseSchema):
    name: str
    parent: Optional[int] = None
    is_enabled: YesNoEnum
    icon: Optional[str] = None
    url: Optional[str] = None
    sort_order: Optional[int] = None
    sign: Optional[str] = None
    created_by: Optional[str] = None


class NavigationUpdateSchema(BaseSchema):
    name: Optional[str] = None
    parent: Optional[int] = None
    is_enabled: Optional[YesNoEnum] = None
    icon: Optional[str] = None
    url: Optional[str] = None
    sort_order: Optional[int] = None
    sign: Optional[str] = None
    updated_by: Optional[str] = None
