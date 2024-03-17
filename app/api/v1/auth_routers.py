from typing import Annotated

from fastapi import APIRouter, Depends

from domain.schemas.auth_schemas import (
    AccessTokenSchema,
    RefreshToAccessSchema,
    TokenResponseSchema,
    UserLoginSchema,
)
from domain.services.auth_service import JWTService
from domain.services.user_service import UserService


auth_router = APIRouter(prefix='/auth')


@auth_router.post('/login/')
async def login_user(
    user_login_schema: UserLoginSchema,
    service: Annotated[UserService, Depends(UserService)],
) -> TokenResponseSchema:
    """Login user."""
    return await service.login(user_login_schema)


@auth_router.post('/token_refresh/')
async def refresh_token(
    token_schema: RefreshToAccessSchema,
    service: Annotated[JWTService, Depends(JWTService)],
) -> AccessTokenSchema:
    """Get new access token from refresh token."""
    return service.create_access_token_by_refresh(token_schema.refresh_token)
