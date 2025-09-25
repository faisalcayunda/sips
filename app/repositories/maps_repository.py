from fastapi_async_sqlalchemy import db
from sqlalchemy import text


class MapsRepository:
    async def get_all(self, filters: dict = None, limit: int = 100, offset: int = 0):
        base_query = """
            SELECT
                adm.nama_kab AS district_name,
                forestry.fore_name AS forestry_unit_name,
                stat_forestry_skema.nama_skema AS forestry_scheme_name,
                stat_forestry_skema.id_skema AS forestry_scheme_id,
                businesses.kups_nama AS business_group_name,
                stat_businesses_class.nama_kelas_kups AS business_class_name,
                stat_businesses_class.id AS business_class_id,
                kom1.komoditas_nama AS product_name,
                kom2.komoditas_nama AS service_name,
                COALESCE(kom1.komoditas_nama, kom2.komoditas_nama) AS commodity_name,
                businesses_product.prdk_panen_produksi AS production_volume,
                businesses_product.prdk_panen_satuan AS harvest_unit,
                stat_businesses_prdk_panen.name_prdk_panen AS harvest_frequency,
                user_account.acc_name AS forest_management_unit_name,
                stat_data_IG.id_spatial AS spatial_index
            FROM forestry
            LEFT JOIN adm ON forestry.reg_id = adm.reg_id
            LEFT JOIN user_account ON forestry.kph_acc_id = user_account.acc_id
            LEFT JOIN stat_data_IG ON forestry.fore_kps_id = stat_data_IG.id_IG
            LEFT JOIN businesses ON forestry.fore_kps_id = businesses.fore_kps_id
            LEFT JOIN businesses_product ON businesses.kups_id = businesses_product.kups_id
            LEFT JOIN businesses_service ON businesses.kups_id = businesses_service.kups_id
            LEFT JOIN komoditas kom1 ON businesses_product.komoditas_id = kom1.komoditas_id
            LEFT JOIN komoditas kom2 ON businesses_service.komoditas_id = kom2.komoditas_id
            LEFT JOIN stat_forestry_skema ON forestry.fore_skema_id = stat_forestry_skema.id_skema
            LEFT JOIN stat_businesses_class ON businesses.kups_kelas_id = stat_businesses_class.id_kelas
            LEFT JOIN stat_businesses_prdk_panen ON businesses_product.prdk_panen_id = stat_businesses_prdk_panen.id_prdk_panen
            WHERE forestry.fore_pps_status = 'SSK'
        """

        alias_to_column = {
            "district_name": "adm.nama_kab",
            "forestry_unit_name": "forestry.fore_name",
            "forestry_scheme_name": "stat_forestry_skema.nama_skema",
            "forestry_scheme_id": "stat_forestry_skema.id_skema",
            "business_group_name": "businesses.kups_nama",
            "business_class_name": "stat_businesses_class.nama_kelas_kups",
            "business_class_id": "stat_businesses_class.id",
            "product_name": "kom1.komoditas_nama",
            "service_name": "kom2.komoditas_nama",
            "commodity_name": "COALESCE(kom1.komoditas_nama, kom2.komoditas_nama)",
            "production_volume": "businesses_product.prdk_panen_produksi",
            "harvest_unit": "businesses_product.prdk_panen_satuan",
            "harvest_frequency": "stat_businesses_prdk_panen.name_prdk_panen",
            "forest_management_unit_name": "user_account.acc_name",
            "spatial_index": "stat_data_IG.id_spatial",
        }

        filter_clauses = []
        params = {}

        if filters:
            for key, value in filters.items():
                if key in alias_to_column and value is not None:
                    param_name = f"param_{key}"
                    filter_clauses.append(f"{alias_to_column[key]} = :{param_name}")
                    params[param_name] = value

        if filter_clauses:
            base_query += " AND " + " AND ".join(filter_clauses)

        # Query for total count
        count_query = f"SELECT COUNT(*) FROM ({base_query}) AS subquery"
        count_result = await db.session.execute(text(count_query), params)
        total = count_result.scalar() or 0

        # Query for paginated data
        paginated_query = base_query + " LIMIT :limit OFFSET :offset"
        params["limit"] = limit
        params["offset"] = offset

        query = text(paginated_query)
        result = await db.session.execute(query, params)
        rows = result.fetchall()
        columns = result.keys()
        items = [dict(zip(columns, row)) for row in rows]
        return items, total
