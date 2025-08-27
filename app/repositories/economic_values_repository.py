from app.models import EconomicValueModel

from . import BaseRepository


class EconomicValuesRepository(BaseRepository[EconomicValueModel]):
    def __init__(self, model: type[EconomicValueModel]):
        super().__init__(model)
