from typing import Dict, Union, override

from app.models import PermitModel
from app.repositories import PermitRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class PermitService(BaseService[PermitModel, PermitRepository]):
    def __init__(self, repository: PermitRepository):
        super().__init__(PermitModel, repository)

    @override
    async def create(self, permit_data: Dict[str, Union[str, int]], current_user: UserSchema) -> PermitModel:
        permit_data["created_by"] = current_user.id
        return await super().create(permit_data)

    @override
    async def update(
        self,
        id: str,
        permit_data: Dict[str, Union[str, int]],
        current_user: UserSchema,
    ) -> PermitModel:
        permit_data["updated_by"] = current_user.id
        return await super().update(id, permit_data)
