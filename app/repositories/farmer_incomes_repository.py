from app.models import FarmerIncomesModel

from . import BaseRepository


class FarmerIncomesRepository(BaseRepository[FarmerIncomesModel]):
    def __init__(self, model: type[FarmerIncomesModel]):
        super().__init__(model)
