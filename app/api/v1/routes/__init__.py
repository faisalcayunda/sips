from .article_route import router as article_router
from .attachment_route import router as attachment_router
from .auth_route import router as auth_router
from .business_harvest_route import router as business_harvest_router
from .business_product_route import router as business_product_router
from .business_service_route import router as business_service_router
from .businesses_route import router as businesses_router
from .commodity_route import router as commodity_router
from .economic_values_route import router as economic_values_router
from .farmer_incomes_route import router as farmer_incomes_router
from .file_route import router as file_router
from .forestry_area_route import router as forestry_area_router
from .forestry_land_route import router as forestry_land_router
from .forestry_schema_route import router as forestry_schema_router
from .infographic_route import router as infographic_router
from .maps_route import router as maps_router
from .navigation_route import router as navigation_router
from .permit_route import router as permit_router
from .piaps_records_route import router as piaps_records_router
from .piaps_route import router as piaps_router
from .proposal_forestry_route import router as proposal_forestry_router
from .proposal_forestry_status_route import router as proposal_forestry_status_router
from .regional_route import router as regional_router
from .roles_route import router as roles_router
from .settings_route import router as settings_router
from .user_route import router as user_router

__all__ = [
    "article_router",
    "auth_router",
    "businesses_router",
    "business_product_router",
    "business_harvest_router",
    "business_service_router",
    "file_router",
    "user_router",
    "regional_router",
    "forestry_schema_router",
    "proposal_forestry_status_router",
    "piaps_router",
    "proposal_forestry_router",
    "attachment_router",
    "forestry_land_router",
    "permit_router",
    "navigation_router",
    "roles_router",
    "forestry_area_router",
    "commodity_router",
    "economic_values_router",
    "piaps_records_router",
    "farmer_incomes_router",
    "infographic_router",
    "maps_router",
    "settings_router",
]
