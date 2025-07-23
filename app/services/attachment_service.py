from typing import override

from app.models import AttachmentModel
from app.repositories import AttachmentRepository
from app.schemas.user_schema import UserSchema

from .base import BaseService


class AttachmentService(BaseService[AttachmentModel, AttachmentRepository]):
    def __init__(self, repository: AttachmentRepository):
        super().__init__(AttachmentModel, repository)

    @override
    async def create(self, attachment_data: dict, current_user: UserSchema) -> AttachmentModel:
        attachment_data["created_by"] = current_user.id
        return await super().create(attachment_data)

    @override
    async def update(self, id: int, attachment_data: dict, current_user: UserSchema) -> AttachmentModel:
        attachment_data["updated_by"] = current_user.id
        return await super().update(id, attachment_data)
