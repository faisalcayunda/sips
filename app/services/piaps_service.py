from app.models import PiapsModel
from app.repositories import PiapsRepository

from . import BaseService


class PiapsService(BaseService[PiapsModel, PiapsRepository]):
    def __init__(self, repository: PiapsRepository):
        super().__init__(PiapsModel, repository)
