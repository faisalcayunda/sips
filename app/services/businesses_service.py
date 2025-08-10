from typing import Any, Dict, override

from app.models import BusinessesModel
from app.repositories import BusinessesRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class BusinessesService(BaseService[BusinessesModel, BusinessesRepository]):
    def __init__(self, repository: BusinessesRepository):
        super().__init__(BusinessesModel, repository)

    @override
    async def create(self, data: Dict[str, Any], current_user: UserSchema) -> BusinessesModel:
        data["created_by"] = current_user.id
        return await super().create(data)

    @override
    async def update(self, id: str, data: Dict[str, Any], current_user: UserSchema) -> BusinessesModel:
        data["updated_by"] = current_user.id
        return await super().update(id, data)
