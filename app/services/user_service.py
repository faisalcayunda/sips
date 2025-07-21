from typing import Dict, List, Tuple, Union, override

from fastapi import HTTPException, status
from uuid6 import UUID

from app.core.exceptions import NotFoundException
from app.core.security import get_password_hash
from app.models import UserModel
from app.repositories import UserRepository
from app.schemas.user_schema import UserSchema

from . import BaseService


class UserService(BaseService[UserModel, UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(UserModel, repository)
        self.forbidden_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this resource",
        )

    @override
    async def create(
        self, user_data: Dict[str, Union[str, int]], current_user: UserSchema
    ) -> UserModel:
        if await self.repository.find_by_username(user_data["name"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        if await self.repository.find_by_email(user_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        user_data["password"] = get_password_hash(user_data["password"])
        user_data["create_by"] = current_user.id
        return await self.repository.create(user_data)

    @override
    async def update(
        self, id: int, user_data: Dict[str, Union[str, int]], current_user
    ) -> UserModel:
        user = await self.repository.find_by_id(id)
        if not user:
            raise NotFoundException("User not found")
        if user_data.get("name") and await self.repository.find_by_username(
            user_data["name"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        if user_data.get("email") and await self.repository.find_by_email(
            user_data["email"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

        if user_data.get("password"):
            user_data["password"] = get_password_hash(user_data["password"])

        user_data["update_by"] = current_user.id
        return await self.repository.update(id, user_data)
