from app.models import BusinessHarvestModel

from . import BaseRepository


class BusinessHarvestRepository(BaseRepository[BusinessHarvestModel]):
    def __init__(self, model):
        super().__init__(model)
