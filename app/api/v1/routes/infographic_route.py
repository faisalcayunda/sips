from fastapi import APIRouter, Depends

from app.api.dependencies.factory import ServiceFactory
from app.services import InfographicService

router = APIRouter()


@router.get("/infographics")
async def get_total_kph_accounts(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    """
    Return all data from all /infographic/* endpoints in a single response.
    """
    return {
        "summary": await service.get_summary_infographic(),
        "farmer_incomes": await service.get_farmer_incomes(),
        "social_forestry_achievement_by_schema": await service.get_social_forestry_achievement_by_schema(),
        "businesses_class_progress": await service.get_businesses_class_progress(),
        "growth_forestry_business_unit": await service.get_growth_forestry_business_unit(),
        "forestry_area_by_regional": await service.get_forestry_area_by_regional(),
        "households_by_regional": await service.get_households_by_regional(),
        "social_forestry_commodities_by_regency": await service.get_social_forestry_commodities_by_regency(),
        "sum_businesses_class_by_regency": await service.get_sum_businesses_class_by_regency(),
        "sum_forestry_schema_by_regency": await service.get_sum_forestry_schema_by_regency(),
    }


@router.get("/infographic/farmer-incomes")
async def get_farmer_incomes(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_farmer_incomes()


@router.get("/infographic/social-forestry-achievement-by-schema")
async def get_social_forestry_achievement_by_scheme(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_social_forestry_achievement_by_schema()


@router.get("/infographic/businesses-class-progress")
async def get_businesses_class_progress(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_businesses_class_progress()


@router.get("/infographic/growth-forestry-business-unit")
async def get_growth_forestry_business_unit(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_growth_forestry_business_unit()


@router.get("/infographic/summary")
async def get_aggregated_data(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_summary_infographic()


@router.get("/infographic/forestry-area-by-regional")
async def get_forestry_area_by_regional(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_forestry_area_by_regional()


@router.get("/infographic/households-by-regional")
async def get_households_by_regional(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_households_by_regional()


@router.get("/infographic/social-forestry-commodities-by-regency")
async def get_social_forestry_commodities_by_regency(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_social_forestry_commodities_by_regency()


@router.get("/infographic/sum-businesses-class-by-regency")
async def get_sum_businesses_class_by_regency(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_sum_businesses_class_by_regency()


@router.get("/infographic/sum-forestry-schema-by-regency")
async def get_sum_forestry_schema_by_regency(
    service: InfographicService = Depends(ServiceFactory().get_infographic_service),
):
    return await service.get_sum_forestry_schema_by_regency()
