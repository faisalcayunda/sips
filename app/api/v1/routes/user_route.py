from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_active_user
from app.api.dependencies.factory import Factory
from app.core.params import CommonParams
from app.schemas.base import PaginatedResponse
from app.schemas.user_schema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services import UserService

router = APIRouter()


@router.get("/users", response_model=PaginatedResponse[UserSchema])
async def get_users(
    params: CommonParams = Depends(),
    user_active: UserSchema = Depends(get_current_active_user),
    service: UserService = Depends(Factory().get_user_service),
):
    """Get paginated list of users."""
    filter = params.filter
    sort = params.sort
    search = params.search
    group_by = params.group_by
    limit = params.limit
    offset = params.offset

    users, total = await service.find_all(
        filters=filter,
        sort=sort,
        search=search,
        group_by=group_by,
        limit=limit,
        offset=offset,
    )

    return PaginatedResponse(
        items=[UserSchema.model_validate(user) for user in users],
        total=total,
        limit=limit,
        offset=offset,
        has_more=total > (offset + limit),
    )


@router.get("/users/{id}", response_model=UserSchema)
async def get_user(
    id: str,
    user: UserSchema = Depends(get_current_active_user),
    service: UserService = Depends(Factory().get_user_service),
):
    """Get user by ID."""
    user = await service.find_by_id(id)
    return user


@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: UserService = Depends(Factory().get_user_service),
):
    """Create new user."""
    user = await service.create(data.model_dump(), current_user)
    return user


@router.patch("/users/{id}", response_model=UserSchema)
async def update_user(
    id: str,
    data: UserUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    service: UserService = Depends(Factory().get_user_service),
):
    """Update existing user."""
    user = await service.update(id, data.model_dump(exclude_unset=True), current_user)
    return user


@router.delete(
    "/users/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_active_user)],
)
async def delete_user(id: str, service: UserService = Depends(Factory().get_user_service)):
    """Delete user by ID."""
    await service.delete(id)
