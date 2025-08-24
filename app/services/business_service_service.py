from typing import Any, Dict, override

from app.models import BusinessServiceModel
from app.repositories import BusinessServiceRepository
from app.schemas import UserSchema

from . import BaseService


class BusinessServiceService(BaseService[BusinessServiceModel, BusinessServiceRepository]):
    def __init__(self, repository: BusinessServiceRepository):
        super().__init__(BusinessServiceModel, repository)

    @override
    async def create(self, data: Dict[str, Any], current_user: UserSchema) -> BusinessServiceModel:
        data["created_by"] = current_user.id
        return await super().create(data)

    @override
    async def update(
        self, id: str, data: Dict[str, Any], current_user: UserSchema, refresh: bool = True
    ) -> BusinessServiceModel:
        data["updated_by"] = current_user.id
        return await super().update(id, data, refresh=refresh)
