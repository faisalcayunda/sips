from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.core.data_types import YesNoEnum

from .base import BaseSchema
from .forestry_schema_schema import ForestrySchemaJoinSchema
from .regional_schema import RegionalSchema
from .user_schema import UserSchema


class ProposalForestrySchema(BaseSchema):
    id: int
    assist_accounts: Optional[List[UserSchema]] = Field(default=[])
    kph_account: Optional[UserSchema] = Field(default={})
    name: Optional[str] = None
    schema: ForestrySchemaJoinSchema
    kph_account_id: str
    akps_id: str
    area: float
    household_count: int
    head_name: str
    head_contact: str
    map_ps: str
    pps_id: Optional[str] = None
    request_year: str
    release_year: Optional[str] = None
    regent_sk: str
    regional: Optional[RegionalSchema] = Field(default={})
    vertex_detail: Optional[dict] = Field(default={})
    kh_detail: Optional[List] = Field(default=[])
    forestry_sk: str
    nagari_sk: Optional[str] = None
    status: Optional[str]
    is_valid: YesNoEnum
    is_kps_valid: YesNoEnum
    created_by: str
    updated_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ProposalForestryCreateSchema(BaseSchema):
    regional_id: str
    assist_account_id: Optional[List[str]] = None
    name: Optional[str] = None
    schema_id: str
    kph_account_id: str
    kh_id: Optional[List[str]] = None
    akps_id: str
    area: float
    household_count: int
    head_name: str
    head_contact: str
    map_ps: str
    pps_id: Optional[str] = None
    regent_sk: str
    forestry_sk: str
    nagari_sk: Optional[str] = None
    vertex: Optional[str] = None
    status: Optional[str] = None
    is_valid: YesNoEnum
    request_year: str
    release_year: Optional[str] = None
    is_kps_valid: YesNoEnum


class ProposalForestryUpdateSchema(BaseSchema):
    regional_id: Optional[str] = None
    assist_account_id: Optional[List[str]] = None
    name: Optional[str] = None
    schema_id: Optional[str] = None
    kph_account_id: Optional[str] = None
    kh_id: Optional[List[str]] = None
    akps_id: Optional[str] = None
    area: Optional[float] = None
    household_count: Optional[int] = None
    head_name: Optional[str] = None
    head_contact: Optional[str] = None
    map_ps: Optional[str] = None
    pps_id: Optional[str] = None
    nagari_sk: Optional[str] = None
    vertex: Optional[str] = None
    status: Optional[str] = None
    request_year: Optional[str] = None
    release_year: Optional[str] = None
    regent_sk: Optional[str] = None
    forestry_sk: Optional[str] = None
    is_valid: Optional[YesNoEnum] = None
    is_kps_valid: Optional[YesNoEnum] = None
