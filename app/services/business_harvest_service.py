from app.models import BusinessHarvestModel
from app.repositories import BusinessHarvestRepository

from . import BaseService


class BusinessHarvestService(BaseService[BusinessHarvestModel, BusinessHarvestRepository]):
    def __init__(self, repository: BusinessHarvestRepository):
        super().__init__(BusinessHarvestModel, repository)
