from app.models import PermitModel

from . import BaseRepository


class PermitRepository(BaseRepository[PermitModel]):
    def __init__(self, model):
        super().__init__(model)
