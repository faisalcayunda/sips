from functools import partial

from app.core.minio_client import MinioClient
from app.models import (
    FileModel,
    RefreshTokenModel,
    UserModel,
)
from app.repositories import (
    FileRepository,
    TokenRepository,
    UserRepository,
)
from app.services import (
    AuthService,
    FileService,
    UserService,
)


class Factory:
    user_repository = staticmethod(partial(UserRepository, UserModel))
    token_repository = staticmethod(partial(TokenRepository, RefreshTokenModel))
    file_repository = staticmethod(partial(FileRepository, FileModel))

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
