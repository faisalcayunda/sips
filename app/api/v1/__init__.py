from fastapi import APIRouter

from app.api.v1.routes import (
    auth_router,
    file_router,
    forestry_schema_router,
    piaps_router,
    proposal_forestry_router,
    proposal_forestry_status_router,
    regional_router,
    user_router,
)

router = APIRouter()
router.include_router(auth_router, tags=["Auth"])
router.include_router(file_router, tags=["Files"])
router.include_router(forestry_schema_router, tags=["forestry Schema"])
router.include_router(regional_router, tags=["Regional"])
router.include_router(piaps_router, tags=["Piaps"])
router.include_router(proposal_forestry_router, tags=["Proposal forestry"])
router.include_router(proposal_forestry_status_router, tags=["Proposal forestry Status"])
router.include_router(user_router, tags=["Users"])
