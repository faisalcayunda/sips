from app.models import PiapsRecordsModel

from . import BaseRepository


class PiapsRecordsRepository(BaseRepository[PiapsRecordsModel]):
    def __init__(self, model: type[PiapsRecordsModel]):
        super().__init__(model)
