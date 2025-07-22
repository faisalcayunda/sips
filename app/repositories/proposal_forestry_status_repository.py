from app.models import ProposalforestryStatusModel

from . import BaseRepository


class ProposalforestryStatusRepository(BaseRepository[ProposalforestryStatusModel]):
    def __init__(self, model):
        super().__init__(model)
