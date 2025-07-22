from .auth_route import router as auth_router
from .file_route import router as file_router
from .forestry_schema_route import router as forestry_schema_router
from .piaps_route import router as piaps_router
from .proposal_forestry_status_route import router as proposal_forestry_status_router
from .regional_route import router as regional_router
from .user_route import router as user_router

__all__ = [
    "auth_router",
    "file_router",
    "user_router",
    "regional_router",
    "forestry_schema_router",
    "proposal_forestry_status_router",
    "piaps_router",
]
