from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema
from .businesses_schema import BusinessesSchema
from .commodity_schema import CommoditySchema


class BusinessServiceSchema(BaseSchema):
    def __init__(self, **data):
        if "updated_at" in data and data["updated_at"] == "":
            data["updated_at"] = None
        super().__init__(**data)

    id: int
    business: Optional[BusinessesSchema] = Field(default={})
    commodity: Optional[CommoditySchema] = Field(default={})
    name: str
    latitude: str
    longitude: str
    visitor_type_id: str
    origin_visitor_id: str
    ticket_price: int
    parking_fee: int
    other_item_price_id: int
    additional_info: Optional[str] = Field(default=None)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)


class BusinessServiceCreate(BaseSchema):
    business_id: str
    commodity_id: int
    name: str
    latitude: str
    longitude: str
    visitor_type_id: str
    origin_visitor_id: str
    ticket_price: int
    parking_fee: int
    other_item_price_id: str
    additional_info: Optional[str] = Field(default=None)


class BusinessServiceUpdate(BaseSchema):
    business_id: Optional[str] = Field(default=None)
    commodity_id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    latitude: Optional[str] = Field(default=None)
    longitude: Optional[str] = Field(default=None)
    visitor_type_id: Optional[str] = Field(default=None)
    origin_visitor_id: Optional[str] = Field(default=None)
    ticket_price: Optional[int] = Field(default=None)
    parking_fee: Optional[int] = Field(default=None)
    other_item_price_id: Optional[str] = Field(default=None)
    additional_info: Optional[str] = Field(default=None)
