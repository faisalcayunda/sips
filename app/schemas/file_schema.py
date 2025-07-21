from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import BaseSchema
from .user_schema import UserSchema


class FileSchema(BaseSchema):
    id: int
    object_name: str
    uploaded_by: UserSchema
    created_at: datetime
    modified_at: Optional[datetime] = None


class FileCreateSchema(BaseSchema):
    filename: str
    content_type: str
    size: int
    description: Optional[str] = None
    url: str


class FileUpdateSchema(BaseSchema):
    filename: Optional[str] = Field(None, title="File Name")
    content_type: Optional[str] = Field(None, title="Content Type")
    size: Optional[int] = Field(None, title="File Size")
    description: Optional[str] = Field(None, title="File Description")
    url: Optional[str] = Field(None, title="File URL")
