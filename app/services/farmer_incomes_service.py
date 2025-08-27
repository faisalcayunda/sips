from app.models import FarmerIncomesModel
from app.repositories import FarmerIncomesRepository

from . import BaseService


class FarmerIncomesService(BaseService[FarmerIncomesModel, FarmerIncomesRepository]):
    def __init__(self, repository: FarmerIncomesRepository):
        super().__init__(FarmerIncomesModel, repository)
