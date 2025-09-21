from app.repositories import InfographicRepository


class InfographicService:
    def __init__(self, repository: InfographicRepository):
        self.repository = repository

    async def get_farmer_incomes(self):
        return await self.repository.get_farmer_incomes()

    async def get_social_forestry_achievement_by_schema(self):
        return await self.repository.get_social_forestry_achievement_by_schema()

    async def get_businesses_class_progress(self):
        return await self.repository.get_businesses_class_progress()

    async def get_growth_forestry_business_unit(self):
        return await self.repository.get_growth_forestry_business_unit()

    async def get_summary_infographic(self):
        return await self.repository.get_summary_infographic()

    async def get_forestry_area_by_regional(self):
        return await self.repository.get_forestry_area_by_regional()

    async def get_households_by_regional(self):
        return await self.repository.get_households_by_regional()

    async def get_social_forestry_commodities_by_regency(self):
        return await self.repository.get_social_forestry_commodities_by_regency()

    async def get_sum_businesses_class_by_regency(self):
        return await self.repository.get_sum_businesses_class_by_regency()

    async def get_sum_forestry_schema_by_regency(self):
        return await self.repository.get_sum_forestry_schema_by_regency()
