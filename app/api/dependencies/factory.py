from functools import partial

from app.core.minio_client import MinioClient
from app.models import (
    AttachmentModel,
    FileModel,
    ForestryAreaModel,
    ForestryLandModel,
    ForestryProposalModel,
    ForestrySchemaModel,
    NavigationModel,
    PermitModel,
    PiapsModel,
    ProposalforestryStatusModel,
    RefreshTokenModel,
    RegionalModel,
    RolesModel,
    UserModel,
)
from app.repositories import (
    AttachmentRepository,
    FileRepository,
    ForestryAreaRepository,
    ForestryLandRepository,
    ForestryProposalRepository,
    ForestrySchemaRepository,
    NavigationRepository,
    PermitRepository,
    PiapsRepository,
    ProposalforestryStatusRepository,
    RegionalRepository,
    RolesRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    AttachmentService,
    AuthService,
    FileService,
    ForestryAreaService,
    ForestryLandService,
    ForestrySchemaService,
    ForestyProposalService,
    NavigationService,
    PermitService,
    PiapsService,
    ProposalforestryStatusService,
    RegionalService,
    RolesService,
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
    permit_repository = staticmethod(partial(PermitRepository, PermitModel))
    navigation_repository = staticmethod(partial(NavigationRepository, NavigationModel))
    roles_repository = staticmethod(partial(RolesRepository, RolesModel))
    forestry_area_repository = staticmethod(partial(ForestryAreaRepository, ForestryAreaModel))

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

    def get_permit_service(
        self,
    ):
        return PermitService(self.permit_repository())

    def get_navigation_service(
        self,
    ):
        return NavigationService(self.navigation_repository())

    def get_roles_service(
        self,
    ):
        return RolesService(self.roles_repository())

    def get_forestry_area_service(
        self,
    ):
        return ForestryAreaService(self.forestry_area_repository())
