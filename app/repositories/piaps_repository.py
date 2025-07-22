from app.models import PiapsModel

from . import BaseRepository


class PiapsRepository(BaseRepository[PiapsModel]):
    def __init__(self, model):
        super().__init__(model)
