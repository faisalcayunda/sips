from .attachment_route import router as attachment_router
from .auth_route import router as auth_router
from .businesses_route import router as businesses_router
from .file_route import router as file_router
from .forestry_area_route import router as forestry_area_router
from .forestry_land_route import router as forestry_land_router
from .forestry_schema_route import router as forestry_schema_router
from .navigation_route import router as navigation_router
from .permit_route import router as permit_router
from .piaps_route import router as piaps_router
from .proposal_forestry_route import router as proposal_forestry_router
from .proposal_forestry_status_route import router as proposal_forestry_status_router
from .regional_route import router as regional_router
from .roles_route import router as roles_router
from .user_route import router as user_router

__all__ = [
    "auth_router",
    "businesses_router",
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
]
