from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError
from pydantic import ValidationError
from pytz import timezone

from app.api.dependencies.factory import Factory
from app.core.config import settings
from app.core.security import decode_token
from app.models import UserModel
from app.schemas.token_schema import TokenPayload
from app.schemas.user_schema import UserSchema
from app.services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(Factory().get_user_service),
) -> UserModel:
    """Validate token and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)

        if token_data.type != "access":
            raise credentials_exception

        user_id: Optional[str] = token_data.sub
        if user_id is None:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await user_service.find_by_id(user_id)
    if user is None:
        raise credentials_exception

    if not user.enable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user


async def get_only_payload(
    request: Request, user_service: UserService = Depends(Factory().get_user_service)
):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None

    scheme, token = get_authorization_scheme_param(authorization)

    if scheme.lower() != "bearer" or not token:
        return None

    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)

        if token_data.exp >= datetime.now(timezone(settings.TIMEZONE)):
            return None

        user_id: Optional[str] = token_data.sub
        if user_id is None:
            return None

        user = await user_service.find_by_id(user_id)
        if user is None:
            return None

        return user

    except (JWTError, ValidationError):
        return None


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """Check if current user is active."""
    if not current_user.enable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
