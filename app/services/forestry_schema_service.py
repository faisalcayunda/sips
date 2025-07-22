from app.models import forestrySchemaModel
from app.repositories import forestrySchemaRepository

from . import BaseService


class forestrySchemaService(BaseService[forestrySchemaModel, forestrySchemaRepository]):
    def __init__(self, repository: forestrySchemaRepository):
        super().__init__(forestrySchemaModel, repository)
