from app.models import ForestryLandModel

from . import BaseRepository


class ForestryLandRepository(BaseRepository[ForestryLandModel]):
    def __init__(self, model):
        super().__init__(model)
