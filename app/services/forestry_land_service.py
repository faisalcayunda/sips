from typing import Dict, Union, override

from app.models import ForestryLandModel
from app.repositories import ForestryLandRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class ForestryLandService(BaseService[ForestryLandModel, ForestryLandRepository]):
    def __init__(self, repository: ForestryLandRepository):
        super().__init__(ForestryLandModel, repository)

    @override
    async def create(self, forestry_data: Dict[str, Union[str, int]], current_user: UserSchema) -> ForestryLandModel:
        forestry_data["created_by"] = current_user.id
        return await super().create(forestry_data)

    @override
    async def update(
        self,
        id: str,
        forestry_data: Dict[str, Union[str, int]],
        current_user: UserSchema,
    ) -> ForestryLandModel:
        forestry_data["updated_by"] = current_user.id
        return await super().update(id, forestry_data)
