from typing import Dict, Union, override

from app.models import NavigationModel
from app.repositories import NavigationRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class NavigationService(BaseService[NavigationModel, NavigationRepository]):
    def __init__(self, repository: NavigationRepository):
        super().__init__(NavigationModel, repository)

    @override
    async def create(self, navigation_data: Dict[str, Union[str, int]], current_user: UserSchema) -> NavigationModel:
        navigation_data["created_by"] = current_user.id
        return await super().create(navigation_data)

    @override
    async def update(
        self,
        id: str,
        navigation_data: Dict[str, Union[str, int]],
        current_user: UserSchema,
    ) -> NavigationModel:
        navigation_data["updated_by"] = current_user.id
        return await super().update(id, navigation_data)
