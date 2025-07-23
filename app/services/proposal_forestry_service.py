from typing import Dict, Union, override

from app.models import ForestryProposalModel
from app.repositories import ForestryProposalRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class ForestyProposalService(BaseService[ForestryProposalModel, ForestryProposalRepository]):
    def __init__(self, repository: ForestryProposalRepository):
        super().__init__(ForestryProposalModel, repository)

    @override
    async def create(
        self, forestry_data: Dict[str, Union[str, int]], current_user: UserSchema
    ) -> ForestryProposalModel:
        forestry_data["created_by"] = current_user.id
        return await super().create(forestry_data)

    @override
    async def update(
        self,
        id: str,
        forestry_data: Dict[str, Union[str, int]],
        current_user: UserSchema,
    ) -> ForestryProposalModel:
        forestry_data["updated_by"] = current_user.id
        return await super().update(id, forestry_data)
