from datetime import datetime
from typing import List, Optional

from pydantic import Field

from app.core.data_types import YesNoEnum
from app.schemas.business_class_schema import BusinessClass
from app.schemas.business_operational_status_schema import BusinessOperationalStatus
from app.schemas.proposal_forestry_schema import ProposalForestrySchema
from app.schemas.user_schema import UserSchema

from .base import BaseSchema


class BusinessesSchema(BaseSchema):
    """Schema for business data from database"""

    id: str
    status: YesNoEnum
    name: str
    forestry: Optional[ProposalForestrySchema] = Field(default={}, name="forestry", alias="forestry")
    sk_number: str
    establishment_year: int
    member_count: int
    chairman_name: str
    chairman_contact: str
    account_users: List[UserSchema]
    latitude: str
    longitude: str
    capital_id: str
    operational_status: Optional[BusinessOperationalStatus] = Field(
        default={}, name="operational_status", alias="operational_status"
    )
    operational_period_id: str
    business_class: BusinessClass = Field(default={}, name="class", alias="class")
    is_validated: YesNoEnum
    capital_provider_name: Optional[str] = None
    capital_provision_type: Optional[str] = None
    capital_provision_type_other: Optional[str] = None
    capital_repayment_period: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class BusinessesCreateSchema(BaseSchema):
    """Schema for creating a new business"""

    status: YesNoEnum = YesNoEnum.Y
    name: str
    forestry_area_id: str
    sk_number: str
    establishment_year: int
    member_count: int
    chairman_name: str
    chairman_contact: str
    account_id: str
    latitude: str
    longitude: str
    capital_id: str
    operational_status_id: str
    operational_period_id: str
    class_id: str
    is_validated: YesNoEnum = YesNoEnum.N
    capital_provider_name: Optional[str] = None
    capital_provision_type: Optional[str] = None
    capital_provision_type_other: Optional[str] = None
    capital_repayment_period: Optional[int] = None


class BusinessesUpdateSchema(BaseSchema):
    """Schema for updating a business - all fields optional"""

    status: Optional[YesNoEnum] = None
    name: Optional[str] = None
    forestry_area_id: Optional[str] = None
    sk_number: Optional[str] = None
    establishment_year: Optional[int] = None
    member_count: Optional[int] = None
    chairman_name: Optional[str] = None
    chairman_contact: Optional[str] = None
    account_id: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    capital_id: Optional[str] = None
    operational_status_id: Optional[str] = None
    operational_period_id: Optional[str] = None
    class_id: Optional[str] = None
    is_validated: Optional[YesNoEnum] = None
    capital_provider_name: Optional[str] = None
    capital_provision_type: Optional[str] = None
    capital_provision_type_other: Optional[str] = None
    capital_repayment_period: Optional[int] = None


class BusinessesListResponse(BaseSchema):
    """Schema for list of businesses response"""

    items: List[BusinessesSchema] = Field(default=[])
    total: int
    limit: int
    offset: int
    has_more: bool


class BusinessesFilter(BaseSchema):
    """Schema for filtering businesses"""

    status: Optional[YesNoEnum] = None
    name: Optional[str] = None
    forestry_area_id: Optional[str] = None
    establishment_year: Optional[int] = None
    is_validated: Optional[YesNoEnum] = None
    chairman_name: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
