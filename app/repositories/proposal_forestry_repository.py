from app.models import ForestryProposalModel

from . import BaseRepository


class ForestryProposalRepository(BaseRepository[ForestryProposalModel]):
    def __init__(self, model):
        super().__init__(model)
