from app.models import PiapsRecordsModel
from app.repositories import PiapsRecordsRepository

from . import BaseService


class PiapsRecordsService(BaseService[PiapsRecordsModel, PiapsRecordsRepository]):
    def __init__(self, repository: PiapsRecordsRepository):
        super().__init__(PiapsRecordsModel, repository)
