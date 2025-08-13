import json
from typing import List, Tuple, override

from fastapi_async_sqlalchemy import db
from sqlalchemy import Integer, Select, String, cast, func, or_, select
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import aliased, joinedload, selectinload

from app.models import (
    ForestryAreaModel,
    ForestryProposalModel,
    ProposalforestryStatusModel,
    RegionalModel,
    UserModel,
)
from app.models.forestry_schema_model import ForestrySchemaModel

from . import BaseRepository


class ForestryProposalRepository(BaseRepository[ForestryProposalModel]):
    def __init__(self, model):
        super().__init__(model)

    def _mapping(self, record: dict) -> dict:
        if not record:
            return {}

        json_fields = [
            "regional",
            "vertex_detail",
            "kh_detail",
            "kph_account",
            "schema",
            "assist_accounts",
        ]

        temp = dict(record)
        for field in json_fields:
            value = temp.get(field)
            if isinstance(value, str):
                try:
                    temp[field] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    temp[field] = value

        return temp

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
                )
            )
            .select_from(user_alias)
            .where(
                func.json_search(
                    self.model.assist_account_id,
                    "one",
                    func.cast(user_alias.id, String),
                ).isnot(None)
            )
            .correlate(self.model)
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
                )
            )
            .select_from(area_alias)
            .where(
                func.json_contains(
                    self.model.kh_id,
                    func.json_quote(area_alias.abbreviation),
                )
            )
            .correlate(self.model)
            .scalar_subquery()
        )

        return (
            select(
                self.model.id.label("id"),
                func.min(self.model.regional_id).label("regional_id"),
                func.min(self.model.assist_account_id).label("assist_account_id"),
                func.min(self.model.name).label("name"),
                func.min(self.model.schema_id).label("schema_id"),
                func.min(self.model.kph_account_id).label("kph_account_id"),
                func.min(self.model.kh_id).label("kh_id"),
                func.min(self.model.area).label("area"),
                func.min(self.model.household_count).label("household_count"),
                func.min(self.model.head_name).label("head_name"),
                func.min(self.model.head_contact).label("head_contact"),
                func.min(self.model.map_ps).label("map_ps"),
                func.min(self.model.pps_id).label("pps_id"),
                func.min(self.model.vertex).label("vertex"),
                func.min(self.model.status).label("status"),
                func.min(self.model.nagari_sk).label("nagari_sk"),
                func.min(self.model.regent_sk).label("regent_sk"),
                func.min(self.model.forestry_sk).label("forestry_sk"),
                func.min(self.model.is_valid).label("is_valid"),
                func.min(self.model.request_year).label("request_year"),
                func.min(self.model.release_year).label("release_year"),
                func.min(self.model.is_kps_valid).label("is_kps_valid"),
                func.min(self.model.created_by).label("created_by"),
                func.min(self.model.updated_by).label("updated_by"),
                func.min(self.model.created_at).label("created_at"),
                func.min(self.model.updated_at).label("updated_at"),
                assist_users_subq.label("assist_accounts"),
                area_subq.label("kh_detail"),
                func.json_object(
                    "id",
                    func.min(ProposalforestryStatusModel.id),
                    "name",
                    func.min(ProposalforestryStatusModel.name),
                    "proposal_forestry_vertex",
                    func.min(ProposalforestryStatusModel.proposal_forestry_vertex),
                    "description",
                    func.min(ProposalforestryStatusModel.description),
                ).label("vertex_detail"),
                func.json_object(
                    "id",
                    func.min(user_alias.id),
                    "name",
                    func.min(user_alias.name),
                    "email",
                    func.min(user_alias.email),
                    "phone",
                    func.min(user_alias.phone),
                    "agency_name",
                    func.min(user_alias.agency_name),
                    "agency_type",
                    func.min(user_alias.agency_type),
                    "avatar",
                    func.min(user_alias.avatar),
                    "enable",
                    func.min(user_alias.enable),
                    "role_id",
                    func.min(user_alias.role_id),
                    "is_verified",
                    func.min(user_alias.is_verified),
                ).label("kph_account"),
                func.json_object(
                    "id",
                    func.min(RegionalModel.id),
                    "name",
                    func.min(RegionalModel.name),
                    "parent",
                    func.min(RegionalModel.parent),
                    "group",
                    func.min(RegionalModel.group),
                    "created_at",
                    func.min(RegionalModel.created_at),
                    "created_by",
                    func.min(RegionalModel.created_by),
                ).label("regional"),
                func.json_object(
                    "schema_id",
                    func.min(ForestrySchemaModel.schema_id),
                    "name",
                    func.min(ForestrySchemaModel.name),
                    "description",
                    func.min(ForestrySchemaModel.description),
                    "ord",
                    func.min(ForestrySchemaModel.ord),
                ).label("schema"),
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
            .outerjoin(
                ForestrySchemaModel,
                self.model.schema_id == ForestrySchemaModel.schema_id,
            )
            .outerjoin(
                user_alias,
                self.model.kph_account_id == user_alias.id,
            )
            .group_by(self.model.id)
        )

    @override
    async def find_by_id(self, id: int, relationships: List[str] = None) -> ForestryProposalModel:
        query = self._build_query()
        result = await db.session.execute(query.where(self.model.id == id))
        result = result.mappings().first()

        return self._mapping(result)

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
        results_dict = [self._mapping(record) for record in records]

        return results_dict, total

    @override
    async def create(self, data: dict) -> ForestryProposalModel:
        stmt = select(func.max(cast(self.model.id, Integer))).where(self.model.id.op("regexp")("^[0-9]+$"))
        result = await db.session.execute(stmt)
        max_id = result.scalar() or 0
        data["id"] = str(max_id + 1)
        result = await super().create(data)
        return await self.find_by_id(result.id)

    @override
    async def update(self, id: int, data: dict, refresh: bool = True) -> ForestryProposalModel:
        print("Data to update", data)
        result = await super().update(id, data, refresh)

        return await self.find_by_id(result["id"])
