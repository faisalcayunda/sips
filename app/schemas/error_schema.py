from .base import BaseSchema


class ErrorResponse(BaseSchema):
    message: str
