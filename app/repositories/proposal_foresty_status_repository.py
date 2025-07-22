from app.models import ProposalForestyStatusModel

from . import BaseRepository


class ProposalForestyStatusRepository(BaseRepository[ProposalForestyStatusModel]):
    def __init__(self, model):
        super().__init__(model)
