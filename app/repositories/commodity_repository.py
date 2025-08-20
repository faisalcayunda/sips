from app.models import CommodityModel

from . import BaseRepository


class CommodityRepository(BaseRepository[CommodityModel]):
    def __init__(self, model):
        super().__init__(model)
