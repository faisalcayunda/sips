from app.models import IncomeModel
from app.repositories import FarmerIncomesRepository

from . import BaseService


class FarmerIncomesService(BaseService[IncomeModel, FarmerIncomesRepository]):
    def __init__(self, repository: FarmerIncomesRepository):
        super().__init__(IncomeModel, repository)
