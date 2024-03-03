from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import (
    AccessTokenSchema,
    RefreshToAccessSchema,
    TokenResponseSchema,
    UserLoginSchema,
    UserQueriesSchema,
    UserRegistrationResponseSchema,
    UserRegistrationSchema,
    UserSchema,
)
from users.services import JWTService, UserService


router = APIRouter(prefix='/users')


@router.get('/')
async def get_users(
    service: Annotated[UserService, Depends(UserService)],
    queries: Annotated[UserQueriesSchema, Depends(UserQueriesSchema)],
) -> list[UserSchema | None]:
    """Get collection of users."""
    return await service.get(queries)


@router.get('/{id}/')
async def get_user(
    service: Annotated[UserService, Depends(UserService)], id: int
) -> UserSchema | None:
    """Get user by id."""
    return await service.get_by_id(id)


@router.post('/signup/')
async def post_user(
    reg_user: UserRegistrationSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> UserRegistrationResponseSchema:
    """Register new user."""
    return await service.create(reg_user)


@router.post('/login/')
async def login_user(
    user_login_scheme: UserLoginSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> TokenResponseSchema:
    """Login user."""
    return await service.login(user_login_scheme)


@router.post('/token_refresh/')
async def refresh_token(
    token_schema: RefreshToAccessSchema,
    service: Annotated[JWTService, Depends(JWTService)],
) -> AccessTokenSchema:
    """Get new access token from refresh token."""
    return service.create_access_token_from_refresh(token_schema.refresh_token)


# @router.get('/me/')
# async def get_current_user_info()
