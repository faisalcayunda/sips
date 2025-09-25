from fastapi import APIRouter

from app.api.v1.routes import (
    article_router,
    attachment_router,
    auth_router,
    business_harvest_router,
    business_product_router,
    business_service_router,
    businesses_router,
    commodity_router,
    economic_values_router,
    farmer_incomes_router,
    file_router,
    forestry_area_router,
    forestry_land_router,
    forestry_schema_router,
    infographic_router,
    maps_router,
    navigation_router,
    permit_router,
    piaps_records_router,
    piaps_router,
    proposal_forestry_router,
    proposal_forestry_status_router,
    regional_router,
    roles_router,
    user_router,
)

router = APIRouter()
router.include_router(auth_router, tags=["Auths"])
router.include_router(article_router, tags=["Articles"])
router.include_router(attachment_router, tags=["Attachments"])
router.include_router(businesses_router, tags=["Businesses"])
router.include_router(business_product_router, tags=["Business Products"])
router.include_router(business_harvest_router, tags=["Business Harvests"])
router.include_router(business_service_router, tags=["Business Services"])
router.include_router(commodity_router, tags=["Commodities"])
router.include_router(file_router, tags=["Files"])
router.include_router(economic_values_router, tags=["Economic Values"])
router.include_router(farmer_incomes_router, tags=["Farmer Incomes"])
router.include_router(forestry_area_router, tags=["Forestry Areas"])
router.include_router(forestry_land_router, tags=["Forestry Lands"])
router.include_router(forestry_schema_router, tags=["Forestry Schemas"])
router.include_router(infographic_router, tags=["Infographics"])
router.include_router(maps_router, tags=["Maps"])
router.include_router(navigation_router, tags=["Navigations"])
router.include_router(regional_router, tags=["Regionals"])
router.include_router(roles_router, tags=["Roles"])
router.include_router(permit_router, tags=["Permissions"])
router.include_router(piaps_router, tags=["Piaps"])
router.include_router(piaps_records_router, tags=["Piaps Records"])
router.include_router(proposal_forestry_router, tags=["Proposal Forestries"])
router.include_router(proposal_forestry_status_router, tags=["Proposal Forestry Statuses"])
router.include_router(user_router, tags=["Users"])
