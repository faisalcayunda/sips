from app.models import BusinessesModel

from . import BaseRepository


class BusinessesRepository(BaseRepository[BusinessesModel]):
    def __init__(self, model):
        super().__init__(model)
