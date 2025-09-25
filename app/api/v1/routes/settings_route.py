from typing import List

from fastapi import APIRouter, Body, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.schemas import (
    SettingsCreateSchema,
    SettingsResponseSchema,
    SettingsUpdateSchema,
)
from app.schemas.base import PaginatedResponse
from app.services import SettingsService

router = APIRouter()


@router.get("/settings", response_model=List[SettingsResponseSchema])
async def get_settings_list(
    service: SettingsService = Depends(Factory().get_settings_service),
):
    settings_list = await service.find_all()
    return [SettingsResponseSchema.model_validate(settings) for settings in settings_list]


@router.post(
    "/settings",
    response_model=PaginatedResponse[SettingsResponseSchema],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_active_user)],
)
async def create_settings(
    data: SettingsCreateSchema = Body(...),
    service: SettingsService = Depends(Factory().get_settings_service),
):
    return await service.create(data.model_dump())


@router.patch(
    "/settings/{key}",
    dependencies=[Depends(get_current_active_user)],
)
async def update_settings(
    key: str,
    data: SettingsUpdateSchema = Body(...),
    service: SettingsService = Depends(Factory().get_settings_service),
):
    return await service.update(key, data.model_dump(exclude_unset=True))


@router.delete(
    "/settings/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_settings(
    key: str,
    service: SettingsService = Depends(Factory().get_settings_service),
):
    await service.delete(key)
