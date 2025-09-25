from ast import Dict
from typing import Any, Dict, override

from fastapi_async_sqlalchemy import db
from sqlalchemy import select

from app.core.exceptions import NotFoundException
from app.models import SettingsModel

from . import BaseRepository


class SettingsRepository(BaseRepository[SettingsModel]):
    def __init__(self, model):
        super().__init__(model)

    async def find_key(self, key: str):
        setting = await db.session.execute(select(SettingsModel).where(SettingsModel.key == key))
        return setting.scalars().first()

    @override
    async def find_all(self):
        settings = await db.session.execute(select(SettingsModel))
        return settings.scalars().all()

    @override
    async def update(self, key: str, data: Dict[str, Any]):
        setting = await self.find_key(key)
        if not setting:
            raise NotFoundException(f"Setting with key {key} not found.")
        for key, value in data.items():
            setattr(setting, key, value)
        await db.session.commit()
        return setting

    @override
    async def delete(self, key: str):
        setting = await self.find_key(key)
        if not setting:
            raise NotFoundException(f"Setting with key {key} not found.")
        await db.session.delete(setting)
        await db.session.commit()
