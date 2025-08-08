from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies.auth import get_current_user_with_permissions
from app.api.dependencies.factory import Factory
from app.schemas.token_schema import RefreshTokenSchema, Token
from app.schemas.user_schema import UserCreateSchema, UserSchema
from app.services.auth_service import AuthService
from app.utils.limiter import limiter

router = APIRouter()


@router.post("/auth/login", response_model=Token)
@limiter.limit("3/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Factory().get_auth_service),
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await auth_service.create_tokens(user.id)


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    refresh_token: RefreshTokenSchema,
    auth_service: AuthService = Depends(Factory().get_auth_service),
):
    success = await auth_service.logout(refresh_token=refresh_token.refresh_token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot logout")


@router.post("/auth/refresh", response_model=Token)
async def refresh_token(
    refresh_token: RefreshTokenSchema,
    auth_service: AuthService = Depends(Factory().get_auth_service),
):
    return await auth_service.refresh_token(refresh_token.refresh_token)


@router.post("/auth/register", response_model=UserSchema)
@limiter.limit("3/minute")
async def register(
    request: Request,
    user: UserCreateSchema,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> UserSchema:
    return await auth_service.register(user.dict(exclude=None))


@router.get("/me")
async def read_users_me(
    current_user: dict = Depends(get_current_user_with_permissions),
):
    user = current_user
    user.pop("password")
    return user
