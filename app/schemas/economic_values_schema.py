from typing import Optional

from pydantic import Field

from .base import BaseSchema


class EconomicValuesSchema(BaseSchema):
    id: int = Field(description="Unique identifier for the economic value")
    kps_id: int = Field(description="Unique identifier for the KPS")
    kups_id: int = Field(description="Unique identifier for the KUPS")
    group_name: str = Field(description="Name of the group")
    year: int = Field(description="Year")
    commodity_id: int = Field(description="Unique identifier for the commodity")
    production: float = Field(description="Production value")
    value: float = Field(description="Economic value")
    note: Optional[str] = Field(default=None, description="Note")


class EconomicValuesCreateSchema(BaseSchema):
    kps_id: int = Field(description="Unique identifier for the KPS")
    kups_id: int = Field(description="Unique identifier for the KUPS")
    group_name: str = Field(description="Name of the group")
    year: int = Field(description="Year")
    commodity_id: int = Field(description="Unique identifier for the commodity")
    production: float = Field(description="Production value")
    value: float = Field(description="Economic value")
    note: Optional[str] = Field(default=None, description="Note")


class EconomicValuesUpdateSchema(BaseSchema):
    kps_id: Optional[int] = Field(default=None, description="Unique identifier for the KPS")
    kups_id: Optional[int] = Field(default=None, description="Unique identifier for the KUPS")
    group_name: Optional[str] = Field(default=None, description="Name of the group")
    year: Optional[int] = Field(default=None, description="Year")
    commodity_id: Optional[int] = Field(default=None, description="Unique identifier for the commodity")
    production: Optional[float] = Field(default=None, description="Production value")
    value: Optional[float] = Field(default=None, description="Economic value")
    note: Optional[str] = Field(default=None, description="Note")
