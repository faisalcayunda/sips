from typing import Any, Dict, override

from app.models import BusinessesModel
from app.repositories import BusinessesRepository
from app.schemas.user_schema import UserSchema
from app.utils.helpers import export_to_xlsx

from . import BaseService


class BusinessesService(BaseService[BusinessesModel, BusinessesRepository]):
    def __init__(self, repository: BusinessesRepository):
        super().__init__(BusinessesModel, repository)

    @override
    async def create(self, data: Dict[str, Any], current_user: UserSchema) -> BusinessesModel:
        data["created_by"] = current_user.id
        return await super().create(data)

    @override
    async def update(self, id: str, data: Dict[str, Any], current_user: UserSchema) -> BusinessesModel:
        data["updated_by"] = current_user.id
        return await super().update(id, data)

    async def export_to_excel(
        self,
        filters: list = [],
        sort: list = [],
        search: str = "",
        group_by: str = None,
        limit: int = 0,
        offset: int = 0,
        relationships: list = [],
        searchable_columns: list = [],
    ) -> bytes:

        businesses_data, _ = await self.repository.find_all(
            filters=filters,
            sort=sort,
            search=search,
            group_by=group_by,
            limit=limit,
            offset=offset,
            relationships=relationships,
            searchable_columns=searchable_columns,
            all=True,
        )

        # Header sesuai gambar dan model
        data = [
            [
                "No",
                "Nama KUPS",
                "Kelas KUPS",
                "Nama KPS",
                "Nama KPH",
                "Komoditas",
                "Dibuat",
                "Diperbarui",
            ]
        ]

        for idx, item in enumerate(businesses_data, start=1):
            # Defensive: handle possible None for nested dicts (patokannya ke find_all mapping)
            business_class = item.get("business_class") or item.get("class") or {}
            forestry = item.get("forestry") or {}
            kph_account = forestry.get("kph_account") or {}

            # Komoditas bisa berupa list of dict, string, atau None
            commodities = item.get("commodities", "")
            if isinstance(commodities, list):
                # Jika list of dict, ambil field 'name' jika ada
                commodities_str = ", ".join(
                    c.get("name", "") if isinstance(c, dict) else str(c) for c in commodities if c
                )
            elif isinstance(commodities, dict):
                # Jika dict, ambil field 'name'
                commodities_str = commodities.get("name", "")
            else:
                # Jika string atau None
                commodities_str = str(commodities) if commodities else ""

            data.append(
                [
                    idx,
                    item.get("name", ""),
                    business_class.get("name", ""),
                    forestry.get("name", ""),
                    kph_account.get("name", ""),
                    commodities_str,
                    (item.get("created_at", "").strftime("%d-%m-%Y") if item.get("created_at") else ""),
                    (item.get("updated_at", "").strftime("%d-%m-%Y") if item.get("updated_at") else ""),
                ]
            )

        return export_to_xlsx(data, sheet_name="kups")
