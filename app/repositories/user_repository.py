import logging

from fastapi_async_sqlalchemy import db
from sqlalchemy import String, cast, or_, select

from app.models import PermitModel, RolesModel, UserModel
from app.models.navigation_model import NavigationModel

from . import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, model):
        super().__init__(model)

    async def find_by_username(self, username: str) -> UserModel | None:
        query = select(self.model).filter(self.model.name == username)
        result = await db.session.execute(query)
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> UserModel | None:
        query = select(self.model).filter(self.model.email == email)
        result = await db.session.execute(query)
        return result.scalar_one_or_none()

    async def find_by_id_with_permissions(self, id: str):
        user_query = select(
            self.model.id.label("id"),
            self.model.name.label("name "),
            self.model.address.label("address"),
            self.model.phone.label("phone"),
            self.model.gender.label("gender"),
            self.model.agency_name.label("agency_name"),
            self.model.agency_type.label("agency_type"),
            self.model.file.label("file"),
            self.model.avatar.label("avatar"),
            self.model.email.label("email"),
            self.model.password.label("password"),
            self.model.enable.label("enable"),
            self.model.last_login.label("last_login"),
            self.model.role_id.label("role_id"),
        ).where(self.model.id == id)

        user_result = await db.session.execute(user_query)
        user_row = user_result.mappings().first()
        if not user_row:
            return None

        role_query = select(
            RolesModel.id.label("id"),
            RolesModel.name.label("name"),
        ).where(RolesModel.id == user_row["role_id"])
        role_result = await db.session.execute(role_query)
        role_row = role_result.mappings().first()
        if not role_row:
            role = None
        else:
            permissions_query = (
                select(
                    NavigationModel.id.label("id"),
                    NavigationModel.name.label("name"),
                    NavigationModel.parent.label("parent"),
                    NavigationModel.is_enabled.label("is_enabled"),
                    NavigationModel.icon.label("icon"),
                    NavigationModel.url.label("url"),
                    NavigationModel.sort_order.label("sort_order"),
                    NavigationModel.sign.label("sign"),
                    PermitModel.permit_content.label("permit_content"),
                )
                .select_from(PermitModel)
                .join(
                    NavigationModel,
                    NavigationModel.id == PermitModel.navigation_id,
                )
                .where(
                    PermitModel.role_id == role_row["id"],
                    or_(
                        PermitModel.permit_content["read"].is_(True),
                        PermitModel.permit_content["create"].is_(True),
                        PermitModel.permit_content["update"].is_(True),
                        PermitModel.permit_content["delete"].is_(True),
                        cast(PermitModel.permit_content["read"], String) == "true",
                        cast(PermitModel.permit_content["create"], String) == "true",
                        cast(PermitModel.permit_content["update"], String) == "true",
                        cast(PermitModel.permit_content["delete"], String) == "true",
                    ),
                )
            )
            permissions_result = await db.session.execute(permissions_query)
            permissions = []
            for row in permissions_result.mappings().all():
                permission_dict = dict(row)
                permit_content = permission_dict.pop("permit_content", {})

                def normalize_permission(value):
                    if isinstance(value, bool):
                        return value
                    elif isinstance(value, str):
                        return value.lower() == "true"
                    else:
                        return False

                permission_dict["permissions"] = {
                    "read": normalize_permission(permit_content.get("read", False)),
                    "create": normalize_permission(permit_content.get("create", False)),
                    "update": normalize_permission(permit_content.get("update", False)),
                    "delete": normalize_permission(permit_content.get("delete", False)),
                }
                permissions.append(permission_dict)

            logger.info(f"Found {len(permissions)} permissions for role {role_row['id']}")

            role = {
                "id": role_row["id"],
                "name": role_row["name"],
                "navigations": permissions,
            }

        user_dict = dict(user_row)
        user_dict.pop("role_id", None)
        user_dict["role"] = role

        return user_dict
