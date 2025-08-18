import json
from typing import Any, List, Optional, Tuple, override

from sqlalchemy import JSON, Select, String, cast, func, or_, select
from sqlalchemy.orm import aliased, joinedload, selectinload

from app.models import (
    BusinessClassModel,
    BusinessesModel,
    BusinessOperationalStatusModel,
    ForestryProposalModel,
    UserModel,
)

from . import BaseRepository


class BusinessesRepository(BaseRepository[BusinessesModel]):
    def __init__(self, model):
        super().__init__(model)

    def _mapping(self, record: dict) -> dict:
        if not record:
            return {}

        json_fields = ["account_users", "business_class", "operational_status", "forestry"]

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
        class_alias = aliased(BusinessClassModel)
        operational_status_alias = aliased(BusinessOperationalStatusModel)
        forestry_alias = aliased(ForestryProposalModel)

        account_users_subq = (
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
                    self.model.account_id,
                    "one",
                    func.cast(user_alias.id, String),
                ).isnot(None)
            )
            .correlate(self.model)
            .scalar_subquery()
        )

        business_class_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        class_alias.id,
                        "name",
                        class_alias.name,
                        "type",
                        class_alias.type,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(class_alias)
            .where(self.model.class_id == class_alias.type)
            .correlate(self.model)
            .scalar_subquery()
        )
        operational_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        operational_status_alias.id,
                        "name",
                        operational_status_alias.name,
                        "type",
                        operational_status_alias.type,
                        "notes",
                        operational_status_alias.notes,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(operational_status_alias)
            .where(self.model.operational_status_id == operational_status_alias.type)
            .correlate(self.model)
            .scalar_subquery()
        )

        def area_in_forestry_area_id_expr(forestry_area_id_col, abbreviation_col):
            return func.find_in_set(abbreviation_col, forestry_area_id_col) > 0

        forestry_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        forestry_alias.id,
                        "name",
                        forestry_alias.name,
                        "regional_id",
                        forestry_alias.regional_id,
                        "kph_account_id",
                        forestry_alias.kph_account_id,
                        "schema_id",
                        forestry_alias.schema_id,
                        "area",
                        forestry_alias.area,
                        "household_count",
                        forestry_alias.household_count,
                        "head_name",
                        forestry_alias.head_name,
                        "head_contact",
                        forestry_alias.head_contact,
                        "map_ps",
                        forestry_alias.map_ps,
                        "pps_id",
                        forestry_alias.pps_id,
                        "vertex",
                        forestry_alias.vertex,
                        "status",
                        forestry_alias.status,
                        "nagari_sk",
                        forestry_alias.nagari_sk,
                        "regent_sk",
                        forestry_alias.regent_sk,
                        "forestry_sk",
                        forestry_alias.forestry_sk,
                        "is_valid",
                        forestry_alias.is_valid,
                        "request_year",
                        forestry_alias.request_year,
                        "release_year",
                        forestry_alias.release_year,
                        "is_kps_valid",
                        forestry_alias.is_kps_valid,
                        "created_by",
                        forestry_alias.created_by,
                        "updated_by",
                        forestry_alias.updated_by,
                        "created_at",
                        forestry_alias.created_at,
                        "updated_at",
                        forestry_alias.updated_at,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(forestry_alias)
            .where(self.model.forestry_id == forestry_alias.id)
            .correlate(self.model)
            .scalar_subquery()
        )

        return (
            select(
                self.model.id.label("id"),
                self.model.status.label("status"),
                self.model.name.label("name"),
                self.model.forestry_id.label("forestry_id"),
                self.model.sk_number.label("sk_number"),
                self.model.establishment_year.label("establishment_year"),
                self.model.member_count.label("member_count"),
                self.model.chairman_name.label("chairman_name"),
                self.model.chairman_contact.label("chairman_contact"),
                self.model.latitude.label("latitude"),
                self.model.longitude.label("longitude"),
                self.model.capital_id.label("capital_id"),
                self.model.operational_status_id.label("operational_status_id"),
                self.model.operational_period_id.label("operational_period_id"),
                self.model.class_id.label("class_id"),
                self.model.is_validated.label("is_validated"),
                self.model.capital_provider_name.label("capital_provider_name"),
                self.model.capital_provision_type.label("capital_provision_type"),
                self.model.capital_provision_type_other.label("capital_provision_type_other"),
                self.model.capital_repayment_period.label("capital_repayment_period"),
                self.model.created_by.label("created_by"),
                self.model.updated_by.label("updated_by"),
                self.model.created_at.label("created_at"),
                self.model.updated_at.label("updated_at"),
                account_users_subq.label("account_users"),
                business_class_subq.label("business_class"),
                operational_subq.label("operational_status"),
                forestry_subq.label("forestry"),
            )
            .select_from(self.model)
            .outerjoin(
                class_alias,
                self.model.class_id == class_alias.id,
            )
            .outerjoin(
                operational_status_alias,
                self.model.operational_status_id == operational_status_alias.id,
            )
            .group_by(self.model.id, class_alias.id, operational_status_alias.id)
        )

    @override
    async def find_all(
        self,
        filters: Optional[List[Any]] = None,
        sort: Optional[List[Any]] = None,
        search: str = "",
        group_by: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        relationships: Optional[List[str]] = None,
        searchable_columns: Optional[List[str]] = None,
    ) -> Tuple[List[BusinessesModel], int]:
        filters = filters or []
        sort = sort or []
        relationships = relationships or []
        searchable_columns = searchable_columns or []

        query = self._build_query().filter(*filters)

        if search:
            if searchable_columns:
                search_conditions = [
                    cast(getattr(self.model, col), String).ilike(f"%{search}%")
                    for col in searchable_columns
                    if hasattr(self.model, col)
                ]
            else:
                search_conditions = [
                    cast(getattr(self.model, col_name), String).ilike(f"%{search}%")
                    for col_name in self.inspector.c.keys()
                ]

            if search_conditions:
                query = query.where(or_(*search_conditions))

        if group_by:
            query = query.group_by(getattr(self.model, group_by))

        count_query = select(func.count()).select_from(query.subquery())
        total = await self.session.scalar(count_query)
        if total is None:
            total = 0

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
        result = await self.session.execute(query)
        records_seq = result.mappings().all()
        records = [self._mapping(record) for record in records_seq]

        return records, total

    @override
    async def find_by_id(self, id: str, relationships: Optional[List[str]] = None) -> Optional[BusinessesModel]:
        query = self._build_query().where(self.model.id == id)

        if relationships:
            for rel in relationships:
                if hasattr(self.model, rel):
                    attr = getattr(self.model, rel)
                    if hasattr(attr.property, "collection_class"):
                        query = query.options(selectinload(attr))
                    else:
                        query = query.options(joinedload(attr))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()
