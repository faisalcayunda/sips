from app.repositories import MapsRepository


class MapsService:
    def __init__(self, repository: MapsRepository):
        self.repository = repository

    async def get_all(self, filters: dict = None, limit: int = 100, offset: int = 0):
        return await self.repository.get_all(filters, limit, offset)
