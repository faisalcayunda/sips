from .auth_route import router as auth_router
from .file_route import router as file_router

from .user_route import router as user_router

__all__ = [
    "auth_router",
    "file_router",
    "user_router",
]
