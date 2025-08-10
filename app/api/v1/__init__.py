from fastapi import APIRouter

from app.api.v1.routes import (
    attachment_router,
    auth_router,
    businesses_router,
    file_router,
    forestry_area_router,
    forestry_land_router,
    forestry_schema_router,
    navigation_router,
    permit_router,
    piaps_router,
    proposal_forestry_router,
    proposal_forestry_status_router,
    regional_router,
    roles_router,
    user_router,
)

router = APIRouter()
router.include_router(auth_router, tags=["Auth"])
router.include_router(attachment_router, tags=["Attachment"])
router.include_router(businesses_router, tags=["Businesses"])
router.include_router(file_router, tags=["Files"])
router.include_router(forestry_area_router, tags=["Forestry Area"])
router.include_router(forestry_land_router, tags=["Forestry Land"])
router.include_router(forestry_schema_router, tags=["Forestry Schema"])
router.include_router(navigation_router, tags=["Navigation"])
router.include_router(regional_router, tags=["Regional"])
router.include_router(roles_router, tags=["Roles"])
router.include_router(permit_router, tags=["Permission"])
router.include_router(piaps_router, tags=["Piaps"])
router.include_router(proposal_forestry_router, tags=["Proposal Forestry"])
router.include_router(proposal_forestry_status_router, tags=["Proposal Forestry Status"])
router.include_router(user_router, tags=["Users"])
