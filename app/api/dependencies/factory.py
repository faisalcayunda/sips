from functools import partial

from app.core.minio_client import MinioClient
from app.models import (
    ArticleCommentModel,
    ArticleModel,
    ArticleRatingModel,
    AttachmentModel,
    BusinessesModel,
    BusinessHarvestModel,
    BusinessProductModel,
    BusinessServiceModel,
    CommodityModel,
    EconomicValueModel,
    FileModel,
    ForestryAreaModel,
    ForestryLandModel,
    ForestryProposalModel,
    ForestrySchemaModel,
    IncomeModel,
    NavigationModel,
    PermitModel,
    PiapsModel,
    PiapsRecordsModel,
    ProposalforestryStatusModel,
    RefreshTokenModel,
    RegionalModel,
    RolesModel,
    SettingsModel,
    UserModel,
)
from app.repositories import (
    ArticleCommentRepository,
    ArticleRatingRepository,
    ArticleRepository,
    AttachmentRepository,
    BusinessesRepository,
    BusinessHarvestRepository,
    BusinessProductRepository,
    BusinessServiceRepository,
    CommodityRepository,
    EconomicValuesRepository,
    FarmerIncomesRepository,
    FileRepository,
    ForestryAreaRepository,
    ForestryLandRepository,
    ForestryProposalRepository,
    ForestrySchemaRepository,
    InfographicRepository,
    MapsRepository,
    NavigationRepository,
    PermitRepository,
    PiapsRecordsRepository,
    PiapsRepository,
    ProposalforestryStatusRepository,
    RegionalRepository,
    RolesRepository,
    SettingsRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    ArticleCommentService,
    ArticleRatingService,
    ArticleService,
    AttachmentService,
    AuthService,
    BusinessesService,
    BusinessHarvestService,
    BusinessProductService,
    BusinessServiceService,
    CommodityService,
    EconomicValuesService,
    FarmerIncomesService,
    FileService,
    ForestryAreaService,
    ForestryLandService,
    ForestrySchemaService,
    ForestyProposalService,
    InfographicService,
    MapsService,
    NavigationService,
    PermitService,
    PiapsRecordsService,
    PiapsService,
    ProposalforestryStatusService,
    RegionalService,
    RolesService,
    SettingsService,
    UserService,
)


class RepositoryFactory:
    """Factory untuk membuat repository instances dengan dependency injection."""

    @staticmethod
    def create_user_repository() -> UserRepository:
        return UserRepository(UserModel)

    @staticmethod
    def create_token_repository() -> TokenRepository:
        return TokenRepository(RefreshTokenModel)

    @staticmethod
    def create_file_repository() -> FileRepository:
        return FileRepository(FileModel)

    @staticmethod
    def create_regional_repository() -> RegionalRepository:
        return RegionalRepository(RegionalModel)

    @staticmethod
    def create_forestry_schema_repository() -> ForestrySchemaRepository:
        return ForestrySchemaRepository(ForestrySchemaModel)

    @staticmethod
    def create_proposal_forestry_status_repository() -> ProposalforestryStatusRepository:
        return ProposalforestryStatusRepository(ProposalforestryStatusModel)

    @staticmethod
    def create_piaps_repository() -> PiapsRepository:
        return PiapsRepository(PiapsModel)

    @staticmethod
    def create_forestry_proposal_repository() -> ForestryProposalRepository:
        return ForestryProposalRepository(ForestryProposalModel)

    @staticmethod
    def create_attachment_repository() -> AttachmentRepository:
        return AttachmentRepository(AttachmentModel)

    @staticmethod
    def create_forestry_land_repository() -> ForestryLandRepository:
        return ForestryLandRepository(ForestryLandModel)

    @staticmethod
    def create_permit_repository() -> PermitRepository:
        return PermitRepository(PermitModel)

    @staticmethod
    def create_navigation_repository() -> NavigationRepository:
        return NavigationRepository(NavigationModel)

    @staticmethod
    def create_roles_repository() -> RolesRepository:
        return RolesRepository(RolesModel)

    @staticmethod
    def create_forestry_area_repository() -> ForestryAreaRepository:
        return ForestryAreaRepository(ForestryAreaModel)

    @staticmethod
    def create_businesses_repository() -> BusinessesRepository:
        return BusinessesRepository(BusinessesModel)

    @staticmethod
    def create_business_product_repository() -> BusinessProductRepository:
        return BusinessProductRepository(BusinessProductModel)

    @staticmethod
    def create_business_harvest_repository() -> BusinessHarvestRepository:
        return BusinessHarvestRepository(BusinessHarvestModel)

    @staticmethod
    def create_commodity_repository() -> CommodityRepository:
        return CommodityRepository(CommodityModel)

    @staticmethod
    def create_business_service_repository() -> BusinessServiceRepository:
        return BusinessServiceRepository(BusinessServiceModel)

    @staticmethod
    def create_article_repository() -> ArticleRepository:
        return ArticleRepository(ArticleModel)

    @staticmethod
    def create_farmer_incomes_repository() -> FarmerIncomesRepository:
        return FarmerIncomesRepository(IncomeModel)

    @staticmethod
    def create_economic_values_repository() -> EconomicValuesRepository:
        return EconomicValuesRepository(EconomicValueModel)

    @staticmethod
    def create_piaps_records_repository() -> PiapsRecordsRepository:
        return PiapsRecordsRepository(PiapsRecordsModel)

    @staticmethod
    def create_article_rating_repository() -> ArticleRatingRepository:
        return ArticleRatingRepository(ArticleRatingModel)

    @staticmethod
    def create_article_comment_repository() -> ArticleCommentRepository:
        return ArticleCommentRepository(ArticleCommentModel)

    @staticmethod
    def create_infographic_repository() -> InfographicRepository:
        return InfographicRepository()

    @staticmethod
    def create_maps_repository() -> MapsRepository:
        return MapsRepository()

    @staticmethod
    def create_settings_repository() -> SettingsRepository:
        return SettingsRepository(SettingsModel)


