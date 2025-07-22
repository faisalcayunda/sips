from app.models import ProposalforestryStatusModel
from app.repositories import ProposalforestryStatusRepository

from . import BaseService


class ProposalforestryStatusService(BaseService[ProposalforestryStatusModel, ProposalforestryStatusRepository]):
    def __init__(self, repository: ProposalforestryStatusRepository):
        super().__init__(ProposalforestryStatusModel, repository)
