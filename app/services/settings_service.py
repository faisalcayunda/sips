from ast import Dict
from typing import Any, override

from app.models import SettingsModel
from app.repositories import SettingsRepository

from . import BaseService


class SettingsService(BaseService[SettingsModel, SettingsRepository]):
    def __init__(self, repository: SettingsRepository):
        super().__init__(SettingsModel, repository)

    @override
    async def find_all(self):
        return await self.repository.find_all()

    @override
    async def update(self, key: str, data: Dict[str, Any]):
        return await self.repository.update(key, data)

    @override
    async def delete(self, key: str):
        return await self.repository.delete(key)
