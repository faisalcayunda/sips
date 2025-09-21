from fastapi_async_sqlalchemy import db
from sqlalchemy import text


class InfographicRepository:
    async def get_farmer_incomes(self):
        query = text(
            """
            WITH yearly AS (
                SELECT
                    p.tahun AS year,
                    SUM(p.pendapatan) AS total_income
                FROM pendapatan p
                GROUP BY p.tahun
                ),
                yoy AS (
                SELECT
                    y.year AS year,
                    y.total_income,
                    LAG(y.total_income) OVER (ORDER BY y.year) AS previous_income
                FROM yearly y
                )
                SELECT
                year,
                total_income,
                (total_income - COALESCE(previous_income, 0)) AS difference,
                CASE
                    WHEN previous_income IS NULL OR previous_income = 0 THEN 0
                    ELSE ROUND(((total_income - previous_income) / previous_income) * 100, 2)
                END AS growth_percentage
                FROM yoy
                ORDER BY year;
            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_social_forestry_achievement_by_schema(self):
        """
        Retrieve social forestry achievement data grouped by scheme.
        """
        query = text(
            """
            WITH
                ps AS (
                SELECT
                    UPPER(TRIM(f.fore_skema_id))                 AS schema_code,
                    COUNT(DISTINCT f.fore_kps_id)                AS total_ps_units,
                    COALESCE(SUM(f.fore_jumlah_kk),0)            AS total_households,
                    COALESCE(SUM(f.fore_luas),0)                 AS total_area_ha
                FROM forestry f
                --   WHERE f.fore_kps_valid = 'Y'
                GROUP BY UPPER(TRIM(f.fore_skema_id))
                ),
                kups AS (
                SELECT
                    UPPER(TRIM(f.fore_skema_id))                 AS schema_code,
                    COUNT(DISTINCT b.kups_id)                    AS total_kups_units
                FROM forestry f
                JOIN businesses b
                    ON UPPER(TRIM(b.fore_kps_id)) = UPPER(TRIM(f.fore_kps_id))
                --   WHERE f.fore_kps_valid = 'Y'
                GROUP BY UPPER(TRIM(f.fore_skema_id))
                )
                SELECT
                    s.nama_skema                                       AS schema_name,
                    COALESCE(ps.total_ps_units, 0)                      AS total_ps_units,
                    COALESCE(ps.total_households, 0)                    AS total_households,
                    COALESCE(ps.total_area_ha, 0)                       AS total_area_ha,
                    COALESCE(k.total_kups_units, 0)                     AS total_kups_units
                FROM stat_forestry_skema s
                LEFT JOIN ps   ON UPPER(TRIM(s.id_skema)) = ps.schema_code
                LEFT JOIN kups k ON UPPER(TRIM(s.id_skema)) = k.schema_code
                ORDER BY COALESCE(s.ord, 999), s.nama_skema;
            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_businesses_class_progress(self):
        query = text(
            """
            WITH
                ps AS (
                    SELECT
                        UPPER(TRIM(f.fore_kps_id)) AS kps_id,
                        UPPER(TRIM(f.fore_skema_id)) AS scheme
                    FROM forestry f
                    --   WHERE f.fore_kps_valid = 'Y'
                ),
                bk AS (
                    SELECT
                        UPPER(TRIM(b.fore_kps_id)) AS kps_id,
                        COALESCE(NULLIF(TRIM(sbc.nama_kelas_kups),''), 'KUPS Not Registered') AS class_name,
                        b.kups_id
                    FROM businesses b
                    LEFT JOIN stat_businesses_class sbc
                        ON sbc.id_kelas = b.kups_kelas_id
                )
                SELECT
                    b.class_name,
                    p.scheme,
                    COUNT(DISTINCT b.kups_id) AS total_kups
                FROM bk b
                JOIN ps p ON p.kps_id = b.kps_id
                GROUP BY b.class_name, p.scheme
                ORDER BY
                    FIELD(b.class_name,'KUPS Not Registered','Blue','Silver','Gold','Platinum'), p.scheme;

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_growth_forestry_business_unit(self):
        query = text(
            """
            WITH base AS (
                SELECT
                    b.kups_pembentukan AS year_established,
                    CASE
                    WHEN UPPER(TRIM(sbo.id_operational)) = 'HOP' THEN 'Beroperasi'
                    WHEN UPPER(TRIM(sbo.id_operational)) = 'NOP' THEN 'Belum Beroperasi'
                    WHEN UPPER(TRIM(sbo.id_operational)) = 'VOP' THEN 'Vakum'
                    ELSE 'Tidak Diketahui'
                    END AS status_en,
                    b.kups_id
                FROM businesses b
                LEFT JOIN stat_businesses_operational sbo
                    ON UPPER(TRIM(sbo.id_operational)) = UPPER(TRIM(b.kups_status_op_id))
                )
                SELECT
                year_established,
                status_en,
                COUNT(DISTINCT kups_id) AS kups_count
                FROM base
                GROUP BY year_established, status_en
                ORDER BY year_established, FIELD(status_en,'Belum Beroperasi','Beroperasi','Vakum','Tidak Diketahui');

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_summary_infographic(self):
        query = text(
            """
            SELECT
                /* 1) Social Forestry Area (Ha) */
                (SELECT COALESCE(SUM(f.fore_luas),0)
                    FROM forestry f)                                               AS ps_area_ha,

                /* 2) Households Impacted */
                (SELECT COALESCE(SUM(f.fore_jumlah_kk),0)
                    FROM forestry f)                                               AS impacted_households,

                /* 3) Distinct commodity types used by PS businesses */
                (SELECT COUNT(DISTINCT bp.komoditas_id)
                    FROM businesses_product bp
                    JOIN businesses b
                    ON b.kups_id = bp.kups_id
                    JOIN forestry f
                    ON UPPER(TRIM(f.fore_kps_id)) = UPPER(TRIM(b.fore_kps_id)))  AS commodity_types,

                /* 4) PS Groups (units) */
                (SELECT COUNT(DISTINCT f.fore_kps_id)
                    FROM forestry f)                                               AS ps_groups,

                /* 5) KUPS Groups */
                (SELECT COUNT(DISTINCT b.kups_id)
                    FROM businesses b
                    JOIN forestry f
                    ON UPPER(TRIM(f.fore_kps_id)) = UPPER(TRIM(b.fore_kps_id)))  AS kups_groups;

            """
        )
        result = await db.session.execute(query)
        row = result.fetchone()
        columns = result.keys()
        return dict(zip(columns, row))

    async def get_forestry_area_by_regional(self):
        query = text(
            """
            SELECT
                r.reg_name                    AS regency_name,
                ROUND(SUM(f.fore_luas), 2)    AS total_area_ha
            FROM forestry f
            LEFT JOIN regional r
                ON r.reg_id = f.reg_id
                -- uncomment if your regional table marks regency/city level explicitly:
                -- WHERE r.reg_level IN (2)   -- 2 = Regency/City
            GROUP BY r.reg_name
            ORDER BY total_area_ha DESC, r.reg_name;
            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_households_by_regional(self):
        query = text(
            """
            SELECT
                r.reg_name                 AS regency_name,
                SUM(f.fore_jumlah_kk)      AS households_sum
            FROM forestry f
            LEFT JOIN regional r
                ON r.reg_id = f.reg_id
            GROUP BY r.reg_name
            ORDER BY households_sum DESC, r.reg_name
            -- LIMIT 15;
            ;

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_social_forestry_commodities_by_regency(self):
        query = text(
            """
            WITH base AS (
            SELECT
                CASE WHEN TRIM(COALESCE(k.komoditas_nama,''))='' THEN 'Lain lain' ELSE k.komoditas_nama END AS commodity_name,
                r.reg_name AS regency_name,
                b.kups_id
            FROM businesses_product bp
            JOIN businesses b  ON b.kups_id = bp.kups_id
            JOIN forestry f    ON UPPER(TRIM(f.fore_kps_id)) = UPPER(TRIM(b.fore_kps_id))
            LEFT JOIN komoditas k ON k.komoditas_id = bp.komoditas_id
            LEFT JOIN regional  r ON r.reg_id = f.reg_id
            ),
            total_per_commodity AS (
            SELECT commodity_name, COUNT(DISTINCT kups_id) AS total_kups
            FROM base
            GROUP BY commodity_name
            ORDER BY total_kups DESC

            )
            SELECT
            b.commodity_name,
            b.regency_name,
            COUNT(DISTINCT b.kups_id) AS kups_count
            FROM base b
            JOIN total_per_commodity t USING (commodity_name)
            GROUP BY b.commodity_name, b.regency_name
            ORDER BY t.total_kups DESC, b.commodity_name, kups_count DESC;

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_sum_businesses_class_by_regency(self):
        query = text(
            """
            WITH ps AS (
                SELECT
                    UPPER(TRIM(f.fore_kps_id)) AS kps_id,
                    r.reg_name                 AS regency_name
                FROM forestry f
                LEFT JOIN regional r ON r.reg_id = f.reg_id
                ),
                biz AS (
                SELECT
                    UPPER(TRIM(b.fore_kps_id)) AS kps_id,
                    b.kups_id,
                    /* Map class to English; NULL/unknown -> Unregistered */
                    CASE UPPER(TRIM(sbc.nama_kelas_kups))
                    WHEN 'BLUE'     THEN 'Blue'
                    WHEN 'SILVER'   THEN 'Silver'
                    WHEN 'GOLD'     THEN 'Gold'
                    WHEN 'PLATINUM' THEN 'Platinum'
                    ELSE 'Unregistered'
                    END AS class_en
                FROM businesses b
                LEFT JOIN stat_businesses_class sbc
                        ON sbc.id_kelas = b.kups_kelas_id
                )
                SELECT
                p.regency_name,
                b.class_en,
                COUNT(DISTINCT b.kups_id) AS kups_count
                FROM biz b
                JOIN ps  p ON p.kps_id = b.kps_id
                GROUP BY p.regency_name, b.class_en
                ORDER BY
                SUM(COUNT(*)) OVER (PARTITION BY p.regency_name) DESC,  -- regency with highest total first
                p.regency_name,
                FIELD(b.class_en,'Blue','Gold','Unregistered','Platinum','Silver');  -- legend order

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

    async def get_sum_forestry_schema_by_regency(self):
        query = text(
            """
            WITH agg AS (
                SELECT
                    r.reg_name                               AS regency_name,
                    UPPER(TRIM(f.fore_skema_id))             AS scheme_code,   -- e.g. HA, HKM, HN, HTR, KK
                    COUNT(DISTINCT f.fore_kps_id)            AS kps_count
                FROM forestry f
                LEFT JOIN regional r ON r.reg_id = f.reg_id
                /* Optional: only validated units
                    WHERE f.fore_kps_valid = 'Y' */
                GROUP BY r.reg_name, UPPER(TRIM(f.fore_skema_id))
                )
                SELECT
                regency_name,
                scheme_code,
                kps_count
                FROM agg
            ORDER BY
                SUM(kps_count) OVER (PARTITION BY regency_name) DESC,  -- biggest totals first
                regency_name,
                FIELD(scheme_code,'HA','HKM','HN','HTR','KK');         -- legend order

            """
        )
        result = await db.session.execute(query)
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]
