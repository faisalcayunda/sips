from fastapi import APIRouter

from app.api.v1.routes import (
    auth_router,
    file_router,
    foresty_schema_router,
    proposal_foresty_status_router,
    regional_router,
    user_router,
)

router = APIRouter()
router.include_router(auth_router, tags=["Auth"])
router.include_router(file_router, tags=["Files"])
router.include_router(foresty_schema_router, tags=["Foresty Schema"])
router.include_router(regional_router, tags=["Regional"])
router.include_router(proposal_foresty_status_router, tags=["Proposal Foresty Status"])
router.include_router(user_router, tags=["Users"])
