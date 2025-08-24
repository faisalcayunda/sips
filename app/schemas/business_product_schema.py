from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema
from .business_harvest_schema import BusinessHarvestSchema
from .businesses_schema import BusinessesSchema
from .commodity_schema import CommoditySchema


class BusinessProductSchema(BaseSchema):
    id: int
    business: Optional[BusinessesSchema] = Field(default={})
    commodity: Optional[CommoditySchema] = Field(default={})
    name: str
    description: str
    beneficiary_count: int
    manufacture_code: str
    latitude: str
    longitude: str
    area_managed: float
    area_planned: float
    area_productive: str
    area_unit: str
    harvest_production: str
    harvest_unit: str
    harvest: Optional[BusinessHarvestSchema] = Field(default={})
    type_id: str
    tools_available: str
    tools_detail: str
    price_sell: int
    buyer_type_id: str
    buyer_count: int
    sales_freq_id: str
    export_status_id: str
    export_purpose: str
    seedstock_availability: Optional[str] = Field(default=None)
    unit_price_label: Optional[str] = Field(default=None)
    unit_sold_label: Optional[str] = Field(default=None)
    buyer_target: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class BusinessProductCreate(BaseSchema):
    business_id: str
    commodity_id: int
    name: str
    description: str
    beneficiary_count: int
    manufacture_code: str
    latitude: str
    longitude: str
    area_managed: float
    area_planned: float
    area_productive: str
    area_unit: str
    harvest_production: str
    harvest_unit: str
    harvest_id: str
    type_id: str
    tools_available: str
    tools_detail: str
    price_sell: int
    buyer_type_id: str
    buyer_count: int
    sales_freq_id: str
    export_status_id: str
    export_purpose: str
    seedstock_availability: Optional[str] = Field(default=None)
    unit_price_label: Optional[str] = Field(default=None)
    unit_sold_label: Optional[str] = Field(default=None)
    buyer_target: Optional[str] = Field(default=None)


class BusinessProductUpdate(BaseSchema):
    business_id: Optional[str] = Field(default=None)
    commodity_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    beneficiary_count: Optional[int] = Field(default=None)
    manufacture_code: Optional[str] = Field(default=None)
    latitude: Optional[str] = Field(default=None)
    longitude: Optional[str] = Field(default=None)
    area_managed: Optional[float] = Field(default=None)
    area_planned: Optional[float] = Field(default=None)
    area_productive: Optional[str] = Field(default=None)
    area_unit: Optional[str] = Field(default=None)
    harvest_production: Optional[str] = Field(default=None)
    harvest_unit: Optional[str] = Field(default=None)
    harvest_id: Optional[str] = Field(default=None)
    type_id: Optional[str] = Field(default=None)
    tools_available: Optional[str] = Field(default=None)
    tools_detail: Optional[str] = Field(default=None)
    price_sell: Optional[int] = Field(default=None)
    buyer_type_id: Optional[str] = Field(default=None)
    buyer_count: Optional[int] = Field(default=None)
    sales_freq_id: Optional[str] = Field(default=None)
    export_status_id: Optional[str] = Field(default=None)
    export_purpose: Optional[str] = Field(default=None)
    seedstock_availability: Optional[str] = Field(default=None)
    unit_price_label: Optional[str] = Field(default=None)
    unit_sold_label: Optional[str] = Field(default=None)
    buyer_target: Optional[str] = Field(default=None)
