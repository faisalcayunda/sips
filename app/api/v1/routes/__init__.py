from .auth_route import router as auth_router
from .file_route import router as file_router
from .foresty_schema_route import router as foresty_schema_router
from .regional_route import router as regional_router
from .user_route import router as user_router

__all__ = [
    "auth_router",
    "file_router",
    "user_router",
    "regional_router",
    "foresty_schema_router",
]
