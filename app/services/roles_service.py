from app.models import RolesModel
from app.repositories import RolesRepository

from . import BaseService


class RolesService(BaseService[RolesModel, RolesRepository]):
    def __init__(self, repository: RolesRepository):
        super().__init__(RolesModel, repository)
