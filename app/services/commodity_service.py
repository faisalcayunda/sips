from app.models import CommodityModel
from app.repositories import CommodityRepository

from . import BaseService


class CommodityService(BaseService[CommodityModel, CommodityRepository]):
    def __init__(self, repository: CommodityRepository):
        super().__init__(CommodityModel, repository)
