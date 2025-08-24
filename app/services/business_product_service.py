from typing import Any, Dict, override

from app.models import BusinessProductModel
from app.repositories import BusinessProductRepository
from app.schemas import UserSchema

from . import BaseService


class BusinessProductService(BaseService[BusinessProductModel, BusinessProductRepository]):
    def __init__(self, repository: BusinessProductRepository):
        super().__init__(BusinessProductModel, repository)

    @override
    async def create(self, data: Dict[str, Any], current_user: UserSchema) -> BusinessProductModel:
        data["created_by"] = current_user.id
        return await super().create(data)

    @override
    async def update(
        self, id: str, data: Dict[str, Any], current_user: UserSchema, refresh: bool = True
    ) -> BusinessProductModel:
        data["updated_by"] = current_user.id
        return await super().update(id, data, refresh=refresh)
