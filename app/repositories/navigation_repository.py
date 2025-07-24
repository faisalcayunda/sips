from app.models import NavigationModel

from . import BaseRepository


class NavigationRepository(BaseRepository[NavigationModel]):
    def __init__(self, model):
        super().__init__(model)
