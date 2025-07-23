from app.models import ForestrySchemaModel
from app.repositories import ForestrySchemaRepository

from . import BaseService


class ForestrySchemaService(BaseService[ForestrySchemaModel, ForestrySchemaRepository]):
    def __init__(self, repository: ForestrySchemaRepository):
        super().__init__(ForestrySchemaModel, repository)