class ServiceFactory:
    """Factory untuk membuat service instances."""

    def __init__(self):
        self.repository_factory = RepositoryFactory()

    def get_auth_service(self) -> AuthService:
        """Get AuthService instance."""
        return AuthService(
            user_repository=self.repository_factory.create_user_repository(),
            token_repository=self.repository_factory.create_token_repository(),
        )

    def get_user_service(self) -> UserService:
        """Get UserService instance."""
        return UserService(self.repository_factory.create_user_repository())

    def get_file_service(self) -> FileService:
        """Get FileService instance."""
        return FileService(self.repository_factory.create_file_repository(), MinioClient())

    def get_regional_service(self) -> RegionalService:
        """Get RegionalService instance."""
        return RegionalService(self.repository_factory.create_regional_repository())

    def get_forestry_schema_service(self) -> ForestrySchemaService:
        """Get ForestrySchemaService instance."""
        return ForestrySchemaService(self.repository_factory.create_forestry_schema_repository())

    def get_proposal_forestry_status_service(self) -> ProposalforestryStatusService:
        """Get ProposalforestryStatusService instance."""
        return ProposalforestryStatusService(self.repository_factory.create_proposal_forestry_status_repository())

    def get_piaps_service(self) -> PiapsService:
        """Get PiapsService instance."""
        return PiapsService(self.repository_factory.create_piaps_repository())

    def get_proposal_forestry_service(self) -> ForestyProposalService:
        """Get ForestyProposalService instance."""
        return ForestyProposalService(self.repository_factory.create_forestry_proposal_repository())

    def get_attachment_service(self) -> AttachmentService:
        """Get AttachmentService instance."""
        return AttachmentService(self.repository_factory.create_attachment_repository())

    def get_forestry_land_service(self) -> ForestryLandService:
        """Get ForestryLandService instance."""
        return ForestryLandService(self.repository_factory.create_forestry_land_repository())

    def get_permit_service(self) -> PermitService:
        """Get PermitService instance."""
        return PermitService(self.repository_factory.create_permit_repository())

    def get_navigation_service(self) -> NavigationService:
        """Get NavigationService instance."""
        return NavigationService(self.repository_factory.create_navigation_repository())

    def get_roles_service(self) -> RolesService:
        """Get RolesService instance."""
        return RolesService(self.repository_factory.create_roles_repository())

    def get_forestry_area_service(self) -> ForestryAreaService:
        """Get ForestryAreaService instance."""
        return ForestryAreaService(self.repository_factory.create_forestry_area_repository())

    def get_businesses_service(self) -> BusinessesService:
        """Get BusinessesService instance."""
        return BusinessesService(self.repository_factory.create_businesses_repository())

    def get_business_product_service(self) -> BusinessProductService:
        """Get BusinessProductService instance."""
        return BusinessProductService(self.repository_factory.create_business_product_repository())

    def get_business_harvest_service(self) -> BusinessHarvestService:
        """Get BusinessHarvestService instance."""
        return BusinessHarvestService(self.repository_factory.create_business_harvest_repository())

    def get_commodity_service(self) -> CommodityService:
        """Get CommodityService instance."""
        return CommodityService(self.repository_factory.create_commodity_repository())

    def get_business_service_service(self) -> BusinessServiceService:
        """Get BusinessServiceService instance."""
        return BusinessServiceService(self.repository_factory.create_business_service_repository())

    def get_article_service(self) -> ArticleService:
        """Get ArticleService instance."""
        return ArticleService(self.repository_factory.create_article_repository())

    def get_farmer_incomes_service(self) -> FarmerIncomesService:
        """Get FarmerIncomesService instance."""
        return FarmerIncomesService(self.repository_factory.create_farmer_incomes_repository())

    def get_economic_values_service(self) -> EconomicValuesService:
        """Get EconomicValuesService instance."""
        return EconomicValuesService(self.repository_factory.create_economic_values_repository())

    def get_piaps_records_service(self) -> PiapsRecordsService:
        """Get PiapsRecordsService instance."""
        return PiapsRecordsService(self.repository_factory.create_piaps_records_repository())

    def get_article_rating_service(self) -> ArticleRatingService:
        """Get ArticleRatingService instance."""
        return ArticleRatingService(
            self.repository_factory.create_article_rating_repository(),
            self.repository_factory.create_article_repository(),
        )

    def get_article_comment_service(self) -> ArticleCommentService:
        """Get ArticleCommentService instance."""
        return ArticleCommentService(
            self.repository_factory.create_article_comment_repository(),
            self.repository_factory.create_article_repository(),
        )

    def get_infographic_service(self) -> InfographicService:
        """Get InfographicService instance."""
        return InfographicService(self.repository_factory.create_infographic_repository())

    def get_maps_service(self) -> MapsService:
        """Get MapsService instance."""
        return MapsService(self.repository_factory.create_maps_repository())

    def get_settings_service(self) -> SettingsService:
        """Get SettingsService instance."""
        return SettingsService(self.repository_factory.create_settings_repository())


