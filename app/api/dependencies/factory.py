from functools import partial

from app.core.minio_client import MinioClient
from app.models import (
    FileModel,
    ForestySchemaModel,
    ProposalForestyStatusModel,
    RefreshTokenModel,
    RegionalModel,
    UserModel,
)
from app.repositories import (
    FileRepository,
    ForestySchemaRepository,
    ProposalForestyStatusRepository,
    RegionalRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    AuthService,
    FileService,
    ForestySchemaService,
    ProposalForestyStatusService,
    RegionalService,
    UserService,
)


class Factory:
    user_repository = staticmethod(partial(UserRepository, UserModel))
    token_repository = staticmethod(partial(TokenRepository, RefreshTokenModel))
    file_repository = staticmethod(partial(FileRepository, FileModel))
    regional_repository = staticmethod(partial(RegionalRepository, RegionalModel))
    foresty_schema_repository = staticmethod(partial(ForestySchemaRepository, ForestySchemaModel))
    proposal_foresty_status_repository = staticmethod(
        partial(ProposalForestyStatusRepository, ProposalForestyStatusModel)
    )

    def get_auth_service(
        self,
    ):
        return AuthService(
            user_repository=self.user_repository(),
            token_repository=self.token_repository(),
        )

    def get_user_service(
        self,
    ):
        return UserService(self.user_repository())

    def get_file_service(
        self,
    ):
        return FileService(self.file_repository(), MinioClient())

    def get_regional_service(
        self,
    ):
        return RegionalService(self.regional_repository())

    def get_foresty_schema_service(
        self,
    ):
        return ForestySchemaService(self.foresty_schema_repository())

    def get_proposal_foresty_status_service(
        self,
    ):
        return ProposalForestyStatusService(self.proposal_foresty_status_repository())
