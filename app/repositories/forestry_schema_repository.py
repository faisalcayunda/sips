from app.models import ForestrySchemaModel

from . import BaseRepository


class ForestrySchemaRepository(BaseRepository[ForestrySchemaModel]):
    def __init__(self, model):
        super().__init__(model)
