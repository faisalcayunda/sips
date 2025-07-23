from functools import partial

from app.core.minio_client import MinioClient
from app.models import (
    AttachmentModel,
    FileModel,
    ForestryLandModel,
    ForestryProposalModel,
    ForestrySchemaModel,
    PiapsModel,
    ProposalforestryStatusModel,
    RefreshTokenModel,
    RegionalModel,
    UserModel,
)
from app.repositories import (
    AttachmentRepository,
    FileRepository,
    ForestryLandRepository,
    ForestryProposalRepository,
    ForestrySchemaRepository,
    PiapsRepository,
    ProposalforestryStatusRepository,
    RegionalRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    AttachmentService,
    AuthService,
    FileService,
    ForestryLandService,
    ForestrySchemaService,
    ForestyProposalService,
    PiapsService,
    ProposalforestryStatusService,
    RegionalService,
    UserService,
)


class Factory:
    user_repository = staticmethod(partial(UserRepository, UserModel))
    token_repository = staticmethod(partial(TokenRepository, RefreshTokenModel))
    file_repository = staticmethod(partial(FileRepository, FileModel))
    regional_repository = staticmethod(partial(RegionalRepository, RegionalModel))
    forestry_schema_repository = staticmethod(partial(ForestrySchemaRepository, ForestrySchemaModel))
    proposal_forestry_status_repository = staticmethod(
        partial(ProposalforestryStatusRepository, ProposalforestryStatusModel)
    )
    piaps_repository = staticmethod(partial(PiapsRepository, PiapsModel))
    forestry_proposal_repository = staticmethod(partial(ForestryProposalRepository, ForestryProposalModel))
    attachment_repository = staticmethod(partial(AttachmentRepository, AttachmentModel))
    forestry_land_repository = staticmethod(partial(ForestryLandRepository, ForestryLandModel))

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

    def get_forestry_schema_service(
        self,
    ):
        return ForestrySchemaService(self.forestry_schema_repository())

    def get_proposal_forestry_status_service(
        self,
    ):
        return ProposalforestryStatusService(self.proposal_forestry_status_repository())

    def get_piaps_service(
        self,
    ):
        return PiapsService(self.piaps_repository())

    def get_proposal_forestry_service(
        self,
    ):
        return ForestyProposalService(self.forestry_proposal_repository())

    def get_attachment_service(
        self,
    ):
        return AttachmentService(self.attachment_repository())

    def get_forestry_land_service(
        self,
    ):
        return ForestryLandService(self.forestry_land_repository())