# Backward compatibility - maintain existing interface
class Factory(ServiceFactory):
    """Legacy Factory class for backward compatibility."""

    def __init__(self):
        super().__init__()
        # Keep static methods for backward compatibility
        self.user_repository = staticmethod(partial(UserRepository, UserModel))
        self.token_repository = staticmethod(partial(TokenRepository, RefreshTokenModel))
        self.file_repository = staticmethod(partial(FileRepository, FileModel))
        self.regional_repository = staticmethod(partial(RegionalRepository, RegionalModel))
        self.forestry_schema_repository = staticmethod(partial(ForestrySchemaRepository, ForestrySchemaModel))
        self.proposal_forestry_status_repository = staticmethod(
            partial(ProposalforestryStatusRepository, ProposalforestryStatusModel)
        )
        self.piaps_repository = staticmethod(partial(PiapsRepository, PiapsModel))
        self.forestry_proposal_repository = staticmethod(partial(ForestryProposalRepository, ForestryProposalModel))
        self.attachment_repository = staticmethod(partial(AttachmentRepository, AttachmentModel))
        self.forestry_land_repository = staticmethod(partial(ForestryLandRepository, ForestryLandModel))
        self.permit_repository = staticmethod(partial(PermitRepository, PermitModel))
        self.navigation_repository = staticmethod(partial(NavigationRepository, NavigationModel))
        self.roles_repository = staticmethod(partial(RolesRepository, RolesModel))
        self.forestry_area_repository = staticmethod(partial(ForestryAreaRepository, ForestryAreaModel))
        self.businesses_repository = staticmethod(partial(BusinessesRepository, BusinessesModel))
        self.business_product_repository = staticmethod(partial(BusinessProductRepository, BusinessProductModel))
        self.business_harvest_repository = staticmethod(partial(BusinessHarvestRepository, BusinessHarvestModel))
        self.commodity_repository = staticmethod(partial(CommodityRepository, CommodityModel))
        self.business_service_repository = staticmethod(partial(BusinessServiceRepository, BusinessServiceModel))
        self.article_repository = staticmethod(partial(ArticleRepository, ArticleModel))
        self.farmer_incomes_repository = staticmethod(partial(FarmerIncomesRepository, IncomeModel))
        self.economic_values_repository = staticmethod(partial(EconomicValuesRepository, EconomicValueModel))
        self.piaps_records_repository = staticmethod(partial(PiapsRecordsRepository, PiapsRecordsModel))
        self.article_rating_repository = staticmethod(partial(ArticleRatingRepository, ArticleRatingModel))
        self.infographic_repository = staticmethod(partial(InfographicRepository))
        self.maps_repository = staticmethod(partial(MapsRepository))
        self.settings_repository = staticmethod(partial(SettingsRepository, SettingsModel))
