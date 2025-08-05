from app.models import ForestryAreaModel
from app.repositories import ForestryAreaRepository

from . import BaseService


class ForestryAreaService(BaseService[ForestryAreaModel, ForestryAreaRepository]):
    def __init__(self, repository: ForestryAreaModel):
        super().__init__(ForestryAreaModel, repository)
