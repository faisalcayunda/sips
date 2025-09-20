from app.models import IncomeModel

from . import BaseRepository


class FarmerIncomesRepository(BaseRepository[IncomeModel]):
    def __init__(self, model: type[IncomeModel]):
        super().__init__(model)
