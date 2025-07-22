from app.models import FileModel

from . import BaseRepository


class RegionalRepository(BaseRepository[FileModel]):
    def __init__(self, model):
        super().__init__(model)
