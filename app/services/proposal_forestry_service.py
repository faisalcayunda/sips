from typing import Dict, List, Optional, Union, override

from app.models import ForestryProposalModel
from app.repositories import ForestryProposalRepository
from app.schemas.user_schema import UserSchema
from app.utils.helpers import export_to_xlsx

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
        refresh: bool = True,
    ) -> ForestryProposalModel:
        forestry_data["updated_by"] = current_user.id
        return await super().update(id, forestry_data, refresh)

    async def export_to_excel(
        self,
        filters: Optional[Union[str, List[str]]] = None,
        sort: Optional[Union[str, List[str]]] = None,
        search: str = "",
        group_by: Optional[str] = None,
        limit: int = 0,
        offset: int = 0,
        relationships: Optional[List[str]] = None,
        searchable_columns: Optional[List[str]] = None,
    ) -> bytes:

        forestry_data, _ = await self.repository.find_all(
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

        data = [
            [
                "No",
                "Nama PPS",
                "Lokasi Kabupaten",
                "Nama KPH",
                "Skema PS",
                "Luas PS",
                "Status Proses",
                "Dibuat",
                "Diperbarui",
            ]
        ]
        for idx, item in enumerate(forestry_data, start=1):
            data.append(
                [
                    idx,
                    item.get("name", ""),
                    (item.get("regional") or {}).get("name", ""),
                    (item.get("kph_account") or {}).get("name", ""),
                    (item.get("schema") or {}).get("name", ""),
                    item.get("area", ""),
                    item.get("status", ""),
                    (item.get("created_at", "").strftime("%d-%m-%Y") if item.get("created_at") else ""),
                    (item.get("updated_at", "").strftime("%d-%m-%Y") if item.get("updated_at") else ""),
                ]
            )

        return export_to_xlsx(data, sheet_name="proposal_kehutanan")
