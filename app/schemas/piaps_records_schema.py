from typing import Optional

from pydantic import Field

from .base import BaseSchema


class PiapsRecordsSchema(BaseSchema):
    id: int = Field(description="Unique identifier for the PIAPS record")
    kph_id: int = Field(description="Unique identifier for the KPH")
    kph_name: str = Field(description="Name of the KPH")
    allocation: float = Field(description="Allocation value for the PIAPS record")
    achievement: float = Field(description="Achievement value for the PIAPS record")


class PiapsRecordsCreateSchema(BaseSchema):
    kph_id: int = Field(description="Unique identifier for the KPH")
    kph_name: str = Field(description="Name of the KPH")
    allocation: float = Field(description="Allocation value for the PIAPS record")
    achievement: float = Field(description="Achievement value for the PIAPS record")


class PiapsRecordsUpdateSchema(BaseSchema):
    kph_id: Optional[int] = Field(default=None, description="Unique identifier for the KPH")
    kph_name: Optional[str] = Field(default=None, description="Name of the KPH")
    allocation: Optional[float] = Field(default=None, description="Allocation value for the PIAPS record")
    achievement: Optional[float] = Field(default=None, description="Achievement value for the PIAPS record")
