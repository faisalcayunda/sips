from app.models import forestrySchemaModel

from . import BaseRepository


class forestrySchemaRepository(BaseRepository[forestrySchemaModel]):
    def __init__(self, model):
        super().__init__(model)
