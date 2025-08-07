from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError
from pydantic import ValidationError

from app.api.dependencies.factory import Factory
from app.core.security import decode_token
from app.models import UserModel
from app.schemas.token_schema import TokenPayload
from app.schemas.user_schema import UserSchema
from app.services import UserService
from app.utils.cache import get_user_cache

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthManager:
    """
    Dependency class untuk mengelola autentikasi dan otorisasi user.
    Bisa digunakan untuk mengambil user aktif, dengan/atau tanpa permission.
    """

    def __init__(self, error: bool = True, with_permissions: bool = False) -> None:
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        self.error = error
        self.with_permissions = with_permissions

    async def __call__(
        self,
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(Factory().get_user_service),
        request: Request = None,
    ) -> Any:
        """
        Dipanggil oleh FastAPI sebagai dependency.
        """
        return await self.get_current_user(
            token=token,
            user_service=user_service,
            request=request,
            error=self.error,
            with_permissions=self.with_permissions,
            credentials_exception=self.credentials_exception,
        )

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(Factory().get_user_service),
        request: Request = None,
        error: bool = True,
        with_permissions: bool = False,
        credentials_exception: HTTPException = None,
    ) -> Any:
        """
        Validasi token dan kembalikan user aktif.
        Jika error=False, kembalikan None jika tidak valid.
        Jika with_permissions=True, kembalikan user beserta permission.
        """
        # Ambil token dari header jika error=False (opsional, misal untuk endpoint publik)
        if not error and request is not None:
            authorization: str = request.headers.get("Authorization")
            if not authorization:
                return None
            scheme, token = get_authorization_scheme_param(authorization)
            if scheme.lower() != "bearer" or not token:
                return None

        try:
            payload = decode_token(token)
            token_data = TokenPayload(**payload)
            if token_data.type != "access":
                if error and credentials_exception:
                    raise credentials_exception
                return None
            user_id: Optional[str] = token_data.sub
            if user_id is None:
                if error and credentials_exception:
                    raise credentials_exception
                return None
        except (JWTError, ValidationError):
            if error and credentials_exception:
                raise credentials_exception
            return None

        user = await get_user_cache(user_id)
        if not user:
            user = await user_service.find_by_id(user_id)

        if user is None:
            if error and credentials_exception:
                raise credentials_exception
            return None
        if isinstance(user, dict):
            user = UserSchema(**user)
        if not (isinstance(user.enable, str) and user.enable.lower() == "y"):
            if error:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
            return None

        if not with_permissions:
            return user

        return await user_service.find_by_id_with_permissions(user.id)


async def get_only_payload(
    current_user: UserModel = Depends(AuthManager(error=True)),
):
    """
    Dependency untuk mengambil user dari token (tanpa permission).
    """
    return current_user


async def get_current_user_with_permissions(
    current_user: Dict = Depends(AuthManager(with_permissions=True)),
):
    """
    Dependency untuk mengambil user beserta permission.
    """
    return current_user


async def get_current_active_user(
    current_user: UserModel = Depends(AuthManager()),
) -> UserModel:
    """
    Dependency untuk memastikan user aktif.
    """
    if not (isinstance(current_user.enable, str) and current_user.enable.lower() == "y"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
