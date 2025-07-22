from datetime import datetime
from typing import Optional

from pydantic import EmailStr, Field, field_validator

from app.core.exceptions import UnprocessableEntity

from .base import BaseSchema


# Disesuaikan dengan struktur user_model.py
class UserSchema(BaseSchema):
    id: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    agency_name: Optional[str] = None
    agency_type: Optional[str] = None
    file: Optional[str] = None
    avatar: Optional[str] = None
    email: EmailStr
    enable: bool = True
    role_id: Optional[int] = None
    last_login: Optional[datetime] = None
    create_by: Optional[str] = None
    update_by: Optional[int] = None
    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class UserCreateSchema(BaseSchema):
    id: str
    name: str = Field(..., min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=10)
    agency_name: Optional[str] = Field(None, max_length=255)
    agency_type: Optional[str] = Field(None, max_length=100)
    file: Optional[str] = Field(None, max_length=255)
    avatar: Optional[str] = Field(None, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    enable: bool = True
    role_id: Optional[int] = Field(None)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None:
            return value
        has_letter = any(c.isalpha() for c in value)
        has_digit = any(c.isdigit() for c in value)
        has_special = any(c in "@$!%*#?&" for c in value)
        if not (has_letter and has_digit and has_special):
            raise UnprocessableEntity(
                "Password must be at least 8 characters long and contain at least one letter, one number, and one special character"
            )
        return value

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value):
        if value is None:
            return value
        # Validasi tambahan untuk domain email jika diperlukan
        # domain = value.split("@")[1]
        # valid_domains = ["gmail.com", "yahoo.com", "hotmail.com", "company.com"]
        # if domain not in valid_domains:
        #     raise UnprocessableEntity(f'Domain email tidak valid. Domain yang diizinkan: {", ".join(valid_domains)}')
        return value


class UserUpdateSchema(BaseSchema):
    id: Optional[str] = Field(None, min_length=2, max_length=100)
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=10)
    agency_name: Optional[str] = Field(None, max_length=255)
    agency_type: Optional[str] = Field(None, max_length=100)
    file: Optional[str] = Field(None, max_length=255)
    avatar: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)
    enable: Optional[bool] = None
    role_id: Optional[int] = Field(None)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is None:
            return value
        has_letter = any(c.isalpha() for c in value)
        has_digit = any(c.isdigit() for c in value)
        has_special = any(c in "@$!%*#?&" for c in value)
        if not (has_letter and has_digit and has_special):
            raise UnprocessableEntity(
                "Password must be at least 8 characters long and contain at least one letter, one number, and one special character"
            )
        return value

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value):
        if value is None:
            return value
        # Validasi tambahan untuk domain email jika diperlukan
        # domain = value.split("@")[1]
        # valid_domains = ["gmail.com", "yahoo.com", "hotmail.com", "company.com"]
        # if domain not in valid_domains:
        #     raise UnprocessableEntity(f'Domain email tidak valid. Domain yang diizinkan: {", ".join(valid_domains)}')
        return value
