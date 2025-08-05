from app.models import RolesModel

from . import BaseRepository


class RolesRepository(BaseRepository[RolesModel]):
    def __init__(self, model):
        super().__init__(model)
