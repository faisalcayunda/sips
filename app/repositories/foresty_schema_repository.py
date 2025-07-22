from app.models import ForestySchemaModel

from . import BaseRepository


class ForestySchemaRepository(BaseRepository[ForestySchemaModel]):
    def __init__(self, model):
        super().__init__(model)
