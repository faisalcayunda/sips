from datetime import datetime
from enum import Enum
from typing import List, Optional

from .base import BaseSchema


class YesNoEnum(str, Enum):
    Y = "Y"
    N = "N"


class ProposalForestrySchema(BaseSchema):
    id: str
    regional_id: str
    assist_account_id: Optional[List[str]] = None
    name: Optional[str] = None
    schema_id: str
    kph_account_id: str
    kh_id: str
    akps_id: str
    area: float
    household_count: int
    head_name: str
    head_contact: str
    map_ps: str
    pps_id: Optional[str] = None
    year_klhk: int
    regent_sk: str
    forestry_sk: str
    is_valid: YesNoEnum
    menlhk_year: Optional[int] = None
    is_kps_valid: YesNoEnum
    create_by: str
    update_by: Optional[str] = None
    create_at: datetime
    update_at: Optional[datetime] = None


class ProposalForestryCreateSchema(BaseSchema):
    regional_id: str
    assist_account_id: Optional[List[str]] = None
    name: Optional[str] = None
    schema_id: str
    kph_account_id: str
    kh_id: str
    akps_id: str
    area: float
    household_count: int
    head_name: str
    head_contact: str
    map_ps: str
    pps_id: Optional[str] = None
    year_klhk: int
    regent_sk: str
    forestry_sk: str
    is_valid: YesNoEnum
    menlhk_year: Optional[int] = None
    is_kps_valid: YesNoEnum
    create_by: str


class ProposalForestryUpdateSchema(BaseSchema):
    regional_id: Optional[str] = None
    assist_account_id: Optional[List[str]] = None
    name: Optional[str] = None
    schema_id: Optional[str] = None
    kph_account_id: Optional[str] = None
    kh_id: Optional[str] = None
    akps_id: Optional[str] = None
    area: Optional[float] = None
    household_count: Optional[int] = None
    head_name: Optional[str] = None
    head_contact: Optional[str] = None
    map_ps: Optional[str] = None
    pps_id: Optional[str] = None
    year_klhk: Optional[int] = None
    regent_sk: Optional[str] = None
    forestry_sk: Optional[str] = None
    is_valid: Optional[YesNoEnum] = None
    menlhk_year: Optional[int] = None
    is_kps_valid: Optional[YesNoEnum] = None
    update_by: Optional[str] = None
    update_at: Optional[datetime] = None
