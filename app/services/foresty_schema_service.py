from app.models import ForestySchemaModel
from app.repositories import ForestySchemaRepository

from . import BaseService


class ForestySchemaService(BaseService[ForestySchemaModel, ForestySchemaRepository]):
    def __init__(self, repository: ForestySchemaRepository):
        super().__init__(ForestySchemaModel, repository)
