from typing import Dict, Union, override

from app.models import RegionalModel
from app.repositories import RegionalRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class RegionalService(BaseService[RegionalModel, RegionalRepository]):
    def __init__(self, repository: RegionalRepository):
        super().__init__(RegionalModel, repository)

    @override
    async def create(self, regional_data: Dict[str, Union[str, int]], current_user: UserSchema) -> RegionalModel:
        regional_data["created_by"] = current_user.id
        return await super().create(regional_data)
