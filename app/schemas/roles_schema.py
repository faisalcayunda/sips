from typing import Optional

from pydantic import Field

from .base import BaseSchema
from .navigation_schema import NavigationPermissionSchema


class RolesSchema(BaseSchema):
    id: int
    name: str


class RolesWithPermission(BaseSchema):
    id: int
    name: str
    permissions: Optional[NavigationPermissionSchema] = Field(default=[])
