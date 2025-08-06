import json
from typing import List, Tuple, override

from fastapi_async_sqlalchemy import db
from sqlalchemy import Select, String, cast, func, or_, select
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import aliased, joinedload, selectinload

from app.models import (
    ForestryAreaModel,
    ForestryProposalModel,
    ProposalforestryStatusModel,
    RegionalModel,
    UserModel,
)

from . import BaseRepository


class ForestryProposalRepository(BaseRepository[ForestryProposalModel]):
    def __init__(self, model):
        super().__init__(model)

    def _build_query(self) -> Select:
        user_alias = aliased(UserModel)
        area_alias = aliased(ForestryAreaModel)

        assist_users_subq = (
            select(
                func.coalesce(
                    func.json_arrayagg(
                        func.json_object(
                            "id",
                            user_alias.id,
                            "name",
                            user_alias.name,
                            "email",
                            user_alias.email,
                            "phone",
                            user_alias.phone,
                            "agency_name",
                            user_alias.agency_name,
                            "agency_type",
                            user_alias.agency_type,
                            "avatar",
                            user_alias.avatar,
                            "enable",
                            user_alias.enable,
                            "role_id",
                            user_alias.role_id,
                            "is_verified",
                            user_alias.is_verified,
                        )
                    ),
                    func.cast("[]", JSON),
                ).label("assist_accounts")
            )
            .select_from(user_alias)
            .where(
                func.json_search(
                    ForestryProposalModel.assist_account_id,
                    "one",
                    func.cast(user_alias.id, String),
                ).isnot(None)
            )
            .where(ForestryProposalModel.id == self.model.id)
            .scalar_subquery()
        )

        area_subq = (
            select(
                func.json_arrayagg(
                    func.json_object(
                        "id",
                        area_alias.id,
                        "name",
                        area_alias.name,
                        "abbreviation",
                        area_alias.abbreviation,
                    )
                ).label("kh_detail"),
            )
            .select_from(area_alias)
            .where(
                func.json_contains(
                    ForestryProposalModel.kh_id,
                    func.json_quote(area_alias.abbreviation),
                )
            )
            .where(ForestryProposalModel.id == self.model.id)
            .scalar_subquery()
        )

        kph_accounts = (
            select(
                func.coalesce(
                    func.json_arrayagg(
                        func.json_object(
                            "id",
                            user_alias.id,
                            "name",
                            user_alias.name,
                            "email",
                            user_alias.email,
                            "phone",
                            user_alias.phone,
                            "agency_name",
                            user_alias.agency_name,
                            "agency_type",
                            user_alias.agency_type,
                            "avatar",
                            user_alias.avatar,
                            "enable",
                            user_alias.enable,
                            "role_id",
                            user_alias.role_id,
                            "is_verified",
                            user_alias.is_verified,
                        )
                    ),
                    func.cast("[]", JSON),
                ).label("kph_accounts")
            )
            .select_from(user_alias)
            .where(
                func.json_contains(
                    ForestryProposalModel.kph_account_id,
                    func.json_quote(user_alias.id),
                )
            )
            .where(ForestryProposalModel.id == self.model.id)
            .scalar_subquery()
        )

        return (
            select(
                self.model.id.label("id"),
                self.model.regional_id.label("regional_id"),
                self.model.assist_account_id.label("assist_account_id"),
                self.model.name.label("name"),
                self.model.schema_id.label("schema_id"),
                self.model.kph_account_id.label("kph_account_id"),
                self.model.kh_id.label("kh_id"),
                self.model.akps_id.label("akps_id"),
                self.model.area.label("area"),
                self.model.household_count.label("household_count"),
                self.model.head_name.label("head_name"),
                self.model.head_contact.label("head_contact"),
                self.model.map_ps.label("map_ps"),
                self.model.pps_id.label("pps_id"),
                self.model.vertex.label("vertex"),
                self.model.status.label("status"),
                self.model.nagari_sk.label("nagari_sk"),
                self.model.regent_sk.label("regent_sk"),
                self.model.forestry_sk.label("forestry_sk"),
                self.model.is_valid.label("is_valid"),
                self.model.request_year.label("request_year"),
                self.model.release_year.label("release_year"),
                self.model.is_kps_valid.label("is_kps_valid"),
                self.model.created_by.label("created_by"),
                self.model.updated_by.label("updated_by"),
                self.model.created_at.label("created_at"),
                self.model.updated_at.label("updated_at"),
                assist_users_subq.label("assist_accounts"),
                area_subq.label("kh_detail"),
                func.json_object(
                    "id",
                    ProposalforestryStatusModel.id,
                    "name",
                    ProposalforestryStatusModel.name,
                    "proposal_forestry_vertex",
                    ProposalforestryStatusModel.proposal_forestry_vertex,
                    "description",
                    ProposalforestryStatusModel.description,
                ).label("vertex_detail"),
                kph_accounts.label("kph_accounts"),
                func.json_object(
                    "id",
                    RegionalModel.id,
                    "name",
                    RegionalModel.name,
                    "parent",
                    RegionalModel.parent,
                    "group",
                    RegionalModel.group,
                    "created_at",
                    RegionalModel.created_at,
                    "created_by",
                    RegionalModel.created_by,
                ).label("regional"),
            )
            .select_from(self.model)
            .outerjoin(
                ProposalforestryStatusModel,
                self.model.vertex == ProposalforestryStatusModel.proposal_forestry_vertex,
            )
            .outerjoin(
                RegionalModel,
                self.model.regional_id == RegionalModel.id,
            )
        )

    @override
    async def find_by_id(self, id: int, relationships: List[str] = None) -> ForestryProposalModel:
        query = self._build_query()
        result = await db.session.execute(query.where(self.model.id == id))
        result = result.mappings().first()
        if result:
            result = dict(result)
            if result.get("regional"):
                result["regional"] = json.loads(result["regional"])
            if result.get("vertex_detail"):
                result["vertex_detail"] = json.loads(result["vertex_detail"])
            if result.get("kh_detail"):
                result["kh_detail"] = json.loads(result["kh_detail"])
            if result.get("kph_accounts"):
                result["kph_accounts"] = json.loads(result["kph_accounts"])

        return result

    @override
    async def find_all(
        self,
        filters: list = ...,
        sort: list = ...,
        search: str = "",
        group_by: str = None,
        limit: int = 100,
        offset: int = 0,
        relationships: List[str] = None,
        searchable_columns: List[str] = None,
    ) -> Tuple[List[ForestryProposalModel], int]:

        query = self._build_query()

        if search:
            if searchable_columns:
                search_conditions = []
                for col in searchable_columns:
                    if hasattr(self.model, col):
                        search_conditions.append(cast(getattr(self.model, col), String).ilike(f"%{search}%"))

            else:
                searchable_fields = [
                    self.model.id,
                    self.model.name,
                    self.model.head_name,
                    self.model.head_contact,
                    self.model.map_ps,
                    self.model.nagari_sk,
                    self.model.regent_sk,
                    self.model.forestry_sk,
                    self.model.request_year,
                    self.model.release_year,
                ]
                search_conditions = [cast(field, String).ilike(f"%{search}%") for field in searchable_fields]

            if search_conditions:
                query = query.where(or_(*search_conditions))

        if group_by:
            # Try to get model field, either directly or through mapping
            if hasattr(self.model, group_by):
                query = query.group_by(getattr(self.model, group_by))
            else:
                # Try to map table column name to model field
                model_field = self.get_model_field(group_by)
                if model_field:
                    query = query.group_by(model_field)
                # If no mapping found, skip group_by

        count_query = select(func.count()).select_from(query.subquery())
        total = await db.session.scalar(count_query)

        if sort:
            query = query.order_by(*sort)
        else:
            query = query.order_by(self.model.id)

        if relationships:
            for rel in relationships:
                if hasattr(self.model, rel):
                    attr = getattr(self.model, rel)
                    if hasattr(attr.property, "collection_class"):
                        query = query.options(selectinload(attr))
                    else:
                        query = query.options(joinedload(attr))

        query = query.limit(limit).offset(offset)
        result = await db.session.execute(query)

        records = result.mappings().all()
        results_dict = []
        print("RECORDS", records)
        for record in records:
            temp = dict(record)
            if temp.get("regional"):
                temp["regional"] = json.loads(temp["regional"])
            if temp.get("vertex_detail"):
                temp["vertex_detail"] = json.loads(temp["vertex_detail"])
            if temp.get("kh_detail"):
                temp["kh_detail"] = json.loads(temp["kh_detail"])
            if temp.get("kph_accounts"):
                temp["kph_accounts"] = json.loads(temp["kph_accounts"])

            results_dict.append(temp)

        return results_dict, total

    @override
    async def create(self, data: dict) -> ForestryProposalModel:
        result = await super().create(data)

        return await self.find_by_id(result.id)

    @override
    async def update(self, id: int, data: dict, refresh: bool = True) -> ForestryProposalModel:
        result = await super().update(id, data)

        return await self.find_by_id(result["id"])
