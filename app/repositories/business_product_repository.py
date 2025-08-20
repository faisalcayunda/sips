import json
from typing import Any, Dict, List, Optional, Tuple, override

from sqlalchemy import JSON, Select, String, cast, func, or_, select
from sqlalchemy.orm import aliased, joinedload, selectinload

from app.models import (
    BusinessClassModel,
    BusinessesModel,
    BusinessHarvestModel,
    BusinessOperationalStatusModel,
    BusinessProductModel,
    CommodityModel,
    ForestryProposalModel,
    UserModel,
)

from . import BaseRepository


class BusinessProductRepository(BaseRepository[BusinessProductModel]):
    def __init__(self, model):

        super().__init__(model)

    def _mapping(self, record: dict) -> dict:
        if not record:
            return {}

        json_fields = ["business", "commodity", "harvest"]

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
        business_alias = aliased(BusinessesModel, name="business_alias")
        commodity_alias = aliased(CommodityModel, name="commodity_alias")
        harvest_alias = aliased(BusinessHarvestModel, name="harvest_alias")

        # Build nested JSON subqueries for business
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
            .where(func.json_contains(business_alias.account_ids, func.json_quote(func.cast(user_alias.id, String))))
            .correlate(business_alias)
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
            .where(business_alias.class_id == class_alias.type)
            .correlate(business_alias)
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
            .where(business_alias.operational_status_id == operational_status_alias.type)
            .correlate(business_alias)
            .scalar_subquery()
        )

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
            .where(business_alias.forestry_id == forestry_alias.id)
            .correlate(business_alias)
            .scalar_subquery()
        )

        business_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        business_alias.id,
                        "status",
                        business_alias.status,
                        "name",
                        business_alias.name,
                        "forestry_id",
                        business_alias.forestry_id,
                        "sk_number",
                        business_alias.sk_number,
                        "establishment_year",
                        business_alias.establishment_year,
                        "member_count",
                        business_alias.member_count,
                        "chairman_name",
                        business_alias.chairman_name,
                        "chairman_contact",
                        business_alias.chairman_contact,
                        "latitude",
                        business_alias.latitude,
                        "longitude",
                        business_alias.longitude,
                        "capital_id",
                        business_alias.capital_id,
                        "operational_status_id",
                        business_alias.operational_status_id,
                        "operational_period_id",
                        business_alias.operational_period_id,
                        "class_id",
                        business_alias.class_id,
                        "is_validated",
                        business_alias.is_validated,
                        "capital_provider_name",
                        business_alias.capital_provider_name,
                        "capital_provision_type",
                        business_alias.capital_provision_type,
                        "capital_provision_type_other",
                        business_alias.capital_provision_type_other,
                        "capital_repayment_period",
                        business_alias.capital_repayment_period,
                        "created_by",
                        business_alias.created_by,
                        "updated_by",
                        business_alias.updated_by,
                        "created_at",
                        business_alias.created_at,
                        "updated_at",
                        business_alias.updated_at,
                        "account_users",
                        account_users_subq,
                        "business_class",
                        business_class_subq,
                        "operational_status",
                        operational_subq,
                        "forestry",
                        forestry_subq,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(business_alias)
            .where(self.model.business_id == business_alias.id)
            .correlate(self.model)
            .scalar_subquery()
        )

        commodity_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        commodity_alias.id,
                        "name",
                        commodity_alias.name,
                        "local_name",
                        commodity_alias.local_name,
                        "latin_name",
                        commodity_alias.latin_name,
                        "type_code",
                        commodity_alias.type_code,
                        "description",
                        commodity_alias.description,
                        "photo",
                        commodity_alias.photo,
                        "status",
                        commodity_alias.status,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(commodity_alias)
            .where(self.model.commodity_id == commodity_alias.id)
            .correlate(self.model)
            .scalar_subquery()
        )

        harvest_subq = (
            select(
                func.coalesce(
                    func.json_object(
                        "id",
                        harvest_alias.id,
                        "harvest_code",
                        harvest_alias.harvest_code,
                        "name",
                        harvest_alias.name,
                        "note",
                        harvest_alias.note,
                    ),
                    func.cast("{}", JSON),
                )
            )
            .select_from(harvest_alias)
            .where(self.model.harvest_id == harvest_alias.id)
            .correlate(self.model)
            .scalar_subquery()
        )

        return (
            select(
                self.model.id.label("id"),
                self.model.name.label("name"),
                self.model.description.label("description"),
                self.model.beneficiary_count.label("beneficiary_count"),
                self.model.manufacture_code.label("manufacture_code"),
                self.model.latitude.label("latitude"),
                self.model.longitude.label("longitude"),
                self.model.area_managed.label("area_managed"),
                self.model.area_planned.label("area_planned"),
                self.model.area_productive.label("area_productive"),
                self.model.area_unit.label("area_unit"),
                self.model.harvest_production.label("harvest_production"),
                self.model.harvest_unit.label("harvest_unit"),
                self.model.type_id.label("type_id"),
                self.model.tools_available.label("tools_available"),
                self.model.tools_detail.label("tools_detail"),
                self.model.price_sell.label("price_sell"),
                self.model.buyer_type_id.label("buyer_type_id"),
                self.model.buyer_count.label("buyer_count"),
                self.model.sales_freq_id.label("sales_freq_id"),
                self.model.export_status_id.label("export_status_id"),
                self.model.export_purpose.label("export_purpose"),
                self.model.seedstock_availability.label("seedstock_availability"),
                self.model.unit_price_label.label("unit_price_label"),
                self.model.unit_sold_label.label("unit_sold_label"),
                self.model.buyer_target.label("buyer_target"),
                self.model.created_by.label("created_by"),
                self.model.created_at.label("created_at"),
                self.model.updated_by.label("updated_by"),
                self.model.updated_at.label("updated_at"),
                # Related subqueries
                business_subq.label("business"),
                commodity_subq.label("commodity"),
                harvest_subq.label("harvest"),
            )
            .select_from(self.model)
            .outerjoin(
                business_alias,
                self.model.business_id == business_alias.id,
            )
            .outerjoin(
                commodity_alias,
                self.model.commodity_id == commodity_alias.id,
            )
            .outerjoin(
                harvest_alias,
                self.model.harvest_id == harvest_alias.id,
            )
            .group_by(self.model.id)
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
    ) -> Tuple[List[BusinessProductModel], int]:
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
    async def find_by_id(self, id: str, relationships: Optional[List[str]] = None) -> Optional[BusinessProductModel]:
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
        result = result.mappings().first()

        return self._mapping(result) if result else None

    @override
    async def create(self, data: Dict[str, Any]) -> BusinessProductModel:
        data = await super().create(data)
        return await self.find_by_id(data.id)

    @override
    async def update(self, id: str, data: Dict[str, Any]) -> BusinessProductModel:
        data = await super().update(id, data)
        return await self.find_by_id(data.id)
