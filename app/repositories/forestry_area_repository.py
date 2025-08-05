from app.models import ForestryAreaModel

from . import BaseRepository


class ForestryAreaRepository(BaseRepository[ForestryAreaModel]):
    def __init__(self, model):
        super().__init__(model)
