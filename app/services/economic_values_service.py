from app.models import EconomicValueModel
from app.repositories import EconomicValuesRepository

from . import BaseService


class EconomicValuesService(BaseService[EconomicValueModel, EconomicValuesRepository]):
    def __init__(self, repository: EconomicValuesRepository):
        super().__init__(EconomicValueModel, repository)
