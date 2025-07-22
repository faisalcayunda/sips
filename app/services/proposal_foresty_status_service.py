from app.models import ProposalForestyStatusModel
from app.repositories import ProposalForestyStatusRepository

from . import BaseService


class ProposalForestyStatusService(BaseService[ProposalForestyStatusModel, ProposalForestyStatusRepository]):
    def __init__(self, repository: ProposalForestyStatusRepository):
        super().__init__(ProposalForestyStatusModel, repository)
